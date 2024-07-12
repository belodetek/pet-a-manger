FROM arm32v6/python:3-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache \
    bash \
    py3-requests \
    py3-rpigpio \
    py3-tz \
    vim

# https://github.com/python/cpython/issues/120788#issuecomment-2181130364
RUN rm -rf /usr/lib/python3.12/lib-dynload

COPY . .

CMD [ "sleep", "infinity" ]
