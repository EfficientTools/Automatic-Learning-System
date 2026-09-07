#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"
"$PYTHON_BIN" -m venv venv
venv/bin/python -m pip install -r requirements.lock
mkdir -p output logs
if [ ! -f .env ]; then
    (umask 077; cp .env.template .env)
fi
printf '%s\n' 'Installation terminée. Configurez .env puis utilisez venv/bin/python.'
printf '%s\n' 'Validation locale : venv/bin/python test_system.py'
printf '%s\n' 'Démo sans réseau : venv/bin/python demo.py'
