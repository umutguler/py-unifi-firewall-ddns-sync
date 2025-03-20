#!/usr/bin/env bash
#
# entrypoint.sh
# - Copies default config files from /app/assets to /config if missing
# - Sets up crontab from environment variables
# - Optionally runs the script once immediately
# - Then execs the container CMD

set -e

echo "[entrypoint.sh] Starting entrypoint..."

########################################
# Copy default configs if not present  #
########################################

if [ -d "/app/assets" ] && [ -d "/config" ]; then
  for default_file in /app/assets/*; do
    basefile="$(basename "$default_file")"
    target="/config/$basefile"
    if [ ! -f "$target" ]; then
      echo "[entrypoint.sh] Copying default config: $basefile -> $target"
      cp "$default_file" "$target"
    fi
  done
fi

#####################
# Handle CRON_VARS  #
#####################
if [ -n "${CRON_MINS}" ]; then
  if [[ "${CRON_MINS}" =~ ^[0-9]+$ ]]; then
    CRON_MINS="*/${CRON_MINS}"
  fi
else
  CRON_MINS="*"
fi

if [ -n "${CRON_HOURS}" ]; then
  if [[ "${CRON_HOURS}" =~ ^[0-9]+$ ]]; then
    CRON_HOURS="*/${CRON_HOURS}"
  fi
else
  CRON_HOURS="*"
fi

if [ -n "${CRON_DAYS}" ]; then
  if [[ "${CRON_DAYS}" =~ ^[0-9]+$ ]]; then
    CRON_DAYS="*/${CRON_DAYS}"
  fi
else
  CRON_DAYS="*"
fi

if [ "${CRON_MINS}" = "*" ] && [ "${CRON_HOURS}" = "*" ] && [ "${CRON_DAYS}" = "*" ]; then
  echo "[entrypoint.sh] ERROR: CRON_MINS, CRON_HOURS, CRON_DAYS are all '*' - aborting."
  exit 1
fi

echo "[entrypoint.sh] CRON schedule => Mins: ${CRON_MINS}, Hours: ${CRON_HOURS}, Days: ${CRON_DAYS}"
echo

######################
# Build script ARGS  #
######################
ARGS=()

if [ -n "${UNIFI_GATEWAY}" ]; then
  if [ "${UNIFI_GATEWAY_HTTPS}" = "true" ]; then
    GATEWAY_URL="https://${UNIFI_GATEWAY}"
  else
    GATEWAY_URL="http://${UNIFI_GATEWAY}"
  fi
  ARGS+=("-g" "${GATEWAY_URL}")
fi

if [ -n "${UNIFI_USERNAME}" ]; then
  ARGS+=("-u" "${UNIFI_USERNAME}")
fi

if [ -n "${UNIFI_PASSWORD}" ]; then
  ARGS+=("-p" "${UNIFI_PASSWORD}")
fi

if [ -n "${UNIFI_SITE}" ]; then
  ARGS+=("--site" "${UNIFI_SITE}")
fi

if [ -n "${UNIFI_SITE_ID}" ]; then
  ARGS+=("--siteid" "${UNIFI_SITE_ID}")
fi

if [ "${UNIFI_NO_VERIFY_SSL}" = "true" ]; then
  ARGS+=("--no-verify-ssl")
fi

if [ -n "${UNIFI_RULE_FILENAME}" ]; then
  ARGS+=("--file" "/config/${UNIFI_RULE_FILENAME}")
fi

echo "[entrypoint.sh] Arguments built."
echo

##########################
# Optional Immediate Run #
##########################
if [ "${RUN_ONCE}" = "true" ]; then
  echo "[entrypoint.sh] RUN_ONCE is true; running script once immediately..."
  python /app/src/unifi_firewall_ddns_sync.py "${ARGS[@]}"
  echo
fi

ARGS_STRING=""
for arg in "${ARGS[@]}"; do
  ARGS_STRING="$ARGS_STRING \"$arg\""
done

CRON_SCHEDULE="${CRON_MINS} ${CRON_HOURS} ${CRON_DAYS} * *"
CRON_CMD="${CRON_SCHEDULE} python /app/src/unifi_firewall_ddns_sync.py${ARGS_STRING} > /proc/1/fd/1 2>/proc/1/fd/2"

echo "[entrypoint.sh] Setting up crontab schedule:"
echo "${CRON_SCHEDULE}"
echo

mkdir -p /var/spool/cron/crontabs
echo "${CRON_CMD}" > /var/spool/cron/crontabs/root

echo "[entrypoint.sh] Entry point complete. Executing CMD: $@"
echo

exec "$@"
