import sys
import logging
import time
import PIL
import h5py
import numpy as np
from collections import defaultdict
sys.path.append("..")
from minibatcher import MiniBatcher
from image_manip import sample_with_rotation, extract_with_box
from viz_tools.array_to_png import rescale_img_array


# possible pre/post-processing components ##########
def zero_one(x, ceiling=255., **kwargs):
    """ Scale a value to fall between 0 and 1,
    and reverse it. By default converts byte-valued variables
    (where 255 is absence) to float-valued ones where 0.0
    is absence"""
    
    try:
        transformed = 1. - float(x)/ceiling
    except TypeError:
        transformed = 1. - x.astype(np.float32)/ceiling
    return transformed
    
def nmec_pre(x, **kwargs):
    """NMEC preaugmentation: scales input by 0.5"""
    x = rescale_img_array(x, 0.5)
    
    return x

def noise_for_example(x, extent = 1000, intensity = 0.1, rng=None, **kwargs):
    """
    Add noise to x. Just for demonstration.
    
    Arguments:
    extent -- number of points to add noise at
    intensity -- scale parameter of half-normal distribution; samples
        from this distribution will be added at each noise location
    """
    
    x = x[:]
    orig_dtype = x.dtype
    noise_x = rng.uniform(0, x.shape[1], extent)
    noise_y = rng.uniform(0, x.shape[0], extent)
    noise_amount = np.abs(rng.normal(0, intensity, extent))
    for ns_x, ns_y, amount in zip(noise_x, noise_y, noise_amount):
        x[ns_y,ns_x] = x[ns_y,ns_x] + amount
 
    return x.astype(orig_dtype)

# Dataset iterator class
class Hdf5MiniBatcher:
    """ Iterator interface for generating minibatches from 
    'author-fragment' style HDF5 sets of data
    """
    
    @staticmethod
    def shingle_item_getter(f, key, shingle_dim=(120,120), 
            fill_value=255, 
            rng=None,
            preprocess=None,
            postprocess=None,
            add_rotation=False,
            stdev_threshold=None):

        '''
        Example item_getter implementation.
        Retrieves a fragment from an iam hdf5 file and shingles into it.
        
        Arguments:
        f -- hdf5 Group(/File) object. 
            Should have format f(File/Grp) > author(Grp) > fragment(Dataset)
        key -- 2-tuple, in form (author_id, fragment_id). Indexes into f.
        shingle_dim -- 2-tuple, in form (rows, cols), describing the size of the
            'shingle' (rectangular sample) to be drawn from the fragment
        fill_value -- quantity to be used to fill "empty" portions of shingle.
            filling (ought to) happen after preprocessing and before postprocessing.
        rng -- numpy RandomState object. All randomization is done from this object,
            to preserve replicability
        preprocess -- callable object, accepting at least a positional argument and kwargs;
            if not None, each fragment is dispatched to preprocess before any shingling.
            A RandomState object 'rng' may be in kwargs, if randomization is needed
        postprocess -- callable object, accepting at least a positional argument and kwargs;
            if not None, each fragment is dispatched to postprocessing just before being
            returned to the MiniBatcher.
            A RandomState object 'rng' may be in kwargs, if randomization is needed
        add_rotation -- boolean: rotate each shingle-sampling box randomly before extracting from
            a fragment? NB: rotation is currently done with slow python code using alaised linear filtering
        stdev_threshold -- if not None, try at most max_tries(=30) times to extract a shingle whose
            standard deviation before postprocessing exceeds this quantity, (implicitly) throwing
            NameError if a qualifying shingle cannot be found. Useful for returning potentially
            informative shingles
        '''
        
        # maximum number of times to try and shingle from a document
        # before failing
        max_tries=30
        logger = logging.getLogger(__name__)
        logger.debug("Shingle dim: {0}".format(shingle_dim))

        # Key format is {author:{form:data}}
        (author, fragment) = key
        # Extract fragment from HDF5 file
        t_alpha = time.clock()
        original_fragment = f[author][fragment][()]
        t_omega = time.clock()
        logger.debug("Getter time: {0}".format(t_omega-t_alpha))

        if preprocess is not None:
            original_fragment = preprocess(original_fragment, rng=rng)
            
        # Pull shingle from the line, until it satisfies constraints
        for i in range(max_tries):
            
            ## Pat and Karl are hacking!
            if not original_fragment.shape == 2:
                original_fragment = np.zeros((shingle_dim))
                
            (height, width) = original_fragment.shape
            shingle_height, shingle_width = shingle_dim

            width=max(width, 1)
            height=max(height,1)
            x_sample = rng.randint(0, width)
            y_sample = rng.randint(0, height)
            
            if add_rotation:
                rotate_angle = rng.normal(0, 0.125)
            else:
                rotate_angle = 0
     
            test_stdev = stdev_threshold is not None
            if rotate_angle != 0:
                output_arr=sample_with_rotation(original_fragment, center=(x_sample, y_sample), 
                                           angle=rotate_angle,
                                           box_dim=shingle_dim,
                                           wraparound=False,
                                           stdev_threshold=stdev_threshold,
                                           test_stdev=test_stdev,
                                           fill_value=fill_value)
                
                if output_arr is None:
                    continue
 
            else:
                logger=logging.getLogger(__name__)
                logger.debug("Using box")
                output_arr=extract_with_box(original_fragment, 
                                            center=(x_sample, y_sample), box_dim=shingle_dim, 
                                            fill_value=fill_value)
            
            
            shingle_stdev=np.std(output_arr)
            logger=logging.getLogger(__name__)
            logger.debug("Shingle SD: {0}".format(shingle_stdev))

            if stdev_threshold is None or shingle_stdev > stdev_threshold:
                break
            
        assert output_arr is not None
        
        if postprocess is not None:
            output_arr = postprocess(output_arr, rng=rng)

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
        preprocess -- function/callable to transform fragments before shingling (must be called in item_getter);
            must accept one argument and **kwargs
        postprocess -- function/callable to transform shingles; accepts one argument and **kwargs
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
                                                                        postprocess=postprocess,
                                                                        stdev_threshold=stdev_threshold,
                                                                        add_rotation=add_rotation)
        
        self.batch_size = batch_size
        m = MiniBatcher(fIn, keys,item_getter=item_getter,
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
        logger = logging.getLogger(__name__)
        logger.debug("Number of items to get: {0}".format(num_items))
        logger.debug("Minibatcher.TRAIN: {0}".format(MiniBatcher.TRAIN))
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
