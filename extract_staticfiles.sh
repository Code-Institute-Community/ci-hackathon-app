#!/bin/bash

rm -fr static

container_id=$(docker create 949266541515.dkr.ecr.eu-west-1.amazonaws.com/ci-hackathon-app:$1)
docker cp $container_id:/static ./static
docker rm -v $container_id

