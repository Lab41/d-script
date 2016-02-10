#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: resize.sh <image-name> <output-name> <scale>"
    exit
fi

convert $1 -resize $3% $2
