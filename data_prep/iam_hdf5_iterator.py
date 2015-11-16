import h5py
import random
import numpy as np
from collections import defaultdict
from minibatcher import MiniBatcher

def main():
    import time
    from scipy.sparse import csr_matrix
    hdf5_file = 'output_shingles_sparse.hdf5'
    num_authors=40
    num_forms_per_author=15
    fIn = h5py.File(hdf5_file, 'r')
    authors = []

    # Filter on number of forms per author
    for author in fIn.keys():
        if len(fIn[author]) > num_forms_per_author:
            authors.append(author)

    if len(authors) < num_authors:
        raise ValueError("There are only %d authors with more than %d forms"%(len(authors), num_forms_per_author))


    keys = []
    # Get all the keys from our hdf5 file
    for author in authors[:num_authors]: # Limit us to num_authors
        forms = list(fIn[author])
        for form in forms[:num_forms_per_author]: # Limit us to num_form_per_author
            for line_name in fIn[author][form].keys():
                for shingle in range(fIn[author][form][line_name].shape[0]):
                    keys.append([(author,form,line_name), shingle])

    # Normalization function which scales values from 0 (white) to 1 (black)
    normalize = lambda x: 1.0 - x.astype(np.float32)/255.0

    m = MiniBatcher(fIn, keys,normalize=normalize, batch_size=32)
    num_batches = 1000#00
    start_time = time.time()
    for i in range(num_batches):
        z = m.get_batch()

    print 'Completed %d batches in: '%num_batches,time.time() - start_time

if __name__ == "__main__":
    main()