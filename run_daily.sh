#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -x venv/bin/python ]; then
    printf '%s\n' 'Environnement absent : exécutez ./setup.sh.' >&2
    exit 1
fi
mkdir -p logs
printf '%s: Début du journal quotidien\n' "$(date)" >> logs/daily.log
if venv/bin/python main.py >> logs/daily.log 2>&1; then
    exit_code=0
else
    exit_code=$?
fi
printf '%s: Fin du journal quotidien (code %s)\n' "$(date)" "$exit_code" >> logs/daily.log
find logs -name '*.log' -mtime +30 -delete
exit "$exit_code"
