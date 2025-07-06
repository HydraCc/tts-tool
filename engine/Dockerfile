# Use official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user (optional, disable if using `user: root`)
RUN useradd --create-home --shell /bin/bash tts-user

# Set working directory to container-side /app
WORKDIR /app

# Copy requirements (relative to build context)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy engine source code into /app
COPY . .

# Install engine package in editable mode
RUN pip install -e .

# Create output/model directories just in case
RUN mkdir -p /app/models /app/output && \
    chown -R tts-user:tts-user /app

# Leave root if needed
# USER tts-user

# Keep container running for dev/debug
CMD ["tail", "-f", "/dev/null"]
