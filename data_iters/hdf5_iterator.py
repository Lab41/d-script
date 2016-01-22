import logging
import PIL
import h5py
import numpy as np
from collections import defaultdict
from minibatcher import MiniBatcher

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

def rescale_array(x, scale_factor=0.25):
    logger = logging.getLogger(__name__)
    logger.debug(x.shape)
    img = PIL.Image.fromarray(x)
    new_w = int(x.shape[1] * scale_factor)
    new_h = int(x.shape[0] * scale_factor)
    img = img.resize((new_w,new_h),PIL.Image.NEAREST)
    x = np.array(img.getdata()).reshape(new_h, new_w)
    logger.debug(x.shape)
    return x
    
    
class Hdf5MiniBatcher:
    """ Iterator interface for generating minibatches from 
    'author-fragment' style HDF5 sets of data
    """
    
    @staticmethod
    def shingle_item_getter(f, key, shingle_dim=(120,120), 
            fill_value=255, 
            rng=None, 
            scale_factor=None,
            std_threshold=None):

        '''
        Retrieve a line from an iam hdf5 file and shingle into the line
        NB: shingle_dim is in rows, cols format
        '''

        # Key format is {author:{form:data}}
        (author, form) = key
        # Extract fragment from HDF5 file
        original_fragment = f[author][form]
        
        # Rescale if necessary
        if scale_factor is not None:
            original_fragment = rescale_array(original_fragment[()], scale_factor)

        # Pull shingle from the line, until it satisfies constraints
        while True:
            (height, width) = original_fragment.shape
            max_x = max(width - shingle_dim[1], 1)
            max_y = max(height - shingle_dim[0], 1)
            x_start = rng.randint(0, max_x)
            y_start = rng.randint(0, max_y)
            shingle_height, shingle_width = shingle_dim

            # check if the line is too small on at least one axis
            if width < shingle_width:
                x_slice = slice(0,width)
            else:
                x_slice = slice(x_start, x_start+shingle_width)
            if  height < shingle_height: 
                y_slice = slice(0,height)
            else:
                y_slice = slice(y_start, y_start+shingle_height)
            slice_width = x_slice.stop - x_slice.start
            slice_height = y_slice.stop - y_slice.start
            # create an output shingle, copy our thing onto it
            output_arr = np.zeros(shingle_dim)
            output_arr.fill(fill_value)
            output_arr[:slice_height,:slice_width] = original_fragment[y_slice, x_slice]
            shingle_std=np.std(output_arr)
            logger=logging.getLogger(__name__)
            logger.debug(shingle_std)
            if std_threshold is None or shingle_std > std_threshold:
                break
        return output_arr

    def __init__(self, fname, num_authors, num_forms_per_author, normalize=zero_one, default_mode=MiniBatcher.TRAIN, shingle_dim=(120,120), batch_size=32, train_pct=.7, test_pct=.2, val_pct=.1, rng_seed=888, fill_value=255,
                scale_factor=None,std_threshold=None):
        """
        Arguments
        fname -- path to HDF5 set
        num_authors -- number of authors to retrieve from HDF5 set
        num_forms_per_author -- number of fragments to retrieve per author
        normalize -- function/callable to normalize shingles in each fragment,
        default_mode -- which set (TRAIN, TEST, VAL) should MiniBatcher return by default?
        shingle_dim=(120,120) -- shingle size (rows, cols)
        batch_size
        train_pct, test_pct, val_pct -- data fold proportions
        rng_seed -- random number seed for item_getter's random number generator and MiniBatcher's (separate)
            random number generator
        fill_value -- what value counts as blank, in case padding needs to be carried out?
        scale_factor -- scale fragments by this much before shingling
        std_threshold -- yield only shingles above this standard deviation, in unnormalized units
        """
        
        self.rng = np.random.RandomState(rng_seed)
        logger = logging.getLogger(__name__)
        logger.debug(self.rng.rand())
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

        item_getter = lambda f, key: Hdf5MiniBatcher.shingle_item_getter(f, key,
                                                                         shingle_dim=(120, 120),
                                                                         fill_value=255,
                                                                         rng=self.rng,
                                                                         scale_factor=scale_factor,
                                                                         std_threshold=std_threshold)
        
        self.batch_size = batch_size
        m = MiniBatcher(fIn, keys,item_getter=item_getter, normalize=normalize,
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
