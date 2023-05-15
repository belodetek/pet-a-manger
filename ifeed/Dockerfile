FROM arm32v6/python:3.10-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache \
    bash \
    py3-requests \
    py3-rpigpio \
    py3-tz \
    vim

COPY . .

CMD [ "sleep", "infinity" ]
