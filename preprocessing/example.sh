#!/bin/bash

./resize.sh 027_1.tif 027_1.5.tif 50
./addtexture.sh 027_1.5.tif 027_1.w.jpg paperTexture.jpeg

./text_onto_rule_paper_with_bumpmap.sh 027_1.5.tif rule_lines1.gif text_ruled1.gif
./text_onto_tiled_rulelines_with_bumpmap.sh 027_1.5.tif rule_lines2.png text_ruled2.gif
./text_onto_grid_with_multiply.sh 027_1.5.tif isometric_graph_paper1.png text_ruled3.gif