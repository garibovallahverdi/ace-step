FROM python:3.11-slim
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch (CPU version)
RUN pip install --upgrade pip setuptools wheel
RUN pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install TTS (Coqui)
RUN pip install TTS

# Copy application code
COPY handler.py .

CMD ["python3", "handler.py"]
