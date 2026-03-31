import os
import io
import uuid
import boto3
import runpod
import torch
import torchaudio

# --- Supabase S3 Ayarları (Bunları öz məlumatlarınla doldur) ---
S3_ACCESS_KEY="1c1662d6ea35d30e1428e4afe11f81d5"
S3_SECRET_KEY="2e07ed2d9ab9542afd91783626a373648b2baf3d7bc434891f44c46f24f7494c"
S3_ENDPOINT="https://kgizqvyekmadsorqpbpc.storage.supabase.co/storage/v1/s3"
BUCKET_NAME="music"
REGION_NAME="ap-southeast-2"

# S3 Müştərisini sazlayırıq
s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=REGION_NAME
)

def load_model():
    print("Model yüklənir...")
    # ACE-Step modelini yükləmə kodunu bura əlavə edə bilərsən
    return None

model_instance = load_model()

def handler(job):
    try:
        job_input = job['input']
        text = job_input.get("text", "Default song")
        
        # 1. Musiqi Yaratma Prosesi
        # ACE-Step modelin hazır olanda bura yerləşdir:
        # audio_tensor, sample_rate = model_instance.generate(text)
        
        # TEST ÜÇÜN: 5 saniyəlik boş səs yaradırıq
        audio_tensor = torch.randn(1, 44100 * 5) 
        sample_rate = 44100

        # 2. Səsi Yaddaşda (RAM) WAV kimi hazırlamaq
        buffer = io.BytesIO()
        # 'soundfile' backend-indən istifadə edərək daha stabil saxlama
        torchaudio.save(buffer, audio_tensor, sample_rate, format="wav", backend="soundfile")
        buffer.seek(0)

        # 3. Fayl Adı (Unikal ID)
        file_name = f"music_{uuid.uuid4()}.wav"
        
        # 4. S3-ə (Supabase Storage) Yükləmə
        s3_client.upload_fileobj(
            buffer, 
            BUCKET_NAME, 
            file_name,
            ExtraArgs={'ContentType': 'audio/wav'}
        )

        # 5. Public URL-in Yaradılması
        # Supabase URL formatı: https://[ID].supabase.co/storage/v1/object/public/[BUCKET]/[FILE]
        base_url = S3_ENDPOINT.replace("/storage/v1/s3", "")
        public_url = f"{base_url}/storage/v1/object/public/{BUCKET_NAME}/{file_name}"

        return {
            "status": "success",
            "url": public_url,
            "filename": file_name
        }

    except Exception as e:
        return {"status": "error", "message": f"Xəta baş verdi: {str(e)}"}

# RunPod Worker-i başladırıq
runpod.serverless.start({"handler": handler})
