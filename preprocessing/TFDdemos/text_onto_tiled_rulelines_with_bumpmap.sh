#!/usr/bin/env bash

if [ $# -ne 3 ]; then
    echo "Usage: text_onto_tiled_rulelines_with_bumpmap <text-image> <background-image> <output-name>"
    exit
fi

composite -compose bumpmap -tile $2 $1 $3