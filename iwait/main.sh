#!/bin/sh

set -axe

function cleanup() {
    rm -f "${globconfig}" "${jobconfig}" "${config}"
    sleep infinity
}
trap cleanup EXIT

IFEED_MEAL_SCHEDULE=${IFEED_MEAL_SCHEDULE:-15 2 6 * * *}
IFEED_SNACK_SCHEDULE1=${IFEED_SNACK_SCHEDULE1:-42 32 12 * * *}
IFEED_SNACK_SCHEDULE2=${IFEED_SNACK_SCHEDULE2:-24 01 19 * * *}
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
schedule = ${IFEED_MEAL_SCHEDULE}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR2'

[job-exec "isnack1"]
schedule = ${IFEED_SNACK_SCHEDULE1}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR1'

[job-exec "isnack2"]
schedule = ${IFEED_SNACK_SCHEDULE2}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR1'

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
