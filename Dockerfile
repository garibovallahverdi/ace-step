# ACE-Step 1.5 RunPod Serverless Image
FROM runpod/base:0.6.0-cuda11.8.0

# Sistem asılılıqları
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv-ni quraşdır
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# İş qovluğu
WORKDIR /app

# ACE-Step repository-sini klonla
RUN git clone https://github.com/ace-step/ACE-Step-1.5.git /app/ACE-Step-1.5
WORKDIR /app/ACE-Step-1.5

# Asılılıqları quraşdır (CUDA üçün)
RUN uv sync --frozen --no-dev

# Handler faylını əlavə et
COPY handler.py /app/handler.py

# Port
EXPOSE 8000

# RunPod handler-i işə sal
CMD ["python", "-u", "/app/handler.py"]
