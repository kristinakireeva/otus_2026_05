FROM python:3.10-slim

# 1. Устанавливаем Firefox и системные библиотеки для его работы в Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# 2. Устанавливаем Python-зависимости (включая PyYAML)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pyyaml \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["pytest"]
