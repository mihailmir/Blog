FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
COPY . /code/
WORKDIR /code/

RUN pip install -r /code/requirements.txt

