FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR .
ADD . .

RUN pip install --no-cache-dir -r requirements.txt
