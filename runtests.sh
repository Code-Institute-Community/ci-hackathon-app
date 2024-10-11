#! /bin/bash

set -e

docker compose exec hackathon-app python3 manage.py test $1
