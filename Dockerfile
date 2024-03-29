FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /webcrm

COPY requirements.txt /webcrm/
RUN pip install -r requirements.txt
RUN python -m pip install Pillow django_select2 django-storages boto3 django-recaptcha reportlab pytest-django unidecode django-cors-headers

COPY . .
