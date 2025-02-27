# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --cache-dir /pip_cache -r requirements.txt

# Copy project files
COPY ./app /app/app

# Ensure app directory is in Python path
ENV PYTHONPATH=/app:$PYTHONPATH
