FROM python:3

ADD . /www
WORKDIR /www

RUN python3 -m pip install -U pip
RUN pip3 install flask
RUN pip3 install uwsgi

CMD uwsgi uwsgi.ini