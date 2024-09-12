FROM python:3.12-alpine


RUN apk add --no-cache redis postgresql-client build-base postgresql-dev

COPY requirements.txt /temp/requirements.txt
COPY service /service


WORKDIR /service

RUN pip install -r /temp/requirements.txt


RUN adduser -D service-adduser
RUN chown -R service-adduser /service

USER service-adduser

EXPOSE 8080