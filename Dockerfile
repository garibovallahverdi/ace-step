FROM runpod/pytorch:2.1.0-py3.11-cuda11.8.0-devel

WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir git+https://github.com/ACE-Step/ACE-Step-1.5.git

COPY handler.py .

CMD ["python", "handler.py"]
