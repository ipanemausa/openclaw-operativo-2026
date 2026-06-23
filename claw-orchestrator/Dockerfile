FROM python:3.11-slim
WORKDIR /app
RUN pip install flask redis docker --no-cache-dir
COPY app/ .
EXPOSE 8090
CMD ["python", "orchestrator.py"]