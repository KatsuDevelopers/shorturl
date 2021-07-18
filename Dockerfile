FROM python:3.7.11-slim-buster

USER root
COPY . /code/

RUN apt-get update
RUN pip install -r code/requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code