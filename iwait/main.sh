#!/bin/sh

set -axe

function cleanup() {
    rm -f "${globconfig}" "${jobconfig}" /etc/ofelia.conf
    sleep infinity
}
trap cleanup EXIT

IWAIT_MEAL_SCHEDULE=${IWAIT_MEAL_SCHEDULE:-15 2 6 * * *}
IWAIT_MEAL_TRIGGER_CMD=${IWAIT_MEAL_TRIGGER_CMD:-/bin/bash -c \'pgrep python3.10 | xargs kill -s USR2\'}
IWAIT_SLACK_ERRORS_ONLY=${IWAIT_SLACK_ERRORS_ONLY:-true}
# semicolon separated cron expressions with commas replacing spaces
IWAIT_SNACK_SCHEDULES=${IWAIT_SNACK_SCHEDULES:-42,32,12,*,*,*;24,01,19,*,*,*}
IWAIT_SNACK_TRIGGER_CMD=${IWAIT_SNACK_TRIGGER_CMD:-/bin/bash -c \'pgrep python3.10 | xargs kill -s USR1\'}
IWAIT_IFEED_CONTAINER_NAME=${IWAIT_IFEED_CONTAINER_NAME:-$(docker ps -q --filter 'name=ifeed*' --format '{{.Names}}')}

globconfig="$(mktemp)"
jobconfig="$(mktemp)"

cat << EOF > "${globconfig}"
[global]
slack-only-on-error = ${IWAIT_SLACK_ERRORS_ONLY}
slack-webhook = ${IWAIT_SLACK_WEBHOOK_URL}

EOF

cat << EOF > "${jobconfig}"
[job-exec "ifeed"]
schedule = ${IWAIT_MEAL_SCHEDULE}
container = ${IWAIT_IFEED_CONTAINER_NAME}
command = ${IWAIT_MEAL_TRIGGER_CMD}

EOF

for schedule in $(echo "${IWAIT_SNACK_SCHEDULES}" | tr ';' ' '); do
    cronexpr="$(echo "${schedule}" | tr ',' ' ')"
    cat << EOF >> "${jobconfig}"
[job-exec "snack-$((RANDOM))"]
schedule = ${cronexpr}
container = ${IWAIT_IFEED_CONTAINER_NAME}
command = ${IWAIT_SNACK_TRIGGER_CMD}

EOF
done

rm -f /etc/ofelia.conf
if [[ -n "$IWAIT_SLACK_WEBHOOK_URL" ]]; then
    cat < "${globconfig}" > /etc/ofelia.conf
fi
cat < "${jobconfig}" >> /etc/ofelia.conf
cat < /etc/ofelia.conf

exec ofelia daemon
