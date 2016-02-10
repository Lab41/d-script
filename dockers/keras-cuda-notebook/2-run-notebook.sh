#!/bin/bash

if [ $# -ne 2 ]; then
  echo "USAGE: 2-run-notebook.sh <local-directory> <python-port>"
  exit
fi

# image name
__image=lab41/keras-notebook:cudnn
__volume_host=$1
#__volume_host=$PWD
__volume_cntr=/work
__volume_data=/fileserver
__ipython_port=$2

# run image
docker run -it\
        --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm \
        --device /dev/nvidia0:/dev/nvidia0 \
        --volume=$__volume_host:$__volume_cntr \
        --volume=/data/fs4/datasets/:$__volume_data \
        --volume=/dev/shm:/memory \
        --publish=$__ipython_port:8888 \
        $__image /bootstrap.sh
