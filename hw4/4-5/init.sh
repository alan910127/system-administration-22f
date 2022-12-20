#!/bin/sh

BASE="/home/judge/hw4/4-5"
VENV="${BASE}/.venv"
PIP="${VENV}/bin/pip"

python3 -m venv "${VENV}"
"${PIP}" install -r "${BASE}/data/requirements.txt"