#!/bin/sh

set -axe

function cleanup() {
    rm -f "${globconfig}" "${jobconfig}" "${config}"
    sleep infinity
}
trap cleanup EXIT

IFEED_SCHEDULE=${IFEED_SCHEDULE:-15 2 6 * * *}
IFEED_SLACK_ERRORS_ONLY=${IFEED_SLACK_ERRORS_ONLY:-true}

name="$(docker ps -q --filter 'name=ifeed*' --format '{{.Names}}')"

globconfig="$(mktemp)"
jobconfig="$(mktemp)"
config="$(mktemp)"

cat << EOF > "${globconfig}"
[global]
slack-only-on-error = ${IFEED_SLACK_ERRORS_ONLY}
slack-webhook = ${IFEED_SLACK_WEBHOOK_URL}

EOF

cat << EOF >> "${jobconfig}"
[job-exec "ifeed"]
schedule = ${IFEED_SCHEDULE}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR2'

[job-local "self-immolate"]
schedule = @every 15m
command = kill -s SIGTERM 1
EOF

if [[ -n "$IFEED_SLACK_WEBHOOK_URL" ]]; then
    cat < "${globconfig}" > "${config}"
fi
cat < "${globconfig}" > "${config}"
cat < "${jobconfig}" >> "${config}"
cat < "${config}"

exec ofelia daemon --config="${config}"
