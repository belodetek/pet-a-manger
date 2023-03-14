FROM mcuadros/ofelia:v0.3.7

RUN apk add --no-cache docker-cli

WORKDIR /usr/src/app

COPY . .

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["/usr/src/app/main.sh"]
