FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto del servicio app
EXPOSE 5000

# Arrancar con Gunicorn apuntando a app.py
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
