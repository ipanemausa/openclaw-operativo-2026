FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde la raíz
COPY ../requirements.txt .

RUN pip install -r requirements.txt

# Copiar el código del gateway
COPY . .

CMD ["python", "gateway.py"]
