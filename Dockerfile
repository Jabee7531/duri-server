FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /srv/duri_server
RUN mkdir /srv/log
RUN mkdir /srv/log/nginx
RUN mkdir /srv/log/uwsgi
RUN mkdir /sock

ADD ./. /srv/duri_server

WORKDIR /srv/duri_server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80