#!/bin/bash
xhost +
docker run -it \
--rm \
--net=host \
--runtime nvidia \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix/:/tmp/.X11-unix \
-v appconfig:/root/app/appconfig \
-v video:/root/app/video \
--mount type=bind,src=/home/edit/app/gism/model,target=/root/app/custom_model \
--privileged \
-w /root/app -v . \
gism-dev-jp441:v2.0.6 \
sh -c "ls" \
/bin/bash /root/rebuild.sh
