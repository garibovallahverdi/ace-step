FROM runpod/pytorch:1.0.3-cu1300-torch291-ubuntu2404

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Python packages
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# ACE-Step (və ya digər repo‑ları)
# Note: ACE-Step pip install bu image ilə uyğun olmalıdır,
# əgər problem gəlsə, biz model load yoluna keçəcəyik.
RUN pip install --no-cache-dir \
    "git+https://github.com/ACE-Step/ACE-Step-1.5.git"

# KODUN
COPY handler.py .

CMD ["python3", "handler.py"]
