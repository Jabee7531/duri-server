FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /srv/dori_server
RUN mkdir /srv/log
RUN mkdir /srv/log/nginx
RUN mkdir /srv/log/uwsgi
RUN mkdir /sock

ADD ./. /srv/dori_server

WORKDIR /srv/dori_server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80