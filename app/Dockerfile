FROM python:3.8.3-alpine

WORKDIR /user/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
