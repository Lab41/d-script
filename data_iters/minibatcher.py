import logging
import numpy as np
from collections import defaultdict

class MiniBatcher:
    TRAIN = 0
    TEST = 1
    VAL = 2
    def __init__(self, hdf5_file, input_keys, item_getter=None, normalize=None,
                 batch_size=32, min_shingles=10, 
                 train_pct=.7, test_pct=.2, val_pct=.1, rng_seed=888):
        """
        Set up MiniBatcher with replicable train/test/validation
        splitting functionality.

        Arguments:
            hdf5_file -- h5py File object, pointing to your data
            input_keys -- list of 2-tuples, providing 
                author/group id and form/document id
            item_getter -- function object taking two arguments,
                an object supporting indexing and the index used
                to index into it. Should return the item in the 
                first argument referred to by the second argument
            normalize -- Can be None; if not, a 1-argument function object
                which will called on every item in the dataset 
            batch_size -- mini-batch size
            min_shingles -- for each author/grouping factor, what is
                the minimum number of documents required to be included
                (TODO: change name?)
            train_pct, test_pct, val_pct -- what fractions of data are to be
                assigned to data subsets?
            rng_seed -- random number generator seed
        """
        self.mode = self.TRAIN
        self.fIn = hdf5_file
        self.batch_size = batch_size
        self.min_shingles = min_shingles

        self.normailize = normalize

        self.train_pct = train_pct
        self.test_pct = test_pct
        self.val_pct = val_pct

        np.random.seed(rng_seed)
        logger = logging.getLogger(__name__)

        # Unfortunately we have to iterate through a few times to make sure we do this right
        # First we get counts to make sure we exclude items without sufficient data
        top_level_counts = defaultdict(int)
        for i in range(len(input_keys)):
            top_level_key = input_keys[i][0]
            top_level_counts[top_level_key] += 1

        # Then we calculate mappings for items with a sufficient number of shingles
        self.name_2_id = {}
        id_num = 0
        # Assume top level of dictionary specifies groups
        for (id_str, id_count) in top_level_counts.items():
            if id_count >= min_shingles:
                self.name_2_id[id_str] = id_num
                id_num += 1
            else:
                print id_str, id_count, min_shingles

        # # TODO: remove this hack, this is
        # print 'Num Input Keys:', len(input_keys)
        # keys_wo_shingles = set()
        # for key in input_keys:
        #     #print key[0]
        #     keys_wo_shingles.add(key[0])
        # keys_wo_shingles = list(keys_wo_shingles)
        # print 'Num Keys wo shingles (forms):', len(keys_wo_shingles)


        if item_getter:
            self.item_getter = item_getter
        else:
            key_depth = len(input_keys[0][0])
            print 'Key Depth: ', key_depth
            print 'Sample Key:', input_keys[0][0]
            if key_depth == 1:
                self.item_getter = lambda x, (l1, i): x[l1][i]
            elif key_depth == 2:
                self.item_getter = lambda x, ((l1,l2),i): x[l1][l2][i]
            elif key_depth == 3:
                self.item_getter = lambda x, ((l1,l2,l3),i): x[l1][l2][l3][i]
            else:
                raise NotImplementedError("Key depth of %d not supported"%key_depth)

        #print keys_wo_shingles[:10]
        # Create training/test/validation
        self.train = []
        self.test = []
        self.val = []
        # maintain references to all three sets, at least locally
        # TODO: consider using only list-of-lists for subsets, to avoid code duplication?
        all_subsets = [self.train, self.test, self.val]
        # loop over authors, dispatch individual "forms" (/lines) 
        # into train/test/val, appropriately
        authors_in_set = set([ input_keys[i][0] for i in range(len(input_keys)) if input_keys[i][0] in self.name_2_id])
        authors_forms_keys = tuples_to_dict(input_keys) 
        # delete authors who don't meet criteria
        for key in authors_forms_keys:
            if key not in authors_in_set:
                del authors_forms_keys[key]
        # loop over authors, shuffle associated form keys, and divide into train/test/val
        for author_key in authors_forms_keys:
            author_form_list = [ (author_key, form_key) for form_key in authors_forms_keys[author_key] ]
            np.random.shuffle(author_form_list)
            # build list of cutoffs for list of (shuffled) keys
            num_forms = len(author_form_list)
            probability_thresholds = [ train_pct, train_pct + test_pct, train_pct + test_pct + val_pct ] 
            subset_cutoffs = [0] + [ int(np.round(p * num_forms)) for p in probability_thresholds ]
            # divide into subsets
            subset_indices = [ subset_cutoffs[i:i+2] for i in range(len(subset_cutoffs) - 1) ]
            for set_i, (set_start, set_end) in enumerate(subset_indices):
                if set_end-set_start == 0:
                    logger.warning("Set {0} being assigned zero documents for author {1},"
                                   " maybe increase minimum docs per author?".format(
                                    set_i, author_key))
                # assign to appropriate subset
                all_subsets[set_i].extend(author_form_list[set_start:set_end])
                    
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

            if self.normailize:
                data = self.normailize(data)

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
