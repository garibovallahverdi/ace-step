# Base image: RunPod-un ACE-Step ilə uyğun PyTorch image-i
FROM runpod/pytorch:2.1.0-py3.11-cuda11.8-runtime

WORKDIR /app

# Non-interactive apt
ENV DEBIAN_FRONTEND=noninteractive

# Sistem dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python packages
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Sənin kodu
COPY handler.py .

# RunPod entrypoint
CMD ["python", "handler.py"]
