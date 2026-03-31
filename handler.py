import os
import io
import uuid
import boto3
import runpod
import torch
import torchaudio
from diffusers import AudioLDM2Pipeline # ACE-Step adətən AudioLDM2 arxitekturasıdır

# --- Supabase S3 Ayarları ---
S3_ACCESS_KEY="1c1662d6ea35d30e1428e4afe11f81d5"
S3_SECRET_KEY="2e07ed2d9ab9542afd91783626a373648b2baf3d7bc434891f44c46f24f7494c"
S3_ENDPOINT="https://kgizqvyekmadsorqpbpc.storage.supabase.co/storage/v1/s3"
BUCKET_NAME="music"
REGION_NAME="ap-southeast-2"

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=REGION_NAME
)

# 1. Modelin Yüklənməsi (GPU-ya köçürülür)
def load_model():
    print("🚀 ACE-Step (AudioLDM2) Model yüklənir... Bu bir az vaxt ala bilər.")
    # ACE-Step 1.5 üçün ən stabil model budur:
    repo_id = "cvssp/audioldm2-music" 
    pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
    pipe.to("cuda")
    print("✅ Model tam yükləndi!")
    return pipe

# Modeli bir dəfə global olaraq yükləyirik
model_pipe = load_model()

def handler(job):
    try:
        job_input = job['input']
        prompt = job_input.get("text", "Lofi hip hop beat, calm and relaxing")
        duration = job_input.get("duration", 10) # Saniyə
        
        # 2. Musiqi Yaratma Prosesi (Real Model İşi)
        print(f"🎵 Musiqi yaradılır: {prompt}")
        
        # ACE-Step / AudioLDM2 səs yaradan hissə
        with torch.inference_mode():
            # audio_length_in_s modelin neçə saniyəlik səs yaradacağını təyin edir
            audio_output = model_pipe(
                prompt, 
                audio_length_in_s=duration, 
                num_inference_steps=50 # Keyfiyyət üçün 50 addım
            ).audios[0]

        # Numpy massivini Tensor-a çeviririk
        audio_tensor = torch.from_numpy(audio_output).unsqueeze(0)
        sample_rate = 16000 # AudioLDM2 adətən 16kHz çıxış verir

        # 3. Səsi RAM-da WAV kimi hazırlamaq
        buffer = io.BytesIO()
        torchaudio.save(buffer, audio_tensor, sample_rate, format="wav", backend="soundfile")
        buffer.seek(0)

        # 4. Fayl Adı
        file_name = f"ace_{uuid.uuid4()}.wav"
        
        # 5. S3-ə Yükləmə
        s3_client.upload_fileobj(
            buffer, 
            BUCKET_NAME, 
            file_name,
            ExtraArgs={'ContentType': 'audio/wav'}
        )

        base_url = S3_ENDPOINT.replace("/storage/v1/s3", "")
        public_url = f"{base_url}/storage/v1/object/public/{BUCKET_NAME}/{file_name}"

        return {
            "status": "success",
            "url": public_url,
            "filename": file_name,
            "prompt": prompt
        }

    except Exception as e:
        return {"status": "error", "message": f"Xəta: {str(e)}"}

runpod.serverless.start({"handler": handler})
