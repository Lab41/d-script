import numpy as np
import h5py
import sys
import logging
sys.path.append('../')

# Neural network stuff
import data_iters
from data_iters.hdf5_iterator import Hdf5MiniBatcher
from data_iters.minibatcher import MiniBatcher
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from fielutil import load_verbatimnet, verbatimnet

from data_iters.archive.iam_iterator import IAM_MiniBatcher


# ### File names
# 
# You will require:
# 1. HDF5 Files:
#     a. Author-Lines
#     b. Flat Images
# 2. Params (for the neural network you're looking at)


# Which training dataset do we want to train from?
train_dataset='iam-lines'

# All the images that you require extraction should be in this HDF5 file
if train_dataset=='nmec':
    hdf5authors='/fileserver/nmec-handwriting/nmec_scaled_author_form.hdf5'
    hdf5authors='/fileserver/nmec-handwriting/nmec_scaled_author_form.hdf5'
    hdf5authors='/fileserver/nmec-handwriting/author_nmec_bin_cropped_uint8.hdf5'
    hdf5authors='/fileserver/nmec-handwriting/author_nmec_no8_bin_cropped_uint8.hdf5'
elif train_dataset=='iam-words':
    hdf5authors='/fileserver/iam/iam-processed/words/author_words.hdf5'
elif train_dataset=='iam-lines':
    hdf5authors='/fileserver/iam/iam-processed/lines/author_lines.hdf5'
else:
    hdf5authors='/fileserver/iam/iam-processed/forms/author_forms.hdf5'

# This is the neural networks and parameters you are deciding to use
paramsfile = '/fileserver/iam/iam-processed/models/fiel_657.hdf5'


# ### Parameter Definitions
labels = h5py.File(hdf5authors, 'r')
num_authors=len(labels)
num_forms_per_author=-1
shingle_dim=(120,120)
batch_size=32
load_size=batch_size*1000
iterations = 1000
lr = 0.001

### Define your model
# Here, we're using the Fiel Network
# vnet = load_verbatimnet( 'fc7', paramsfile=paramsfile, compiling=False )
vnet = verbatimnet( layer='fc7', input_shape=(1,)+shingle_dim, compiling=False )
vnet.add(Dense(num_authors))
vnet.add(Activation('softmax'))
sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
vnet.compile(loss='categorical_crossentropy', optimizer=sgd)
print "Finished compilation"


# ### Minibatcher (to load in your data for each batch)
if False:
    mini_m = Hdf5MiniBatcher(hdf5authors, num_authors, num_forms_per_author,
                            shingle_dim=shingle_dim, default_mode=MiniBatcher.TRAIN,
                            batch_size=batch_size, add_rotation=True)
else:
    mini_m = IAM_MiniBatcher(hdf5authors, num_authors, num_forms_per_author,
                            shingle_dim=shingle_dim, default_mode=MiniBatcher.TRAIN,
                            batch_size=load_size)

from PIL import Image
def randangle(batch):
    newbatch = np.zeros(batch.shape)
    for i,im in enumerate(batch):
        imangle = np.asarray(Image.fromarray(im.squeeze()).rotate(7.5*np.random.randn()))
        newbatch[i]=imangle
    return newbatch

def get_pbatch( mini_m, load_size=32*1000, shingle_dim = (120,120) ):
        (X_train, Y_train) = mini_m.get_batch( load_size )
        X_train = 1.0 - X_train / 255.0
        X_train = np.expand_dims(X_train, 1)
        X_train = randangle(X_train)
        Y_train = to_categorical(Y_train, num_authors)
        return (X_train, Y_train)


### Train your model for however many specified iterations
# logging.getLogger('data_iters.hdf5_iterator').setLevel(logging.DEBUG)
for batch_iter in range(iterations):
    (X_train,Y_train) = get_pbatch(mini_m, load_size=load_size )
    vnet.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=1, show_accuracy=True, verbose=1) # , validation_data=(X_val, Y_val))
    print "Finished training on the "+str(batch_iter)+"th batch"
    if (batch_iter % 20)==0 and batch_iter != 0:
        vnet.save_weights('fielnet120-iam.hdf5', overwrite=True)

vnet.fit(X_train, Y_train, batch_size=32, nb_epoch=1, show_accuracy=True, verbose=1)

