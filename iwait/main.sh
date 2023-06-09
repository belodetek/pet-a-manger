#!/bin/sh

set -axe

function cleanup() {
    rm -f "${globconfig}" "${jobconfig}" /etc/ofelia.conf
    sleep infinity
}
trap cleanup EXIT

IWAIT_MEAL_SCHEDULES=${IWAIT_MEAL_SCHEDULES:-21,2,6,*,*,*}
IWAIT_MEAL_TRIGGER_CMD=${IWAIT_MEAL_TRIGGER_CMD:-/bin/bash -c \'pgrep python3 | xargs kill -s USR2\'}
IWAIT_SLACK_ERRORS_ONLY=${IWAIT_SLACK_ERRORS_ONLY:-true}
# semicolon separated cron expressions with commas replacing spaces
IWAIT_SNACK_SCHEDULES=${IWAIT_SNACK_SCHEDULES:-42,2,12,*,*,*;19,1,19,*,*,*}
IWAIT_SNACK_TRIGGER_CMD=${IWAIT_SNACK_TRIGGER_CMD:-/bin/bash -c \'pgrep python3 | xargs kill -s USR1\'}
IWAIT_IFEED_CONTAINER_NAME=${IWAIT_IFEED_CONTAINER_NAME:-$(docker ps -q --filter 'name=ifeed*' --format '{{.Names}}')}
IWAIT_ISTREAM_TRIGGER_CMD=${IWAIT_ISTREAM_TRIGGER_CMD:-/bin/bash -c \'pgrep raspistill | xargs kill -s USR1\'}
IWAIT_ISTREAM_CONTAINER_NAME=${IWAIT_ISTREAM_CONTAINER_NAME:-$(docker ps -q --filter 'name=istream*' --format '{{.Names}}')}

globconfig="$(mktemp)"
jobconfig="$(mktemp)"

cat << EOF > "${globconfig}"
[global]
slack-only-on-error = ${IWAIT_SLACK_ERRORS_ONLY}
slack-webhook = ${IWAIT_SLACK_WEBHOOK_URL}

EOF

for schedule in $(echo "${IWAIT_MEAL_SCHEDULES}" | tr ';' ' '); do
    cronexpr="$(echo "${schedule}" | tr ',' ' ')"
    cat << EOF >> "${jobconfig}"
[job-exec "meal-$((RANDOM))"]
schedule = ${cronexpr}
container = ${IWAIT_IFEED_CONTAINER_NAME}
command = ${IWAIT_MEAL_TRIGGER_CMD}

EOF
done

for schedule in $(echo "${IWAIT_SNACK_SCHEDULES}" | tr ';' ' '); do
    cronexpr="$(echo "${schedule}" | tr ',' ' ')"
    cat << EOF >> "${jobconfig}"
[job-exec "snack-$((RANDOM))"]
schedule = ${cronexpr}
container = ${IWAIT_IFEED_CONTAINER_NAME}
command = ${IWAIT_SNACK_TRIGGER_CMD}

EOF
done

for schedule in $(echo "${IWAIT_ISTREAM_SCHEDULES}" | tr ';' ' '); do
    cronexpr="$(echo "${schedule}" | tr ',' ' ')"
    cat << EOF >> "${jobconfig}"
[job-exec "snap-$((RANDOM))"]
schedule = ${cronexpr}
container = ${IWAIT_ISTREAM_CONTAINER_NAME}
command = ${IWAIT_ISTREAM_TRIGGER_CMD}

EOF
done

rm -f /etc/ofelia.conf
if [[ -n "$IWAIT_SLACK_WEBHOOK_URL" ]]; then
    cat < "${globconfig}" > /etc/ofelia.conf
fi
cat < "${jobconfig}" >> /etc/ofelia.conf
cat < /etc/ofelia.conf
ofelia validate

exec ofelia daemon
