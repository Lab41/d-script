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
from fielutil import load_verbatimnet
from featextractor import extract_imfeats_debug

from data_iters.archive.iam_iterator import IAM_MiniBatcher

from PIL import Image
def randangle(im, rng=np.random):
    newbatch = np.zeros(im.shape)
    # for i,im in enumerate(batch):
    #     imangle = np.asarray(Image.fromarray(im.squeeze()).rotate(7.5*rng.randn()))
    #     newbatch[i]=imangle
    imangle = np.asarray(Image.fromarray(im.squeeze()).rotate(7.5*rng.randn()))
    newbatch = imangle
    return imangle

# def PipelineTdb():
if True:
    
    # Which training dataset do we want to train from?
    train_dataset='nmec'

    # Do you want to load the features in? Or save them to a file?
    load_features = False

    # All the images that you require extraction should be in this HDF5 file
    if train_dataset=='nmec':
        hdf5authors='/memory/nmec_scaled_author_form.hdf5'
        hdf5authors='/fileserver/nmec-handwriting/nmec_scaled_author_form.hdf5'
        hdf5images='nmecdata/nmec_scaled_flat.hdf5'
    elif train_dataset=='iam-words':
        hdf5authors='/fileserver/iam/iam-processed/words/author_words.hdf5'
    elif train_dataset=='iam-lines':
        hdf5authors='/fileserver/iam/iam-processed/lines/author_lines.hdf5'
    else:
        hdf5authors='/fileserver/iam/iam-processed/forms/author_forms.hdf5'

    # This is the file that you will load the features from or save the features to
    # featurefile = 'icdar13data/benchmarking-processed/icdar13be_fiel657.npy'
    # featurefile = 'icdar13data/experimental-processed/icdar13ex_fiel657.npy'
    featurefile = 'nmecdata/nmec_fiel657_features.npy'

    # This is the neural networks and parameters you are deciding to use
    paramsfile = '/fileserver/iam/iam-processed/models/fiel_657.hdf5'


    ### Parameter Definitions

    labels = h5py.File(hdf5authors, 'r')
    num_authors=len(labels)
    num_forms_per_author=-1
    shingle_dim=(56,56)
    batch_size=320
    load_size=batch_size*1
    iterations = 1000
    lr = 0.001


    # ### Define your model
    # 
if False:
    # Here, we're using the Fiel Network
    vnet = load_verbatimnet( 'fc7', paramsfile=paramsfile, compiling=False )
    vnet.add(Dense(num_authors))
    vnet.add(Activation('softmax'))
    sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
    vnet.compile(loss='categorical_crossentropy', optimizer=sgd)
    print "Finished compilation"

if True:
    # ### Minibatcher (to load in your data for each batch)
    # logging.getLogger('data_iters.hdf5_iterator').setLevel(logging.DEBUG)
    if True:
        mini_m = Hdf5MiniBatcher(hdf5authors, num_authors, num_forms_per_author, preprocess=None,
                                shingle_dim=shingle_dim, default_mode=MiniBatcher.TRAIN,
                                batch_size=load_size, add_rotation=False)
    else:
        mini_m = IAM_MiniBatcher(hdf5authors, num_authors, num_forms_per_author,
                                shingle_dim=shingle_dim, default_mode=MiniBatcher.TRAIN,
                                batch_size=load_size)


    # ### Train your model for however many specified iterations

    # logging.getLogger('data_iters.hdf5_iterator').setLevel(logging.DEBUG)
    for batch_iter in range(100):
        (X_train,Y_train) = mini_m.get_train_batch()
        # X_train = 1.0 - X_train / 255.0
        X_train = np.expand_dims(X_train, 1)
        Y_train = to_categorical(Y_train, num_authors)
        vnet.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=1, show_accuracy=True, verbose=1)
        print "Finished training on the "+str(batch_iter)+"th batch"
        if (batch_iter % 20)==0 and batch_iter != 0:
            model.save_weights('fielnet-nmec.hdf5', overwrite=True)

    vnet.fit(X_train, Y_train, batch_size=32, nb_epoch=1, show_accuracy=True, verbose=1)