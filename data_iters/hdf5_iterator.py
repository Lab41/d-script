import logging
import PIL
import h5py
import numpy as np
from collections import defaultdict
from minibatcher import MiniBatcher
from image_manip import sample_with_rotation, rescale_array

def zero_one(x, ceiling=255.):
    """ Scale a value to fall between 0 and 1,
    and reverse it. By default converts byte-valued variables
    (where 255 is absence) to float-valued ones where 0.0
    is absence"""
    
    try:
        transformed = 1. - float(x)/ceiling
    except TypeError:
        transformed = 1. - x.astype(np.float32)/ceiling
    return transformed
    
def nmec_pre(x, rng=None):
    # NMEC preaugmentation:
    # scale by 0.5
    x = rescale_array(x, 0.5)
    return x


class Hdf5MiniBatcher:
    """ Iterator interface for generating minibatches from 
    'author-fragment' style HDF5 sets of data
    """
    
    @staticmethod
    def shingle_item_getter(f, key, shingle_dim=(120,120), 
            fill_value=255, 
            rng=None,
            preprocess=None,
            add_rotation=False,
            stdev_threshold=None):

        '''
        Retrieve a line from an iam hdf5 file and shingle into the line
        NB: shingle_dim is in rows, cols format
        '''
        
        # maximum number of times to try and shingle from a document
        # before failing
        max_tries=30

        # Key format is {author:{form:data}}
        (author, form) = key
        # Extract fragment from HDF5 file
        original_fragment = f[author][form][()]
        
        if preprocess is not None:
            original_fragment = preprocess(original_fragment)

        # Pull shingle from the line, until it satisfies constraints
        for i in range(max_tries):
            (height, width) = original_fragment.shape
            shingle_height, shingle_width = shingle_dim

            x_sample = rng.randint(0, width)
            y_sample = rng.randint(0, height)
            
            if add_rotation:
                rotate_angle = rng.normal(0, 0.125)
            else:
                rotate_angle = 0
            try:
                test_stdev = stdev_threshold is not None
                output_arr=sample_with_rotation(original_fragment, (x_sample, y_sample), 
                                           rotate_angle,
                                           wraparound=False,
                                           stdev_threshold=stdev_threshold,
                                           test_stdev=test_stdev)
            except ValueError as e:
                logger=logging.getLogger(__name__)
                logger.debug('Sample SD too low?', exc_info=True)
                continue
            
            
            shingle_stdev=np.std(output_arr)
            logger=logging.getLogger(__name__)
            logger.debug(shingle_stdev)
            if stdev_threshold is None or shingle_stdev > stdev_threshold:
                break
        return output_arr

    def __init__(self, fname, 
                 num_authors, 
                 num_forms_per_author,
                 preprocess=None,
                 postprocess=zero_one, 
                 default_mode=MiniBatcher.TRAIN, 
                 shingle_dim=(120,120), 
                 batch_size=32, 
                 train_pct=.7, test_pct=.2, val_pct=.1, 
                 rng_seed=888, 
                 fill_value=255,
                 scale_factor=None,
                 stdev_threshold=None,
                 add_rotation=False):
        """
        Arguments
        fname -- path to HDF5 set
        num_authors -- number of authors to retrieve from HDF5 set
        num_forms_per_author -- number of fragments to retrieve per author
        preprocess -- function/callable to transform fragments before shingling (must be called in item_getter)
        postprocess -- function/callable to transform shingles
        default_mode -- which set (TRAIN, TEST, VAL) should MiniBatcher return by default?
        shingle_dim=(120,120) -- shingle size (rows, cols)
        batch_size
        train_pct, test_pct, val_pct -- data fold proportions
        rng_seed -- random number seed for item_getter's random number generator and MiniBatcher's (separate)
            random number generator
        fill_value -- what value counts as blank, in case padding needs to be carried out?
        scale_factor -- scale fragments by this much before shingling
        stdev_threshold -- yield only shingles above this standard deviation, in unnormalized units
        add_rotation -- boolean, randomly sample an angle (between -0.125 and 0.125 radians) to rotate shingles by?
        """
        
        self.rng = np.random.RandomState(rng_seed)
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

        # Remove duplicates to prevent test/val contamination
        keys = list(set(keys))

        item_getter = lambda f, key: Hdf5MiniBatcher.shingle_item_getter(f, key,
                                                                        shingle_dim=shingle_dim,
                                                                        fill_value=fill_value,
                                                                        rng=self.rng,
                                                                        preprocess=preprocess,
                                                                        stdev_threshold=stdev_threshold,
                                                                        add_rotation=add_rotation)
        
        self.batch_size = batch_size
        m = MiniBatcher(fIn, keys,item_getter=item_getter, postprocess=postprocess,
                        batch_size=self.batch_size, min_fragments=0, 
                        train_pct=train_pct, test_pct=test_pct, val_pct=val_pct,
                        rng_seed=rng_seed)
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

    iam_m = Hdf5MiniBatcher(options.filename, options.num_authors, options.num_forms_per_author,
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
