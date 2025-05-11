#!/bin/sh
set -e

exec gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  --reload \
  --bind 0.0.0.0:${REST_PORT} \
  --workers 1