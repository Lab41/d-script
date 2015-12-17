import h5py
import random
import numpy as np
from collections import defaultdict
from minibatcher import MiniBatcher

class IAM_MiniBatcher:
    @staticmethod
    def shingle_item_getter(f, key, shingle_dim=(120,120), use_form=False):
        '''
        Retrieve a line from an iam hdf5 file and shingle into the line
        '''

        if use_form:
            # Key format is {author:{form:data}}
            #print key
            (author, form) = key
            # Extract line from HDF5 file
            original_line = f[author][form]
        else:
            # Key format is {author:{form:{line:data}}
            #print key
            (author, form, line) = key
            # Extract line from HDF5 file
            original_line = f[author][form][line]

        # Pull shingle from the line
        (height, width) = original_line.shape
        max_x = max(width - shingle_dim[1], 0)
        max_y = max(height - shingle_dim[0], 0)
        x_start = random.randint(0, max_x)
        y_start = random.randint(0, max_y)
        if width < shingle_dim[1] or height < shingle_dim[0]: # The line is too small in at least one access
            output_arr = np.zeros(shingle_dim)
            output_arr.fill(255)
            output_arr[:height,:width] = original_line[:min(height, shingle_dim[0]), :min(width, shingle_dim[1])]
            return output_arr
        else:
            return original_line[y_start:y_start+ shingle_dim[0], x_start:x_start+shingle_dim[1]]

    def __init__(self, fname, num_authors, num_forms_per_author, use_form=False, default_mode=MiniBatcher.TRAIN, shingle_dim=(120,120), batch_size=32):
        self.hdf5_file = fname

        fIn = h5py.File(self.hdf5_file, 'r')
        authors = []

        # Filter on number of forms per author
        for author in fIn.keys():
            if len(fIn[author]) >= num_forms_per_author:
                authors.append(author)

        if len(authors) < num_authors:
            raise ValueError("There are only %d authors with more than %d forms"%(len(authors), num_forms_per_author))


        keys = []
        # Get all the keys from our hdf5 file
        for author in authors[:num_authors]: # Limit us to num_authors
            forms = list(fIn[author])
            for form in forms[:num_forms_per_author]: # Limit us to num_form_per_author
                if use_form:
                    keys.append((author, form))
                else:
                    for line_name in fIn[author][form].keys():
                        for shingle in range(fIn[author][form][line_name].shape[0]):
                            keys.append((author,form,line_name))

        # Remove duplicates to prevent test/val contamination
        keys = list(set(keys))

        if use_form:
            expected_num_of_lines_per_form = 1
        else:
            expected_num_of_lines_per_form = 7

        normalize = lambda x: 1.0 - x.astype(np.float32)/255.0

        item_getter = lambda f, key: IAM_MiniBatcher.shingle_item_getter(f, key, shingle_dim, use_form)
        self.batch_size = batch_size
        m = MiniBatcher(fIn, keys,item_getter=item_getter, normalize=normalize,
                        batch_size=self.batch_size, min_shingles=expected_num_of_lines_per_form*num_forms_per_author)
        self.m = m
        self.default_mode = default_mode

    def get_test_batch(self, num_items=None):
        if num_items is None:
            num_items = self.batch_size
        return self.get_batch(num_items, MiniBatcher.TEST)

    def get_train_batch(self, num_items=None):
        if num_items is None:
            num_items = self.batch_size
        return self.get_batch(num_items, MiniBatcher.TRAIN)

    def get_val_batch(self, num_items=None):
        if num_items is None:
            num_items = self.batch_size
        return self.get_batch(num_items, MiniBatcher.VAL)

    def get_batch(self, num_items, mode=None):
        if mode is None:
            mode = self.default_mode
        self.m.set_mode(mode)
        self.m.batch_size = num_items
        return self.m.get_batch()


def main():
    import time
    import sys
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Log file to read")
    parser.add_option("--num_authors", dest='num_authors', type=int, help="Number of authors to include")
    parser.add_option("--num_forms_per_author", dest='num_forms_per_author',
                      type=int, help="Number of forms per author required")
    parser.add_option("--shingle_dim", dest='shingle_dim', help="Shingle dimensions, comma separated i.e. 120,120")
    parser.add_option("--batch_size", dest="batch_size", type=int, default=32, help="Iteration Batch Size")
    parser.add_option("--from_form", dest="use_form", action='store_true', default=False)
    (options, args) = parser.parse_args()

    shingle_dim = map(int, options.shingle_dim.split(','))

    iam_m = IAM_MiniBatcher(options.filename, options.num_authors, options.num_forms_per_author,
                            shingle_dim=shingle_dim, use_form=options.use_form,
                            default_mode=MiniBatcher.TRAIN, batch_size=options.batch_size)

    num_batches = 10
    start_time = time.time()
    for i in range(num_batches):
        z = iam_m.get_train_batch()

    print 'Completed %d batches in: '%num_batches,time.time() - start_time
    print z[0].shape
if __name__ == "__main__":
    main()