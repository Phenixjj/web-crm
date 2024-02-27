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
    curl \
    && pip install --upgrade pip

# Copy project requirement files here for efficient caching
COPY ./requirements-bot.txt .

# Install project dependencies
RUN pip install -r requirements-bot.txt
RUN pip install requests

# Copy the current directory contents into the container at /bot-api
COPY . /bot_api/

WORKDIR /bot_api/api

# Run the command to start uWSGI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]