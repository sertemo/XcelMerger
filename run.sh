#! /bin/bash

docker image prune -af
docker-compose down
docker-compose build
docker-compose up