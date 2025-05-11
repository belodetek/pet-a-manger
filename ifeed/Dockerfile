FROM arm32v6/python:3.12-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache \
    bash \
    py3-requests \
    py3-rpigpio \
    py3-tz \
    py3-flask \
    vim

COPY . .

CMD [ "sleep", "infinity" ]
