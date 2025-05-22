FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

WORKDIR /app

COPY requirements.txt requirements.txt
# use poetry or remove it from source.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
