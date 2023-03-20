FROM mcuadros/ofelia@sha256:441a5ee0cd44d14e295b69ee1aa2cc3b1b73038bfc1b7744c4d9c9103d4badf7

RUN apk add --no-cache docker-cli

WORKDIR /usr/src/app

COPY . .

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["/usr/src/app/main.sh"]
