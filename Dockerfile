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
RUN pip install runpod

# ACE-Step clone
RUN git clone https://github.com/ace-step/ACE-Step-1.5.git

# Simvolik link yarat - köhnə yol üçün
RUN ln -s /app/ACE-Step-1.5 /app/acestep

# ACE-Step dependencies
RUN cd ACE-Step-1.5 && \
    pip install --no-cache-dir -r requirements.txt || true

COPY handler.py .

CMD ["python", "handler.py"]
