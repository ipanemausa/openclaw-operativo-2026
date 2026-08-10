FROM python:3.11-slim

WORKDIR /app

RUN pip install flask gunicorn requests

COPY . .

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
