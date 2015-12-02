import glob
import h5py
import sys
import os

import scipy.misc
from utils import *

def process_file(input_path):
    pass
    # Read line
    # return

def process_folder(input_path, output_fname):
    '''
    Takes input data, normalizes lines and saves to hdf5 (assumes data is organized as input_path/author/form/line#.png)
    '''

    # Caculate which files we need to look at
    png_files = glob.glob(os.path.join(input_path, '*', '*', '*.png'))
    split_files = []
    for png_file in png_files:
        (path, line_name) = os.path.split(png_file)
        (path, form_name) = os.path.split(path)
        (path, author) = os.path.split(path)
        split_files.append((author, form_name, line_name, png_file))


    # Open Output File
    fOut = h5py.File(output_fname, 'w')

    seen_authors = {}
    seen_forms = {}
    num_items = len(split_files)
    count = 0
    for (author, form_name, line_name, full_path) in split_files:
        if author not in seen_authors:
            author_grp = fOut.create_group(author)
            seen_authors[author] = author_grp

        if form_name not in seen_forms:
            author_grp = seen_authors[author]
            form_grp = author_grp.create_group(form_name)
            seen_forms[form_name] = form_grp

        input_line = scipy.misc.imread(full_path)
        resized_data = normalize_line(input_line)
        form_grp.create_dataset(line_name, data=resized_data)
        count += 1

        if count %100 == 0:
            print 'Completed %d of %d'%(count, num_items)

    fOut.close()

def main():
    if len(sys.argv) != 2:
        print "Usage: python iam_lines_2_hdf5.py /path/to/line_pngs/ /path/to/output_fname.hdf5"
        sys.exit(1)

    input_directory = sys.argv[1]
    output_hdf5_fname = sys.argv[2]
    process_folder(input_directory, output_hdf5_fname)

if __name__ == "__main__":
    main()