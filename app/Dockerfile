FROM python:3.10-slim-bullseye

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install default-libmysqlclient-dev python-dev gcc -y

COPY ./requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /src/app
