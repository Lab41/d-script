import glob
import h5py
import sys
import os
from collections import defaultdict, namedtuple
import numpy as np
import scipy.misc

from utils import *

bbox = namedtuple('bbox', ['min_x', 'min_y', 'max_x', 'max_y'])

def get_form_info(fname):
    line_info = defaultdict(list)
    for line in open(fname):
        if not line.startswith('#'):
            ls = line.strip().split()
            line_name = ls[0].split('-')
            line_info['-'.join(line_name[:2])].append(ls)

    X = 4
    Y = 5
    W = 6
    H = 7
    form_info = {}
    for form in line_info:
        max_x = None
        min_x = None
        max_y = None
        min_y = None
        for line in line_info[form]:
            #print line
            #print line[X], line[Y], line[W], line[H]
            #raise
            x = int(line[X])
            y = int(line[Y])
            w = int(line[W])
            h = int(line[H])
            if max_x is None or x + w > max_x:
                max_x = x + w
            if min_x is None or x < min_x:
                min_x = x
            if max_y is None or y  + h> max_y:
                max_y = y + h
            if min_y is None or y < min_y:
                min_y = y
        form_info[form] = bbox(min_x, min_y, max_x, max_y)
    return form_info


def process_folder(input_path, output_fname, form_info):
    '''
    Takes input data, normalizes lines and saves to hdf5 (assumes data is organized as input_path/author/form/line#.png)
    '''

    # Caculate which files we need to look at
    png_files = glob.glob(os.path.join(input_path, '*.png'))
    split_files = []
    for png_file in png_files:
        form_name = os.path.basename(png_file).split('.')[0]
        author = form_name.split('-')[0]
        split_files.append((author, form_name, png_file))

    # Open Output File
    fOut = h5py.File(output_fname, 'w')

    seen_authors = {}
    num_items = len(split_files)
    count = 0
    for (author, form_name, full_path) in split_files:
        text_bbow = form_info[form_name]
        if author not in seen_authors:
            author_grp = fOut.create_group(author)
            seen_authors[author] = author_grp

        #if form_name not in seen_forms:
        author_grp = seen_authors[author]

        input_line = scipy.misc.imread(full_path)
        resized_data = input_line[text_bbow.min_y:text_bbow.max_y, text_bbow.min_x:text_bbow.max_x]
        author_grp.create_dataset(form_name, data=resized_data.astype(np.uint8))
        count += 1

        if count %100 == 0:
            print 'Completed %d of %d'%(count, num_items)

    fOut.close()

def main():
    if len(sys.argv) != 4:
        print "Usage: python iam_forms_2_hdf5.py lines.txt /path/to/line_pngs/ /path/to/output_fname.hdf5"
        sys.exit(1)

    line_fname = sys.argv[1]
    input_directory = sys.argv[2]
    output_hdf5_fname = sys.argv[3]
    form_info = get_form_info(line_fname)
    process_folder(input_directory, output_hdf5_fname, form_info)

if __name__ == "__main__":
    main()