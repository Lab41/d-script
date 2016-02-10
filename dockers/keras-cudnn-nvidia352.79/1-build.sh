#!/bin/bash
set -e

# image name
__image=lab41/cudnn-keras-notebook
__tag=352.79
__dockerfile=Dockerfile

cp $FSERVER/users/pcallier/cudnn-7.0-linux-x64-v4.0-rc.tgz .

# build image
echo "Building $__image:$__tag"
docker build -f $__dockerfile -t $__image:$__tag .

rm cudnn-7.0-linux-x64-v4.0-rc.tgz
