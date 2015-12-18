import glob
import h5py
import sys
import os
import gzip
from collections import defaultdict, namedtuple
import numpy as np
import scipy.misc

from utils import *

bbox = namedtuple('bbox', ['min_x', 'min_y', 'max_x', 'max_y'])

def get_form_info(fname):
    form_to_author = {}
    if fname.endswith('.gz'):
        fIn = gzip.open(fname)
    else:
        fIn = open(fname)
    line_info = defaultdict(list)
    for line in fIn:
        if not line.startswith('#'):
            ls = line.strip().split()
            line_name = ls[0].split('-')
            form_to_author[from_name] = ls[1]
            form_name = '-'.join(line_name[:2])
            line_info[form_name].append(ls)

    X = 4
    Y = 5
    W = 6
    H = 7
    form_info = defaultdict(list)
    for form in line_info:
        for line in line_info[form]:
            x = int(line[X])
            y = int(line[Y])
            w = int(line[W])
            h = int(line[H])
            form_info[form].append(bbox(x, y, x+w, y+h))
    return form_to_author, form_info


def process_folder(input_path, output_fname, form_to_author, form_info):
    '''
    Takes input data, normalizes lines and saves to hdf5 (assumes data is organized as input_path/author/form/line#.png)
    '''

    # Caculate which files we need to look at
    png_files = glob.glob(os.path.join(input_path, '*.png'))
    split_files = []
    for png_file in png_files:
        form_name = os.path.basename(png_file).split('.')[0]
        # author = form_name.split('-')[1]
        # a1 = author
        # if author.find('.') != -1:
        #     # Strip off extension
        #     author = author[: author.find('.') ]
        # while not author[-1].isdigit() and len(author) > 0:
        #     author = author[:-1]
        author = form_to_author[form_name]
        split_files.append((author, form_name, png_file))

    # Open Output File
    fOut = h5py.File(output_fname, 'w')
    seen_authors = {}
    num_items = len(split_files)
    count = 0
    for (author, form_name, full_path) in split_files:
        if author not in seen_authors:
            author_grp = fOut.create_group(author)
            seen_authors[author] = author_grp

        author_grp = seen_authors[author]
        form_grp = author_grp.create_group(form_name)

        input_line = scipy.misc.imread(full_path)
        for i,line_bbox in enumerate(form_info[form_name]):
            data_line = input_line[line_bbox.min_y:line_bbox.max_y, line_bbox.min_x:line_bbox.max_x]
            resized_line = normalize_line(data_line)
            line_name = '%s-%d.png'%(form_name, i)
            form_grp.create_dataset(line_name, data=resized_line.astype(np.uint8))

        count += 1

        if count %10 == 0:
            print 'Completed %d of %d'%(count, num_items)

    fOut.close()

def main():
    if len(sys.argv) != 4:
        print "Usage: python iam_forms_2_hdf5.py lines.txt /path/to/line_pngs/ /path/to/output_fname.hdf5"
        sys.exit(1)

    line_fname = sys.argv[1]
    input_directory = sys.argv[2]
    output_hdf5_fname = sys.argv[3]
    form_to_author, form_info = get_form_info(line_fname)
    process_folder(input_directory, output_hdf5_fname, form_to_author, form_info)

if __name__ == "__main__":
    main()