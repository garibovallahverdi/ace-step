FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# 🔥 lazımlı system paketlər
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# pip update
RUN pip install --upgrade pip setuptools wheel

# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 ACE-Step install (fix ilə)
RUN pip install --no-cache-dir \
    "git+https://github.com/ACE-Step/ACE-Step-1.5.git"

# kod
COPY handler.py .

CMD ["python", "handler.py"]
