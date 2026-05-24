FROM openclaw-operativo-2026-app:latest

# Instalar herramientas adicionales
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python packages para video + IA
RUN pip install --no-cache-dir \
    opencv-python \
    ffmpeg-python \
    google-generativeai

WORKDIR /workspace
VOLUME /workspace

CMD ["/bin/bash"]
