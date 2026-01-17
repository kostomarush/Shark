#!/usr/bin/env bash
set -euo pipefail

pids=()

term() {
  for pid in "${pids[@]:-}"; do
    kill -TERM "$pid" 2>/dev/null || true
  done
  wait || true
}
trap term INT TERM

python3 djnagoPRC/djangoRPC/manage.py runserver 0.0.0.0:8080 &
pids+=("$!")

python3 djnagoPRC/djangoRPC/manage.py grpcserver &
pids+=("$!")

wait -n
exit_code=$?

term
exit "$exit_code"