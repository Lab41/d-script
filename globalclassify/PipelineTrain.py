#!/usr/bin/env python

from functools import partial
import numpy as np
import h5py
import sys
import logging
sys.path.append('../')

# Neural network stuff
import data_iters
from data_iters.hdf5_iterator import Hdf5GetterBatcher
from data_iters.minibatcher import MiniBatcher
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from fielutil import load_verbatimnet, patnet_layers
from preprocessing.segmentation import original_connected

#from data_iters.archive.iam_iterator import IAM_MiniBatcher


# ### File names
# 
# You will require:
# 1. HDF5 Files:
#     a. Author-Lines
#     b. Flat Images
# 2. Params (for the neural network you're looking at)


# Which training dataset do we want to train from?
train_dataset='iam-forms'
#train_dataset='nmec'


# Do you want to load the features in? Or save them to a file?
load_features = False

# All the images that you require extraction should be in this HDF5 file
if train_dataset=='nmec':
    hdf5authors='/memory/nmec_scaled_author_form.hdf5'
    hdf5authors='/fileserver/nmec-handwriting/nmec_scaled_author_form.hdf5'
    # hdf5authors='/fileserver/nmec-handwriting/author_nmec_bin_uint8.hdf5'
    hdf5images='nmecdata/nmec_scaled_flat.hdf5'
elif train_dataset=='iam-words':
    hdf5authors='/fileserver/iam/iam-processed/words/author_words.hdf5'
elif train_dataset=='iam-forms':
    hdf5authors='/fileserver/iam/iam-processed/forms/author_forms.hdf5'
    hdf5images='/fileserver/iam/iam-processed/forms/forms.hdf5'
elif train_dataset=='iam-lines':
    hdf5authors='/fileserver/iam/iam-processed/lines/author_lines.hdf5'
else:
    hdf5authors='/fileserver/iam/iam-processed/forms/author_forms.hdf5'

# This is the file that you will load the features from or save the features to
# featurefile = 'icdar13data/benchmarking-processed/icdar13be_fiel657.npy'
# featurefile = 'icdar13data/experimental-processed/icdar13ex_fiel657.npy'
#featurefile = 'nmecdata/nmec_fiel657_features.npy'

# This is the neural networks and parameters you are deciding to use
#paramsfile = '/fileserver/iam/iam-processed/models/fiel_657.hdf5'


# ### Parameter Definitions

# In[5]:

labels = h5py.File(hdf5authors, 'r')
num_authors=len(labels)
num_forms_per_author=-1
shingle_dim=(56,56)
batch_size=32
load_size=batch_size*1000
iterations = 10000
lr = 0.001


# ### Define your model
# 
print "Compiling model"
patnet = patnet_layers(num_authors, (1, 56, 56))
sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
patnet.compile(loss='categorical_crossentropy', optimizer=sgd)
print "Finished compilation"


from PIL import Image
def randangle(batch):
    newbatch = np.zeros(batch.shape)
    for i,im in enumerate(batch):
        
        newbatch[i]=imangle
    return newbatch

def iam_forms_pre(x, **kwargs):
    # Chop the top and bottom off
    x_new = x[700:2700]

    return x_new

def iam_forms_post(x, **kwargs):
    x_new = 1 - x/255.
    return x_new


# ### Minibatcher (to load in your data for each batch)
rng = np.random.RandomState(888)

print "Getting Data"
cc_getter = partial(original_connected.connected_component_getter, 
                    shingle_dim=shingle_dim,
                    rng=rng,
                    fill_value=255,
                    preprocess_doc=iam_forms_pre,
                    postprocess=iam_forms_post)

batch_object = Hdf5GetterBatcher(hdf5authors, 
                     num_authors=num_authors,
                     num_forms_per_author=num_forms_per_author,
                     item_getter=cc_getter,
                     default_mode=MiniBatcher.TRAIN,
                     batch_size=load_size,
                     train_pct=.7, test_pct=.2, val_pct=.1,
                     rng=rng)    


# ### Train your model for however many specified iterations

print "Starting training"
# logging.getLogger('data_iters.hdf5_iterator').setLevel(logging.DEBUG)
for batch_iter in range(iterations):
    (X_train,Y_train) = batch_object.get_train_batch()
    X_train = X_train.reshape((batch_size, 1) + shingle_dim)
    Y_train = to_categorical(Y_train, num_authors)
    patnet.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=1, show_accuracy=True, verbose=1)
    print "Finished training on the "+str(batch_iter)+"th batch"
    if (batch_iter % 20)==0 and batch_iter != 0:
        patnet.save_weights('/work/d-script/weights/patnet-iam.hdf5', overwrite=True)


#patnet.fit(X_train, Y_train, batch_size=32, nb_epoch=1, show_accuracy=True, verbose=1)

