# Use official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user (optional, disable if using `user: root` in compose)
RUN useradd --create-home --shell /bin/bash tts-user

# Set working directory to container-side /app
WORKDIR /app

# Copy Python dependency definitions
COPY requirements.txt .
COPY setup.py .

# Install Python dependencies and your package (editable mode)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

# Copy actual engine package (your codebase)
COPY engine/ engine/

# Create persistent directories and set permissions
RUN mkdir -p /app/engine/models /app/engine/output && \
    chown -R tts-user:tts-user /app

# Optional: drop privileges
# USER tts-user

# Keep container alive for development
CMD ["tail", "-f", "/dev/null"]
