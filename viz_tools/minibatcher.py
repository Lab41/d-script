import random
import numpy as np
from collections import defaultdict

class MiniBatcher:
    TRAIN = 0
    TEST = 1
    VAL = 2
    def __init__(self, hdf5_file, input_keys, normalize=None, batch_size=32, min_shingles=20*8*15, train_pct=.7, test_pct=.2, val_pct=.1):
        self.mode = self.TRAIN
        self.fIn = hdf5_file
        self.batch_size = batch_size
        self.min_shingles = min_shingles

        self.normailize = normalize

        self.train_pct = train_pct
        self.test_pct = test_pct
        self.val_pct = val_pct

        random.seed(1024) # Repeatable

        # Unfortunately we have to iterate through a few times to make sure we do this right
        # First we get counts to make sure we exclude items without sufficient data
        top_level_counts = defaultdict(int)
        for i in range(len(input_keys)):
            top_level_key = input_keys[i][0][0]
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

        # Create training/test/validation
        self.train = []
        self.test = []
        self.val = []
        for i in range(len(input_keys)):
            top_level_key = input_keys[i][0][0]
            if top_level_key in self.name_2_id:
                num = random.random()
                if num < train_pct:
                    self.train.append(input_keys[i])
                elif num < train_pct + test_pct:
                    self.test.append(input_keys[i])
                else:
                    self.val.append(input_keys[i])

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
        batch_keys = random.sample(src_arr, self.batch_size)

        # Collect data
        batch_data = []
        #ids_in_batch = []
        batch_data = None
        ids_in_batch = np.zeros((self.batch_size))
        for i,key in enumerate(batch_keys):
            top_key = key[0][0]
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