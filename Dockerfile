FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# RunPod SDK
RUN pip install runpod

# ACE-Step clone
RUN git clone https://github.com/ace-step/ACE-Step-1.5.git

COPY handler.py .

CMD ["python", "handler.py"]
