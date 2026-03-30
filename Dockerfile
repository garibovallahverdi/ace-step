FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# system deps
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 🔥 MINICONDA install
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

# 🔥 Python 3.11 env
RUN conda create -y -n ace python=3.11
SHELL ["conda", "run", "-n", "ace", "/bin/bash", "-c"]

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

CMD ["conda", "run", "-n", "ace", "python", "handler.py"]
