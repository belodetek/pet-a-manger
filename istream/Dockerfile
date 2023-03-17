FROM arm32v6/alpine:3

RUN apk add --no-cache \
    bash \
    curl \
    ffmpeg \
    jq \
    raspberrypi

ENV PATH="/opt/vc/bin:${PATH}"

CMD ["sleep", "infinity"]
