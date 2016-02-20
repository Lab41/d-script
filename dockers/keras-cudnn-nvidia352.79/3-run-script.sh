#!/bin/bash

if [ $# -lt 2 ]; then
  echo "USAGE: 2-run-notebook.sh <local-directory> <remote-command>"
  exit
fi

# image name
__image=lab41/cudnn-keras-notebook:352.79
__volume_host=$1
__volume_cntr=/work
__volume_data=/fileserver
__script_path=$(readlink -f $2)
__command=/opt/script
__command=$2

echo $__command
# run image
docker run -ti \
        --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm \
        --device /dev/nvidia0:/dev/nvidia0 \
        --volume=$__volume_host:$__volume_cntr \
        --volume=/data/fs4/datasets/:$__volume_data \
        --volume=/dev/shm:/memory \
        $__image /bin/bash -c "$__command"
