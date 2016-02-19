import sys
import logging
import time
import random
import numpy as np
from collections import defaultdict, namedtuple
from optparse import OptionParser

import h5py
import fielutil

class StepShingler:
    
    ShingleSize=namedtuple('ShingleSize', ['rows','cols'])
    
    def __init__(self, img, 
                 hstep, vstep, 
                 shingle_size=ShingleSize(rows=120,cols=120),
                 fill_value=255):
        """ given an image of a document fragment, 
        produce deterministic shingles from that document
        
        Arguments:
            img -- array (numpy array interface)
            hstep -- number of columns to step between shingles
            vstep -- number of rows to step between shingles
            shingle_size -- ROWS, COLS format.
        """
        self.img = img
        self.shingle_size = StepShingler.ShingleSize(*shingle_size)
        self.vstep = vstep
        self.hstep = hstep
        
        # warn if danger of leaving off right or bottom edge
        h_step_space = img.shape[1] - self.shingle_size.cols
        # number of pixels left over on right edge
        h_step_margin = h_step_space % hstep
        if h_step_margin != 0:
            # fill horizontal margin with fill_value
            fill_block = np.empty((img.shape[0], h_step_margin))
            fill_block.fill(fill_value)
            img = np.concatenate((img, fill_block), axis=1)
        v_step_space = img.shape[0] - self.shingle_size.rows
        # number of pixels left over on bottom edge
        v_step_margin = v_step_space % vstep
        if v_step_margin != 0:
            # fill vertical margin with fill_value
            fill_block = np.empty((v_step_margin,img.shape[1]))
            fill_block.fill(fill_value)
            img = np.concatenate((img, fill_block), axis=0)
            
    def __iter__(self):
        for row_i in xrange(0, self.img.shape[0] - self.shingle_size[0], self.vstep):
            for col_j in xrange(0, self.img.shape[1] - self.shingle_size[1], self.hstep):
                logger = logging.getLogger(__name__)
                #logger.info("Row {0}, Col {1}".format(row_i, col_j))
                end_col = col_j + self.shingle_size[1]
                end_row = row_i + self.shingle_size[0]
                yield self.img[row_i:end_row, col_j:end_col]
                

def zero_one(x):
    """ Normalize byte-sized integer to 0-1 and flip it so 255 (white)
    maps to 0.0
    """
    x = 1. - (x/255.)
    return x
                
def shingles_4_inference(authors_fragments_set, hstep=90, vstep=90,
                         shingle_size=StepShingler.ShingleSize(rows=120, cols=120),
                         var_threshold=None, postprocess=zero_one,
                         verbose=False):
    """ Given a dictionary-like object (e.g. HDF5 Groups, etc.) of
    author-keyed fragments, iterate over individual authors, fragments,
    and yield pairs of shingle (using deterministic step shingling) and author id.
    
    Arguments:
        authors_fragments_set -- dictionary-like object
        hstep -- horizontal step size in pixels/cols
        vstep -- vertical step size in pixels/rows
        shingle_size -- (rows, cols) tuple indicating size of shingle
            StepShingler.ShingleSize provides a useful namedtuple to avoid 
            parameter order confusion
        var_threshold -- float or None; if given, do not yield any shingle whose
            variance falls below this quantity
        verbose -- if True, will warn on fragments where there are unshingled pixels at the right
            or bottom edge
    """
    
    try:
        if verbose:
            old_level = logging.getLogger(__name__).getEffectiveLevel()
            logging.getLogger(__name__).setLevel(logging.INFO)
        for author_key in authors_fragments_set:
            logger=logging.getLogger(__name__); logger.info("Author: {0}".format(author_key))
            author_fragments = authors_fragments_set[author_key]
            for fragment_key in author_fragments:
                fragment = author_fragments[fragment_key]
                logger.info("Fragment shape: {0}".format(fragment.shape))
                shingle_iterator = StepShingler(fragment, hstep, vstep, shingle_size)
                for shingle in shingle_iterator:
                    if postprocess is not None:
                        shingle=postprocess(shingle)
                    if var_threshold is not None:
                        shingle_var = np.var(shingle)
                        if shingle_var < var_threshold:
                            continue
                    yield shingle, author_key, fragment_key
    finally:
        if verbose:
            logging.getLogger(__name__).setLevel(old_level)

