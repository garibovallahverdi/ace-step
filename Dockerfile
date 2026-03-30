FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# 🔥 interactive problemləri söndür
ENV DEBIAN_FRONTEND=noninteractive

# 🔥 system + Python 3.11 qururuq
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-distutils \
    python3.11-venv \
    python3-pip \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# 🔥 default python → 3.11 edirik
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# 🔥 pip upgrade (3.11 üçün)
RUN python3 -m pip install --upgrade pip setuptools wheel

# requirements
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# 🔥 ACE-Step (indi artıq error verməyəcək)
RUN python3 -m pip install --no-cache-dir \
    "git+https://github.com/ACE-Step/ACE-Step-1.5.git"

# kod
COPY handler.py .

CMD ["python3", "handler.py"]
