#!/bin/sh

DOMAIN="$1"
SAMPLE="$2"
OUTPUT="$3"

# Change domain
sed "s/<DOMAIN>/${DOMAIN}/g" "${SAMPLE}" > "${OUTPUT}"

# Reload config
caddy reload --adapter caddyfile --config "${OUTPUT}"
