FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests psycopg2-binary flask-cors --no-cache-dir
COPY . .
EXPOSE 8080
CMD ["python", "app_clean.py"]
