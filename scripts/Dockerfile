FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde la raíz del repo
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del gateway
COPY . .

# Exponer el puerto correcto
EXPOSE 8080

# Comando de arranque
CMD ["python", "gateway.py"]
