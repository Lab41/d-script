import logging
import h5py
import numpy as np
from collections import defaultdict
from oldbatcher import MiniBatcher

class IAM_MiniBatcher:
    @staticmethod
    def shingle_item_getter(f, key, shingle_dim=(120,120)):

        '''
        Retrieve a line from an iam hdf5 file and shingle into the line
        NB: shingle_dim is in rows, cols format
        '''

        # Key format is {author:{form:data}}
        (author, form) = key
        # Extract line from HDF5 file
        original_line = f[author][form]
        # There was an option to index into form. That
        # format is deprecated. It originally had a hierarchy
        #      Key format is {author:{form:{line:data}}
        # and the code was:
        #      (author, form, line) = key
        #      original_line = f[author][form][line]

        # Pull shingle from the line
        # TODO: pull out shingle_dim[n] into two holder variables
        (height, width) = original_line.shape
        max_x = max(width - shingle_dim[1], 1)
        max_y = max(height - shingle_dim[0], 1)
        x_start = np.random.randint(0, max_x)
        y_start = np.random.randint(0, max_y)
        # check if the line is too small on at least one axis
        if width < shingle_dim[1]:
            x_slice = slice(0,width)
        else:
            x_slice = slice(x_start, x_start+shingle_dim[1])
        if  height < shingle_dim[0]: 
            y_slice = slice(0,height)
        else:
            y_slice = slice(y_start, y_start+shingle_dim[1])
        slice_width = x_slice.stop - x_slice.start
        slice_height = y_slice.stop - y_slice.start
        # create an output shingle, copy our thing onto it
        output_arr = np.zeros(shingle_dim)
        output_arr.fill(255)
        output_arr[:slice_height,:slice_width] = original_line[y_slice, x_slice]
        return output_arr

    def __init__(self, fname, num_authors, num_forms_per_author, default_mode=MiniBatcher.TRAIN, shingle_dim=(120,120), batch_size=32, train_pct=.7, test_pct=.2, val_pct=.1):
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
                keys.append((author, form))
                # Original hierarchy with "use_form" option:
                # for line_name in fIn[author][form].keys():
                #     for shingle in range(fIn[author][form][line_name].shape[0]):
                #         keys.append((author,form,line_name))

        # Remove duplicates to prevent test/val contamination
        keys = list(set(keys))

        normalize = lambda x: 1.0 - x.astype(np.float32)/255.0

        item_getter = lambda f, key: IAM_MiniBatcher.shingle_item_getter(f, key, shingle_dim)
        self.batch_size = batch_size
        m = MiniBatcher(fIn, keys,item_getter=item_getter, batch_size=self.batch_size, min_fragments=0, 
                        train_pct=train_pct, test_pct=test_pct, val_pct=val_pct)
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
    parser.add_option("--log_level", dest="log_level", type=int, default=logging.WARNING)
    (options, args) = parser.parse_args()

    logging.basicConfig(level=options.log_level)
    shingle_dim = map(int, options.shingle_dim.split(','))

    iam_m = IAM_MiniBatcher(options.filename, options.num_authors, options.num_forms_per_author,
                            shingle_dim=shingle_dim, default_mode=MiniBatcher.TRAIN,
                            batch_size=options.batch_size)

    num_batches = 10
    start_time = time.time()
    for i in range(num_batches):
        z = iam_m.get_train_batch()

    print 'Completed %d batches in: '%num_batches,time.time() - start_time
    print 'Batch shape: ', z[0].shape
    print 'Number of unique authors in first batch: {}'.format(len(set(z[1])))
if __name__ == "__main__":
    main()

