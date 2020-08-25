#!/usr/bin/env bash
set -xeEuo pipefail

docker-compose run --rm app lint
