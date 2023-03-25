FROM python:3.10-slim-bullseye

EXPOSE 5000

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install default-libmysqlclient-dev python-dev gcc -y

COPY ./requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /src/app

RUN echo "from app.app import create_app" > wsgi.py
RUN echo "application = create_app()" >> wsgi.py
