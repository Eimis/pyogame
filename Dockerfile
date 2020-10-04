FROM python:3-alpine

RUN python -m pip install --upgrade pip
RUN apk update && apk add bash

RUN mkdir /code

COPY requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip3 install -r requirements.txt

COPY . /code
