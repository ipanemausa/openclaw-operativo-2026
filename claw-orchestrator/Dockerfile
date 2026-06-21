FROM python:3.11-slim
WORKDIR /app
RUN pip install flask redis --no-cache-dir
COPY app/orchestrator.py .
EXPOSE 8090
CMD ["python", "orchestrator.py"]
