#!/bin/bash


docker build -t crawler-ingredient -f IngredientCrawlerDockerfile .
docker image tag crawler-ingredient:latest hakankaynar/crawler-ingredient:latest
#docker push hakankaynar/ingredient:latest
