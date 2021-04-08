#!/bin/bash

exec gunicorn --graceful-timeout 25 --max-requests 100000 --max-requests-jitter 2000 -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 fastapi_jaeger:app
