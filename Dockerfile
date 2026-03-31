# PyTorch və CUDA dəstəkli rəsmi RunPod imici
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Sistem paketlərini yeniləyirik və səs emalı üçün ffmpeg + sox quraşdırırıq
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsox-dev \
    && rm -rf /var/lib/apt/lists/*

# İş qovluğu
WORKDIR /

# Kitabxanaları yükləyirik
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları içəri kopyalayırıq
COPY handler.py .

# Handler-i başladırıq
CMD [ "python", "-u", "/handler.py" ]
