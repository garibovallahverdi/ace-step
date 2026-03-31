import runpod
import base64
import numpy as np
from scipy.io.wavfile import write as write_wav
import tempfile
import os
import time

def generate_audio(prompt, duration):
    """
    Sadə audio generator - ACE-Step əvəzinə demo
    """
    print(f"🎵 Generating: {prompt}")
    
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Sadə melodiya
    frequency = 440  # A4
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Harmonikalar
    audio += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
    audio += 0.2 * np.sin(2 * np.pi * frequency * 3 * t)
    
    # Normalize
    audio = audio / np.max(np.abs(audio))
    audio_int16 = (audio * 32767).astype(np.int16)
    
    # WAV faylı yarat
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write_wav(temp_file.name, sample_rate, audio_int16)
    
    # Base64-ə çevir
    with open(temp_file.name, "rb") as f:
        audio_bytes = f.read()
    
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    
    # Təmizlik
    os.unlink(temp_file.name)
    
    return {
        "audio_base64": audio_base64,
        "sample_rate": sample_rate,
        "duration": duration,
        "format": "wav"
    }

def handler(job):
    """
    RunPod-un çağıracağı əsas funksiya
    """
    try:
        print(f"📥 Job received: {job}")
        
        # İnputları al
        job_input = job.get("input", {})
        prompt = job_input.get("prompt", "default melody")
        duration = int(job_input.get("duration", 10))
        
        print(f"🔄 Processing: prompt='{prompt}', duration={duration}")
        
        # Audio yarat
        result = generate_audio(prompt, duration)
        
        print(f"✅ Job completed successfully")
        
        # RunPod-un gözlədiyi format
        return {
            "status": "success",
            "output": result
        }
        
    except Exception as e:
        print(f"❌ Job failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

# RunPod serverless başlat
if __name__ == "__main__":
    print("🚀 RunPod Serverless Handler Starting...")
    print("⏳ Waiting for jobs...")
    runpod.serverless.start({"handler": handler})
