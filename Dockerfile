FROM python:3.10-slim-bullseye

EXPOSE 5000

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install default-libmysqlclient-dev python-dev gcc -y

COPY ./app/requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY ./app src/app
COPY ./local src/local

WORKDIR src

RUN echo "from app.app import create_app" > wsgi.py
RUN echo "application = create_app()" >> wsgi.py

CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
