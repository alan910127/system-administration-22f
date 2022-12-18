#!/bin/sh

DOMAIN="$1"

sudo sed -i "" "s/[a-zA-Z0-9-]*.28.nasa.nycu/${DOMAIN}/" /etc/hosts
