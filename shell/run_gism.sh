#!/bin/bash
xhost +
docker run -it \
--rm \
--net=host \
--runtime nvidia \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix/:/tmp/.X11-unix \
-v appconfig:/app/appconfig \
-v video:/app/video \
--mount type=bind,source=/home/edit/app/gism/model,target=/app/custom_model \
--privileged \
gism:v2.0
