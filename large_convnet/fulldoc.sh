#!/bin/bash

python fulldoc.py -f /memory/raw_lines_from_forms_uint8.hdf5 --num_authors 55 --num_forms_per_author 10 --shingle_dim 120,1200 --num_iters 500 # --from_form # --weights /work/models/authors_55_forms_per_author_10_epoch_2000.hdf5.hdf5


