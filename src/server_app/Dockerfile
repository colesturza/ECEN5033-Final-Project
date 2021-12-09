# syntax=docker/dockerfile:1

FROM python:3

ENV PYTHONUNBUFFERED=1

ADD . /server_app
WORKDIR /server_app

COPY requirements.txt /server_app/
RUN pip install -r requirements.txt

COPY . /server_app/

EXPOSE 8080

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8080"]