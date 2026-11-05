# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for video processing, decryption, and python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    aria2 \
    mediainfo \
    libmagic1 \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency definition and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure helper binaries in ott/ have execution permissions
RUN chmod +x ott/aria2c ott/mp4decrypt 2>/dev/null || true

# Command to run the bot
CMD ["python3", "bot.py"]
