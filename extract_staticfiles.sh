#!/bin/bash

rm -fr staticfiles

container_id=$(docker create 949266541515.dkr.ecr.eu-west-1.amazonaws.com/ci-hackathon-app:$1)
docker cp $container_id:/hackathon-app/static ./staticfiles
docker rm -v $container_id

