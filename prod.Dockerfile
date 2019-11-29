FROM python:3.8-slim-buster

# handle static files
ENV STATIC_URL /static

# if making changes this should be an absolute path
ENV STATIC_PATH /data/web/static

# set working directory and import /data/web/*
COPY ./data/web /data/web
WORKDIR /data/web

# Make /data/web* available to be imported by Python globally
ENV PYTHONPATH=/data/web

ENV FLASK_APP /data/web/app.py
ENV FLASK_RUN_HOST 0.0.0.0

# install requirements 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["flask", "run"]
