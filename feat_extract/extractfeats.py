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
# %matplotlib inline

import sys
sys.path.append('/work/code/repo/d-script/')
# d-script imports
from data_iters.minibatcher import MiniBatcher
from data_iters.iam_hdf5_iterator import IAM_MiniBatcher

from fielutil import *

# Create feature extractor by loading in original model and lopping off last layer
model = fielnet('../convnets/fielnet/fielnet.hdf5')
featmodel = Sequential()
for i in xrange( len(model.layers)-4 ):
    featmodel.add( model.layers[i] )
featmodel.compile(loss='mse', optimizer='sgd')

# Data ingest and file IO
hdf5_file = '/memory/author_lines.hdf5'
num_forms_per_author=50
shingle_dim=(120,120)
use_form=True
iam_m = IAM_MiniBatcher(hdf5_file, num_authors, num_forms_per_author, shingle_dim=shingle_dim, use_form=use_form, default_mode=MiniBatcher.TRAIN, batch_size=batch_size)
[X_test, Y_test] = iam_m.get_test_batch(batch_size*20)
X_test = np.expand_dims(X_test, 1)
X_test = randangle(X_test)
Y_test = to_categorical(Y_test, num_authors)

# Let's test the feature extractor out!
f_test = featmodel.predict(X_test)

# Let's apply the feature extractor to an entire form.
im = smi.imread('/fileserver/iam/forms/h07-025a.png')

# Let's convert some dense layers into convolutional layers
dense_weights = model.layers[16].get_weights()
modeld2c = Sequential()
for i in xrange(15):
    modeld2c.add( model.layers[i] )
modeld2c.add( Convolution2D( 128, 10, 10, border_mode = 'valid' ) )
modeld2c.add( Activation('relu') )
    
modeld2c.predict( X_test )
