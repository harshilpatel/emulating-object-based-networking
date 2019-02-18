#!/bin/bash

docker rm $(docker stop $(docker ps -a -q --filter ancestor=rpc-client)) &
docker rm $(docker stop $(docker ps -a -q --filter ancestor=rpc-server))