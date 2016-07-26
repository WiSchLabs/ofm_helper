#!/usr/bin/env bash
set -e
REGISTRY="wischlabs"
BASE_IMAGE="ofm_helper"
IMAGE="$REGISTRY/$BASE_IMAGE"
CID=$(docker ps | grep $BASE_IMAGE | awk '{print $1}')
docker pull $IMAGE

for im in $CID
do
    LATEST=`docker inspect --format "{{.Id}}" $IMAGE`
    RUNNING=`docker inspect --format "{{.Image}}" $im`
    NAME=`docker inspect --format '{{.Name}}' $im | sed "s/\///g"`
    echo "Latest:" $LATEST
    echo "Running:" $RUNNING
    if [ "$RUNNING" != "$LATEST" ];then
        echo "upgrading $NAME"
        docker stop $NAME
        docker rm -f $NAME
        docker run -d --name ofm_helper --volumes-from dbstore --restart=unless-stopped wischlabs/ofm_helper
    else
        echo "$NAME up to date"
    fi
done