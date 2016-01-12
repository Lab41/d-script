#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: addtexture <image-name> <output-name> <texture>"
    exit
fi

convert $3 -colorspace gray -normalize \
	-fill gray50 +level 90% $3.gif
composite $3.gif $1 -tile -compose Hardlight $2
