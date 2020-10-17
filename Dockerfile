FROM python:3-alpine

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /code
WORKDIR $APP_DIR

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apk update

ADD . /tmp/local

ADD . /tmp/dstmp

ADD ./src $APP_DIR

CMD python $APP_DIR/app.py


