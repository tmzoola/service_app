FROM python:3.12-alpine


COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8080

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-adduser

USER service-adduser