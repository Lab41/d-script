#!/usr/bin/env bash

if [ $# -ne 3 ]; then
    echo "Usage: text_onto_grid_with_multiply <text-image> <background-image> <output-name>"
    exit
fi

composite -compose multiply -geometry +50+400 \( $1 -resize 50% \) $2 $3