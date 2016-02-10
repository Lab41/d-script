#!/bin/bash
set -e

# image name
__image=lab41/cudnn-keras-notebook
__tag=352.79
__dockerfile=Dockerfile

# build image
echo "Building $__image:$__tag"
docker build -f $__dockerfile -t $__image:$__tag .

