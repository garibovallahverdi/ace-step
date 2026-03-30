FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# 🔥 BU SƏTİR PROBLEMİ HƏLL EDİR
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir \
    "git+https://github.com/ACE-Step/ACE-Step-1.5.git"

COPY handler.py .

CMD ["python", "handler.py"]
