FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# system deps
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 🔥 Python 3.11 base image əvəzinə image dəyişək
# Bu base image artıq Python 3.11 ilə gəlməlidir
# runpod/pytorch:2.1.0-py3.11-cuda11.8-devel
# yəni burada python upgrade və miniconda lazım deyil

# pip upgrade
RUN pip install --upgrade pip setuptools wheel

# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ACE-Step
RUN pip install --no-cache-dir \
    "git+https://github.com/ACE-Step/ACE-Step-1.5.git"

# kod
COPY handler.py .

CMD ["python", "handler.py"]
