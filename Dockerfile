FROM python:3.7-slim-buster


ADD . /app
COPY ./config.json .
WORKDIR /app
RUN pip install -r requirements.txt