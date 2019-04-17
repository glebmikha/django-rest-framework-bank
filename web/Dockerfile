FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh
COPY ./haarcascade_frontalface_default.xml /haarcascade_frontalface_default.xml

# install psycopg2
RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev netcat \
  #opencv
  libglib2.0-0 libsm6 libxext6 libxrender-dev \
  --no-install-recommends

RUN pip install -r requirements.txt

WORKDIR /app

RUN adduser --disabled-password --gecos '' user

USER user

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
