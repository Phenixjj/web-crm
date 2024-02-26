# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory in the container
WORKDIR /bot-api

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Copy project requirement files here for efficient caching
COPY ./requirements-bot.txt .

# Install project dependencies
RUN pip install -r requirements-bot.txt

# Copy the current directory contents into the container at /bot-api
COPY . /bot-api/

WORKDIR /bot-api/api

# Run the command to start uWSGI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]