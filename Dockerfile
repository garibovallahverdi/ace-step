# Python və CUDA (GPU üçün) olan hazır baza götürürük
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# İş qovluğunu təyin edirik
WORKDIR /

# Kitabxanaları kopyalayıb yükləyirik
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Model fayllarını və kodlarımızı içəri atırıq
COPY handler.py .
# Əgər modelin çəkisi (weights) yerlidirsə, onları da COPY ilə əlavə et

# RunPod handler-i işə salırıq
CMD [ "python", "-u", "/handler.py" ]
