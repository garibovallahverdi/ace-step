import runpod
import subprocess
from pathlib import Path
import uuid
import base64
import os

def handler(job):
    job_input = job["input"]
    prompt = job_input.get("text", "")
    
    if not prompt:
        return {
            "status": "error",
            "message": "No text prompt provided"
        }
    
    # Əvvəlcə ACE-Step qovluğunu yoxla
    ace_step_path = Path("/app/ACE-Step-1.5")
    
    if not ace_step_path.exists():
        return {
            "status": "error",
            "message": f"ACE-Step directory not found at {ace_step_path}"
        }
    
    # requirements-in yükləndiyini yoxla
    print(f"Checking ACE-Step at: {ace_step_path}")
    
    # infer.py faylını yoxla
    infer_py = ace_step_path / "infer.py"
    
    if not infer_py.exists():
        return {
            "status": "error",
            "message": f"infer.py not found at {infer_py}"
        }
    
    # ACE-Step qovluğunda faylları listele (debug üçün)
    try:
        files = list(ace_step_path.glob("*"))
        print(f"Files in ACE-Step: {[f.name for f in files[:10]]}")
    except:
        pass
    
    output_file = Path(f"/tmp/{uuid.uuid4()}.wav")
    
    # Əvvəlcə ACE-Step-in tələblərini yüklə
    try:
        # requirements.txt varsa yüklə
        req_file = ace_step_path / "requirements.txt"
        if req_file.exists():
            print("Installing ACE-Step requirements...")
            subprocess.run(
                ["pip", "install", "-r", str(req_file)],
                cwd=str(ace_step_path),
                capture_output=True,
                timeout=60
            )
    except Exception as e:
        print(f"Requirements install warning: {e}")
    
    # Komanda
    cmd = [
        "python",
        str(infer_py),
        "--text", prompt,
        "--output", str(output_file)
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Komandanı işə sal
        result = subprocess.run(
            cmd,
            cwd=str(ace_step_path),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        
        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"Command failed with code {result.returncode}: {result.stderr}"
            }
        
        # Faylın yaradıldığını yoxla
        if not output_file.exists():
            return {
                "status": "error",
                "message": f"Output file not created: {output_file}"
            }
        
        # Audio faylı oxu
        with open(output_file, "rb") as f:
            audio_data = f.read()
        
        # Base64-ə çevir
        audio_base64 = base64.b64encode(audio_data).decode()
        
        # Təmizlə
        output_file.unlink()
        
        return {
            "status": "success",
            "audio": audio_base64,
            "size_bytes": len(audio_data)
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Command timeout after 120 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
