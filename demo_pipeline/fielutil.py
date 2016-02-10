import time
import random
import numpy as np
from collections import defaultdict
from optparse import OptionParser
import pickle

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
import sys
sys.path.append('..')
# d-script imports
from data_iters.minibatcher import MiniBatcher
# from data_iters.hdf5_iterator import IAM_MiniBatcher
from class_icdar_iterator import *


from PIL import Image
def randangle(batch):
    newbatch = np.zeros(batch.shape)
    for i,im in enumerate(batch):
        imangle = np.asarray(Image.fromarray(im.squeeze()).rotate(7.5*np.random.randn()))
        newbatch[i]=imangle
    return newbatch

# Get a shingle from a line with dimension shingle_dim
def get_shingle(original_line, shingle_dim):
    # Pull shingle from the line
    (height, width) = original_line.shape
    max_x = max(width - shingle_dim[1], 0)
    max_y = max(height - shingle_dim[0], 0)
    x_start = random.randint(0, max_x)
    y_start = random.randint(0, max_y)
    if width < shingle_dim[1] or height < shingle_dim[0]: # The line is too small in at least one access
        output_arr = np.zeros(shingle_dim)
        output_arr.fill(255)
        output_arr[:height,:width] = original_line[:min(height, shingle_dim[0]), :min(width, shingle_dim[1])]
        return output_arr
    else:
        return original_line[y_start:y_start+ shingle_dim[0], x_start:x_start+shingle_dim[1]]

# From a dictionary, get a random sample
def sample_dictionary( the_dict ):
    keys = the_dict.keys()
    sampleno = np.random.randint(0, len(keys))
    randkey = keys[sampleno]
    return the_dict[ randkey ]    
    
# From an HDF5 file, a list of author ID's, return a minibatch
def get_batch( author_hdf5_file, author_ids, shingle_size=(120,120), data_size=32 ):
    
    author_keys = author_ids.keys()
    author_rands = np.random.randint(0, len(author_keys), data_size)
    
    author_batch = np.zeros( (data_size, shingle_size[0], shingle_size[1]))
    author_truth = np.zeros( data_size )
    for i, author_rand in enumerate(author_rands):
        author_group = author_hdf5_file[ author_keys[author_rand] ]
        author_batch[i,:,:] = get_shingle( sample_dictionary( author_group ).value , shingle_size)
        author_truth[i] = author_ids[ author_keys[author_rand] ]
        
    return author_batch, author_truth

def tfdnet( hdf5file, layer='softmax', compile=False ):
    model = Sequential()
    model.add(Convolution2D(48, 12, 12,
                        border_mode='valid',
                        input_shape=(1, shingle_dim[0], shingle_dim[1])))

    model.add(BN())
    #model.add(PReLU())
    model.add(Activation('relu'))

    model.add(Convolution2D(48, 6, 6))
    model.add(BN())
    model.add(Activation('relu'))
    #model.add(PReLU())
    model.add(MaxPooling2D(pool_size=(2,2)))
    #model.add(Dropout(0.25))

    model.add(Convolution2D(128, 6, 6, border_mode = 'valid'))
    model.add(BN())
    model.add(Activation('relu'))
    #    model.add(PReLU())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #    #model.add(Dropout(0.5))

    model.add(Convolution2D(128, 3, 3, border_mode = 'valid'))
    model.add(BN())
    model.add(Activation('relu'))
    #model.add(PReLU())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(BN())
    model.add(Activation('relu'))
    if layer=='fc6':
        f = h5py.File(hdf5file)
        for k in range(18):
            g = f['layer_{}'.format(k)]
            weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
            model.layers[k].set_weights( weights )
        f.close()
        return model

    
    model.add(Dense(128))
    model.add(BN())
    model.add(Activation('relu'))
    #model.add(Dropout(0.5))
    if layer=='fc7':
        f = h5py.File(hdf5file)
        for k in range(22):
            g = f['layer_{}'.format(k)]
            weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
            model.layers[k].set_weights( weights )
        f.close()
        return model

    model.add(Dense(num_authors))

    if layer=='fc8':
        f = h5py.File(hdf5file)
        for k in range((f.attrs['nb_layers']) - 1):
            g = f['layer_{}'.format(k)]
            weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
            model.layers[k].set_weights( weights )
        f.close()
        return model
        
    model.add(Activation('softmax'))
    
    if compile:
        print "Compiling model"
        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
        model.compile(loss='categorical_crossentropy', optimizer=sgd)
        print "Finished compilation"

    model.load_weights( hdf5file )

    return model

    
def verbatimnet( layer='softmax', compiling=False ):
    
    layers = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5',
              'fc6', 'fc7', 'softmax']
    
    model = Sequential()
    model.add(Convolution2D(96, 11, 11,
                            border_mode='valid', subsample=(4,4),
                            input_shape=(1, 56, 56),
                            activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    if layer in layers[-7:]:
        model.add(Convolution2D(96, 5, 5, activation='relu', border_mode='same'))
        model.add(MaxPooling2D(pool_size=(2,2)))

    if layer in layers[-6:]:
        model.add(Convolution2D(256, 3, 3, border_mode = 'same', activation='relu'))

    if layer in layers[-5:]:
        model.add(Convolution2D(256, 3, 3, border_mode = 'same', activation='relu'))

    if layer in layers[-4:]:
        model.add(Convolution2D(256, 3, 3, border_mode = 'same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(3, 3)))
        model.add(Dropout(0.25))
    
    if layer in layers[-3:]:
        model.add(Flatten())
        model.add(Dense(4096, activation='relu'))

    if layer in layers[-2:]:
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.25))
    
    if layer in layers[-1]:
        model.add(Dense(num_authors))
        model.add(Activation('softmax'))
    
    if compiling:
        print "Compiling model"
        sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd)
        print "Finished compilation"
    
    return model



def loadparams( model, hdf5file ):
    
    params = h5py.File(hdf5file)
    for k in range(len(model.layers)):
        # This method does not make use of Sequential.set_weights()
        # for backwards compatibility.
        g = params['layer_{}'.format(k)]
        weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
        model.layers[k].set_weights(weights)
    params.close()
    
    
def load_verbatimnet( layer, paramsfile = '/fileserver/iam/iam-processed/models/fiel_1k.hdf5', compiling=False ):

    print "Establishing Fiel's verbatim network"
    vnet = verbatimnet(layer,compiling=compiling)
    loadparams( vnet, paramsfile )
    print "Loaded neural network up to "+layer+" layer"    
    
    return vnet


def extract_imfeats( hdf5name, network ):

    # Image files
    hdf5file=h5py.File(hdf5name)

    # Final output of neural network
    imfeatures = np.zeros( (0,4096) )

    # Loop through all the images in the HDF5 file
    for imname in hdf5file.keys():
        img = 1.0 - hdf5file[imname].value /255.0 
        shards = np.zeros( (0, 1, 56, 56) )

        # Collect the inputs for the image
        for shard in StepShingler(img, hstep=30, vstep=30, shingle_size=(56,56)):    
            shard = np.expand_dims(np.expand_dims(shard, 0),0)
            shards = np.concatenate( (shards, shard) )
        print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
        sys.stdout.flush()

        # Predict the neural network and append the mean of features to overall imfeatures
        features = network.predict( shards, verbose=1 )
        imfeatures = np.concatenate( (imfeatures, np.expand_dims(features.mean(axis=0),0)) )
        
    return imfeatures
