import runpod
import subprocess
import time
import requests
import json
import base64
import os
import signal
import atexit
from pathlib import Path

# Qlobal proses
api_process = None

def start_ace_step_api():
    """ACE-Step API serverini arxa planda işə salır."""
    global api_process
    try:
        ace_step_dir = Path("/app/ACE-Step-1.5")
        
        # API serverini işə sal
        cmd = ["uv", "run", "acestep-api"]
        
        api_process = subprocess.Popen(
            cmd,
            cwd=ace_step_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True
        )
        
        # Serverin başlaması üçün gözlə
        print("⏳ ACE-Step API server başladılır...")
        time.sleep(15)
        
        # Test sorğusu
        try:
            test_response = requests.get("http://localhost:8001/health", timeout=5)
            if test_response.status_code == 200:
                print("✅ ACE-Step API server hazırdır!")
                return True
        except:
            print("⚠️ Health check gözlənilir...")
            time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ API server başlatma xətası: {e}")
        return False

def cleanup():
    """Təmizləmə funksiyası"""
    global api_process
    if api_process:
        print("🛑 ACE-Step API server dayandırılır...")
        api_process.terminate()
        api_process.wait(timeout=10)

# Təmizləməni qeydə al
atexit.register(cleanup)
signal.signal(signal.SIGTERM, lambda sig, frame: cleanup())

def handler(job):
    """
    RunPod serverless üçün əsas handler funksiyası.
    """
    job_input = job["input"]
    
    # Prompt və parametrləri al
    prompt = job_input.get("prompt", "")
    duration = job_input.get("duration", 30)
    bpm = job_input.get("bpm", 120)
    genre = job_input.get("genre", "pop")
    steps = job_input.get("steps", 8)  # turbo model üçün 8
    cfg_scale = job_input.get("cfg_scale", 1.0)
    
    if not prompt:
        return {"status": "error", "message": "Prompt boş ola bilməz"}
    
    print(f"🎵 Generating music: {prompt[:50]}...")
    
    # ACE-Step API-yə sorğu
    payload = {
        "prompt": prompt,
        "duration": duration,
        "bpm": bpm,
        "genre": genre,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "format": "wav"
    }
    
    try:
        # API-yə POST sorğusu
        response = requests.post(
            "http://localhost:8001/generate",
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"ACE-Step API xətası ({response.status_code}): {response.text}"
            }
        
        result = response.json()
        
        if "audio" in result and result["audio"]:
            return {
                "status": "success",
                "audio": result["audio"],
                "format": "wav",
                "duration": duration,
                "prompt": prompt
            }
        else:
            return {
                "status": "error",
                "message": "ACE-Step API audio data qaytarmadı"
            }
            
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "ACE-Step API vaxt aşımı (120s)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# RunPod serverless başlatma
if __name__ == "__main__":
    print("🚀 ACE-Step RunPod Worker başladılır...")
    
    # API serverini işə sal
    if start_ace_step_api():
        print("✅ API server hazır, handler işə salınır...")
        runpod.serverless.start({"handler": handler})
    else:
        print("❌ API server başlamaq mümkün olmadı!")
        exit(1)
