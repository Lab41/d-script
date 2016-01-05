import sys
import logging
import time
import random
import numpy as np
from collections import defaultdict, namedtuple
from optparse import OptionParser


class StepShingler:
    
    ShingleSize=namedtuple('ShingleSize', ['rows','cols'])
    
    def __init__(self, img, 
                 hstep, vstep, 
                 shingle_size=ShingleSize(rows=120,cols=120)):
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
            logger = logging.getLogger(__name__)
            logger.debug("Horizontal step/window settings do not divide evenly into image width. "
                        "{0} pixels of information will be lost".format(h_step_margin))
        v_step_space = img.shape[0] - self.shingle_size.rows
        # number of pixels left over on bottom edge
        v_step_margin = v_step_space % vstep
        if v_step_margin != 0:
            logger = logging.getLogger(__name__)
            logger.debug("Vertical step/window settings do not divide evenly into image width. "
                        "{0} pixels of information may be lost".format(v_step_margin))
        
    def __iter__(self):
        for row_i in xrange(0, self.img.shape[0] - self.shingle_size[0], self.vstep):
            for col_j in xrange(0, self.img.shape[1] - self.shingle_size[1], self.hstep):
                logger = logging.getLogger(__name__)
                logger.info("Row {0}, Col {1}".format(row_i, col_j))
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
