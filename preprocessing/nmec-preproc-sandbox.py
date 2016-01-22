import time
import random
import numpy as np
from collections import defaultdict
from optparse import OptionParser
import pickle
import scipy.misc as smi

# Required libraries
import h5py
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

import matplotlib.pylab as plt
import matplotlib.cm as cm
from IPython.display import Image, display
# %matplotlib inline

import sys
sys.path.append('../repo/d-script/')
# d-script imports
from data_iters.minibatcher import MiniBatcher
from data_iters.iam_hdf5_iterator import IAM_MiniBatcher
from viz_tools.array_to_png import get_png_from_array, display_img_array

from feat_extract.fielutil import *
from viz_tools.VizUtils import *
from scipy.ndimage.morphology import *

containerdir = '/fileserver/'
containerdir = '/data/fs4/datasets/'
frenchdir = containerdir+'nmec-handwriting/stil-writing-corpus/French/French-Images/'

im = readtif( frenchdir+'FR-041-002.tif' )
# plt.imshow(im, cmap = cm.Greys_r )

bim = np.round( 1.0 - im / 255.0 ).astype(int)
# plt.figure(1)
# plt.imshow( 1-bim, cmap=cm.Greys_r )

# Binary erosion:
ebim = binary_erosion( bim, iterations=5 )
# plt.figure(2)
# plt.imshow( 1-ebim, cmap=cm.Greys_r )

bg = readcolim( 'paperTexture.jpeg' )
bimp = ebim[2000:2400,2000:2400].astype(int)
nbimp = np.zeros( bg.shape )
for i in xrange(3):
    nbimp[:,:,i] = (1-bimp)*bg[:,:,i]
nbimp = nbimp.astype(int)

plt.figure(1)
plt.imshow( 1-bimp, cmap='gray' )
plt.figure(2)
plt.imshow(nbimp[:,:,0], cmap='gray')
