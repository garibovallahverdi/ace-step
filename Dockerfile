FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# system deps
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pip
RUN pip install --upgrade pip setuptools wheel

# əsas python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 ACE-Step clone (pip YOX!)
RUN git clone https://github.com/ace-step/ACE-Step-1.5.git /app/acestep

# working dir dəyiş
WORKDIR /app/acestep

# ACE-Step öz requirements
RUN pip install --no-cache-dir -r requirements.txt || true

# geri dön
WORKDIR /app

# sənin handler
COPY handler.py .

CMD ["python", "handler.py"]
