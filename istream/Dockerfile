FROM arm32v6/alpine:3 as build

# https://unix.stackexchange.com/a/32184/78029
COPY nweb.c .

RUN apk add --no-cache \
    gcc \
    libc-dev \
    wget \
    && gcc -O -DLINUX nweb.c -o /usr/bin/nweb

FROM arm32v6/alpine:3

COPY --from=build /usr/bin/nweb /usr/bin/

COPY favicon.ico /root/

RUN apk add --no-cache \
    bash \
    curl \
    ffmpeg \
    jq \
    raspberrypi \
    vips-tools

ENV PATH="/opt/vc/bin:${PATH}"

CMD ["sleep", "infinity"]
