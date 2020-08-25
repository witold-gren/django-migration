#!/usr/bin/env bash
set -xeEuo pipefail

docker-compose run --rm app python manage.py makemigrations --check --dry-run
