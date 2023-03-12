FROM arm32v6/python:3-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache \
    bash \
    py3-rpigpio \
    vim

COPY . .

CMD [ "sleep", "infinity" ]