class ICDARFeaturizer:
    """
    Easy interface for featurizing documents in ICDAR13
    """
    def __init__(self, icdar_hdf5_path, fiel_weights):
        """ hdf5_path -- path to docid-only ICDAR13 set"""
        self.fielnet = fielutil.tfdnet(fiel_weights, layer='fc7')
        # vacuous compile, will not be trained
        self.fielnet.compile(optimizer='sgd', loss='mse')
        self.icdar_hdf5_path = icdar_hdf5_path
        
    def fielify_img(self, img):
        fiel_features = self.fielnet.predict(img)
        return fiel_features

    def fielify_doc_by_id(self, doc_id, hstep=120, vstep=120, return_mean=False, stdev_threshold=None, num_shingles=None):
        """ Get Fiel features for a document
        
        Arguments:
            doc_id -- document ID (e.g. '002_3.tif')
            hstep, vstep -- horizontal and vertical stride between shingles
            return_mean -- Return features for all features (False) or do
                mean aggregation?
            stdev_threshold -- shingle must have stdev > this to be counted, if not None
            num_shingles -- if not None, sort shingles by variance and extract features
                only from this many. If fewer than num_shingles shingles are available in a document,
                ValueError is raised.
        """
        with h5py.File(self.icdar_hdf5_path, "r") as icdar_hdf5:
            img = icdar_hdf5[doc_id]
            # Get shingle generator
            shingler = StepShingler(img, hstep=hstep, vstep=vstep)
            all_features = []
            for shingle in shingler:
                shingle = np.expand_dims(np.expand_dims(shingle, 0),0)
                # normalize
                shingle = zero_one(shingle)
                # skip if threshold not satisfied
                if stdev_threshold is not None and np.std(shingle) < stdev_threshold:
                    continue
                # extract features
                fiel_features=self.fielify_img(shingle)
                all_features.append(fiel_features)
            all_features = np.array(all_features)
            # handle conditions involving shingle quantity
            if num_shingles is not None and all_features.shape[0] < num_shingles:
                raise ValueError("Not enough shingles in document")
            if num_shingles is not None and all_features.shape[0] > num_shingles:
                # sort shingles by variance and pick the top few
                all_features = np.array(all_features)
                variances = np.var(all_features, axis=(1,2))
                variance_rankings = np.argsort(-variances)
                all_features = all_features[variance_rankings[:num_shingles], :]
                
                assert(all_features.shape[0] == num_shingles, 
                    "Wanted {0} shingles, got {1}.\n{2}".format(num_shingles,
                                                                all_features.shape[0],
                                                                variance_rankings[:30]))
            # do mean aggregation if required    
            if return_mean:
                all_features=np.mean(all_features, axis=0)
            return all_features


def get_icdar_features(features_hdf5_path, 
                       icdar_docsonly_hdf5_path, icdar_authors_docs_hdf5_path,
                       fielnet_weights_path="../convnets/fielnet/fielnet.hdf5",
                       **kwargs):
    """
    Get Fiel features for ICDAR13. Requires both author-document and documents-only
    HDF5 files for the set.
    
    Arguments:
        features_hdf5_path -- save results to an HDF5 file at this path
        icdar_docsonly_hdf5_path -- path to documents-only ICDAR13 HDF5 set
        icdar_authors_docs_hdf5_path -- path to authors+docs ICDAR13 HDF5 set
        fielnet_weights_path -- path to HDF5 set of saved weights for Fiel-style convnet
        kwargs -- arguments to be passed along to ICDARFeaturizer.fielify_doc_by_id for each
            document in ICDAR13
    """
    ic_feat = ICDARFeaturizer(icdar_docsonly_hdf5_path,fielnet_weights_path)
    
    # featurize documents, authors
    with h5py.File(features_hdf5_path, "w") as fiel_feats:
        with h5py.File(icdar_authors_docs_hdf5_path, "r") as f:
            # do document-level features and author-level features (just means of document feats for now)
            authors_group = fiel_feats.create_group("authors")
            fragments_group = fiel_feats.create_group("fragments")
            for i, author in enumerate(f):
                fragments_author_group = fragments_group.create_group(author)
                author_fragments = []
                for fragment in f[author]:
                    fragments_fiel_features = ic_feat.fielify_doc_by_id(fragment, **kwargs)
                    fragment_dataset = fragments_author_group.create_dataset(fragment, data=fragments_fiel_features)
                    # check that any features were extracted at all, if not 
                    # then do not use fragment for author-level features
                    if len(fragments_fiel_features.shape) > 0:
                        author_fragments.append(fragment_dataset)
                    else:
                        logger = logging.getLogger(__name__)
                        logger.info("No features extracted for {0} (threshold too high?)".format(fragment))
                # get author-level features by aggregating over documents
                try:
                    author_mean = np.mean(author_fragments, axis=0)
                except:
                    print author_fragments
                    raise
                authors_group.create_dataset(author, data=author_mean)


def demo_shingles():
    # get an ICDAR image
    icdar_path = "/fileserver/icdar13/benchmarking-processed/author_icdar_be.hdf5"
    icdar_hdf5 = h5py.File(icdar_path, "r")
    img = icdar_hdf5['001']['001_1.tif']
    
    inf_shingler = StepShingler(img, hstep=90, vstep=120, shingle_size=(120,120))

    plt.figure(figsize=(10, 3))
    for i, shingle in enumerate(inf_shingler):
        plt.subplot(1,9,i+1)
        plt.imshow(shingle,cmap='gray')
        plt.tick_params(
            axis='both',
            which='both',      
            bottom='off',      
            top='off',        
            left='off',
            right='off',
            labelbottom='off',
            labelleft='off') 

        if (i+1) % 9 == 0:
            plt.show()
            break
            
def demo_shingle_iteration():
    # get ICDAR images
    icdar_path = "/fileserver/icdar13/benchmarking-processed/author_icdar_be.hdf5"
    icdar_hdf5 = h5py.File(icdar_path, "r")

    icdar_shingles = shingles_4_inference(icdar_hdf5, var_threshold=0.025, verbose=False)
    if icdar_shingles is not None:
        for icdar_shingle, author_id, fragment_id in icdar_shingles:
            logger=logging.getLogger(__name__)
            logger.info(icdar_shingle.shape)
            #a2p.display_img_array(icdar_shingle)
            plt.imshow(icdar_shingle, cmap='gray')
            plt.show()
            print "Author: {0}, Fragment: {1}".format(author_id, fragment_id)
            shingle_var = np.var(icdar_shingle.reshape(-1))
            print "Variance: {0}".format(shingle_var)
            IPython.display.clear_output(wait=True)
            time.sleep(0.15)
            
# demo_shingles()
# demo_shingle_iteration()
if __name__ == "__main__":

    demo_shingle_iteration()

