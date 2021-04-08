#!/bin/bash
xhost +
docker run -it \
--rm \
--net=host \
--runtime nvidia \
-e DISPLAY=$DISPLAY \
--privileged \
gism-dev:v1.7
