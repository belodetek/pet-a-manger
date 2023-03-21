#!/bin/sh

set -axe

function cleanup() {
    rm -f "${globconfig}" "${jobconfig}" /etc/ofelia.conf
    sleep infinity
}
trap cleanup EXIT

IWAIT_MEAL_SCHEDULE=${IWAIT_MEAL_SCHEDULE:-15 2 6 * * *}
IWAIT_SNACK_SCHEDULE1=${IWAIT_SNACK_SCHEDULE1:-42 32 12 * * *}
IWAIT_SNACK_SCHEDULE2=${IWAIT_SNACK_SCHEDULE2:-24 01 19 * * *}
IWAIT_SLACK_ERRORS_ONLY=${IWAIT_SLACK_ERRORS_ONLY:-true}

name="$(docker ps -q --filter 'name=ifeed*' --format '{{.Names}}')"

globconfig="$(mktemp)"
jobconfig="$(mktemp)"

cat << EOF > "${globconfig}"
[global]
slack-only-on-error = ${IWAIT_SLACK_ERRORS_ONLY}
slack-webhook = ${IWAIT_SLACK_WEBHOOK_URL}

EOF

cat << EOF >> "${jobconfig}"
[job-exec "ifeed"]
schedule = ${IWAIT_MEAL_SCHEDULE}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR2'

[job-exec "isnack1"]
schedule = ${IWAIT_SNACK_SCHEDULE1}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR1'

[job-exec "isnack2"]
schedule = ${IWAIT_SNACK_SCHEDULE2}
container = ${name}
command = /bin/bash -c 'pgrep python3.10 | xargs kill -s USR1'
EOF

if [[ -n "$IWAIT_SLACK_WEBHOOK_URL" ]]; then
    cat < "${globconfig}" > /etc/ofelia.conf
fi
cat < "${globconfig}" > /etc/ofelia.conf
cat < "${jobconfig}" >> /etc/ofelia.conf
cat < /etc/ofelia.conf

exec ofelia daemon
