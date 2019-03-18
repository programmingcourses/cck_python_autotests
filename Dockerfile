FROM python:3.6-stretch

WORKDIR /root

ADD requirements.txt .
RUN pip install -r requirements.txt
