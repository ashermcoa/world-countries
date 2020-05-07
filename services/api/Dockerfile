FROM python:3.8.0

ENV PYTHONUNBUFFERED 1

RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
  netcat \
  && apt-get -q clean

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app

# add entrypoint.sh
ADD ./entrypoint.sh /usr/src/app/entrypoint.sh

# run server
CMD ["./entrypoint.sh"]
