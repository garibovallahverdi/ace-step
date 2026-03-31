import json
import os
import torch
import torchaudio
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import base64
import io
import wave
import struct
from scipy.io.wavfile import write as write_wav
import tempfile
import time

app = FastAPI()

class MusicRequest(BaseModel):
    prompt: str
    duration: int = 10  # saniyə

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/generate")
async def generate_music(request: MusicRequest):
    try:
        print(f"Generating music for prompt: {request.prompt}")
        print(f"Duration: {request.duration} seconds")
        
        # Burada ACE-Step modelini yükləyib istifadə edəcəksən
        # İndilik demo olaraq sadə bir audio yaradırıq
        
        sample_rate = 22050
        duration = request.duration
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Sadə bir melodiya (süni)
        frequency = 440  # A4 notası
        audio = 0.5 * np.sin(2 * np.pi * frequency * t)
        
        # Harmonik əlavə et
        audio += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
        audio += 0.2 * np.sin(2 * np.pi * frequency * 3 * t)
        
        # Normalize
        audio = audio / np.max(np.abs(audio))
        
        # WAV formatına çevir
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Müvəqqəti fayl yarat
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        write_wav(temp_file.name, sample_rate, audio_int16)
        
        # Faylı oxuyub base64-ə çevir
        with open(temp_file.name, "rb") as f:
            audio_data = f.read()
        
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        
        # Müvəqqəti faylı sil
        os.unlink(temp_file.name)
        
        return {
            "status": "success",
            "audio": audio_base64,
            "sample_rate": sample_rate,
            "duration": duration
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
