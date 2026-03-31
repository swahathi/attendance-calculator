FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for mysql-connector and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1   
EXPOSE 5001

CMD ["python", "webapp.py"]
