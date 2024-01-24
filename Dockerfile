FROM python:3.9.18-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk add --no-cache ffmpeg \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
# /web/Dockerfile
# /redis/Dockerfile
# /db/Dockerfile
# /worker/Dockerfile