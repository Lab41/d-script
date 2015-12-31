import logging
import numpy as np
from collections import defaultdict

class MiniBatcher:
    TRAIN = 0
    TEST = 1
    VAL = 2
    def __init__(self, hdf5_file, input_keys, item_getter, normalize=None,
                 batch_size=32, min_fragments=3, 
                 train_pct=.7, test_pct=.2, val_pct=.1, rng_seed=888):
        """
        Set up MiniBatcher with replicable train/test/validation
        splitting functionality.

        Arguments:
            hdf5_file -- h5py File object, pointing to your data
            input_keys -- list of 2-tuples, providing 
                author id and fragment (form, line, word,etc.) id 
            item_getter -- function object taking two arguments,
                an object supporting indexing and the index used
                to index into it. Should return the item in the 
                first argument referred to by the second argument
            normalize -- Can be None; if not, a 1-argument function object
                which will called on every item in the dataset 
            batch_size -- mini-batch size
            min_fragments -- for each author, what is
                the minimum number of fragments required to be included?
            train_pct, test_pct, val_pct -- what fractions of data are to be
                assigned to data subsets?
            rng_seed -- random number generator seed
        """
        self.mode = self.TRAIN
        self.fIn = hdf5_file
        self.batch_size = batch_size
        self.min_fragments = min_fragments

        self.normalize = normalize

        if round(1e6*(train_pct + test_pct + val_pct))!= 1e6:
            raise ValueError('Train(%f)+ Test(%f) + Validation(%f) set percentatages must add to 1.0' %(train_pct,test_pct,val_pct))
        self.train_pct = train_pct
        self.test_pct = test_pct
        self.val_pct = val_pct

        np.random.seed(rng_seed)
        logger = logging.getLogger(__name__)

        # Unfortunately we have to iterate through a few times to make sure we do this right
        # First we get counts to make sure we exclude items without sufficient data
        author_counts = defaultdict(int)
        for i in range(len(input_keys)):
            author_key = input_keys[i][0]
            author_counts[author_key] += 1

        # Then we calculate mappings for items with a sufficient number of available fragments
        self.name_2_id = {}
        id_num = 0
        # Assume top level of dictionary specifies groups
        for (id_str, id_count) in author_counts.items():
            if id_count >= min_fragments:
                self.name_2_id[id_str] = id_num
                id_num += 1
            else:
                logger.debug("Skipped author {0}, with {1} fragments (min_fragments={2})".format(id_str, id_count, min_fragments))

        self.item_getter = item_getter

        # Create training/test/validation
        self.train = []
        self.test = []
        self.val = []
        # maintain references to all three sets, at least locally
        # TODO: consider using only list-of-lists for subsets, to avoid code duplication?
        all_subsets = [self.train, self.test, self.val]
        # loop over authors, dispatch individual fragments 
        # into train/test/val, appropriately
        authors_in_set = set([ input_keys[i][0] for i in range(len(input_keys)) if input_keys[i][0] in self.name_2_id])
        authors_fragments_keys = tuples_to_dict(input_keys) 
        # loop over authors, shuffle associated fragment keys, and divide into train/test/val
        for author_key in authors_fragments_keys:
            if author_key not in authors_in_set:
                continue
            author_fragment_list = [ (author_key, fragment_key) for fragment_key in authors_fragments_keys[author_key] ]
            np.random.shuffle(author_fragment_list)
            # build list of cutoffs for list of (shuffled) keys
            num_fragments = len(author_fragment_list)
            probability_thresholds = [ train_pct, train_pct + test_pct, train_pct + test_pct + val_pct ] 
            subset_cutoffs = [0] + [ int(np.round(p * num_fragments)) for p in probability_thresholds ]
            # divide into subsets
            subset_indices = [ subset_cutoffs[i:i+2] for i in range(len(subset_cutoffs) - 1) ]
            for set_i, (set_start, set_end) in enumerate(subset_indices):
                if set_end-set_start == 0:
                    logger.warning("Set {0} being assigned zero documents for author {1},"
                                   " maybe increase minimum docs per author?".format(
                                    set_i, author_key))
                # assign to appropriate subset
                all_subsets[set_i].extend(author_fragment_list[set_start:set_end])
                    
    def set_mode(self, mode):
        if mode not in set([self.TRAIN, self.TEST, self.VAL]):
            raise ValueError('Invalid mode specified (%s)'%(str(mode)))

        self.mode = mode
    def get_batch(self):
        # Pull batch from correct set
        if self.mode == self.TRAIN:
            src_arr = self.train
        elif self.mode == self.TEST:
            src_arr = self.test
        elif self.mode == self.VAL:
            src_arr = self.val

        # Randomize batch
        batch_keys = []
        randints = np.random.randint(0, len(src_arr), self.batch_size)
        for i in range(self.batch_size):
            ind = randints[i]
            try:
                batch_keys.append(src_arr[ind])
            except:
                print len(src_arr), type(src_arr), ind
                raise
        #batch_keys = random.sample(src_arr, self.batch_size)

        # Collect data
        batch_data = []
        #ids_in_batch = []
        batch_data = None
        ids_in_batch = np.zeros((self.batch_size))
        for i,key in enumerate(batch_keys):
            top_key = key[0]
            top_ind = self.name_2_id[top_key]

            data = self.item_getter(self.fIn, key)

            if self.normalize:
                data = self.normalize(data)

            if batch_data is None:
                data_shape = data.shape
                batch_data = np.zeros((self.batch_size, data_shape[0], data_shape[1]))
            ids_in_batch[i] = top_ind
            batch_data[i,:,:] = data

        # Return randomized batch
        return (batch_data, ids_in_batch)

def tuples_to_dict(pairs):
    d = {}
    for key, val in pairs:
        d.setdefault(key, []).append(val)
    return d
