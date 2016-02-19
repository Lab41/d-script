#!/usr/bin/env bash

if [ $# -ne 3 ]; then
    echo "Usage: text_onto_rule_paper_with_bumpmap <text-image> <background-image> <output-name>"
    exit
fi

composite \( $1 -resize 50% \) $2 -compose bumpmap -gravity center $3