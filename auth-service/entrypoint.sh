#!/bin/sh
set -e

exec gunicorn src.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${REST_PORT} \
  --workers 1 \
  --reload
