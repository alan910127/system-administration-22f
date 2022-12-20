#!/bin/sh

DOMAIN="$1"

until curl "https://${DOMAIN}"; do
    echo "* Server is starting..."
done
