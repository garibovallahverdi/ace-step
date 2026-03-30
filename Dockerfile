FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git ffmpeg libgl1 build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# ACE‑Step source
RUN git clone https://github.com/ACE-Step/ACE-Step-1.5.git /app/ace-step

WORKDIR /app/ace-step

# uv install deps & sync
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv sync

COPY handler.py /app/

CMD ["uv", "run", "acestep-api"]
