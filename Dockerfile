FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pip upgrade
RUN pip install --upgrade pip setuptools wheel

# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ACE-Step install (EN SONDA!)
RUN pip install --no-cache-dir \
    "git+https://github.com/ace-step/ACE-Step-1.5.git"

# app
COPY handler.py .

CMD ["python", "handler.py"]
