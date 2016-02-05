#!/bin/bash
set -e

# image name
__image=lab41/keras-notebook
__tag=cudnn

# build image
echo "Building $__image:$tag"
docker build --no-cache -t $__image:$__tag .

