import time
import random
import numpy as np
from collections import defaultdict
from optparse import OptionParser
import pickle
import h5py

# Required neural network libraries
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

# Plotting and stuffs (which probably won't work due to X11 issues)
import matplotlib.pylab as plt
import sys

# d-script imports
sys.path.append('..')
import data_iters
from data_iters.hdf5_iterator import Hdf5MiniBatcher
from data_iters.archive.iam_iterator import IAM_MiniBatcher
from data_iters.minibatcher import MiniBatcher

# Denoising stuff
from data_iters.CoffeeStainer import *
from data_iters.NoiseAdder import *

def basic_model( shingle_dim=(70,70) ):

    model = Sequential()
    model.add(Convolution2D(24, 6, 6,
                            border_mode='valid',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(1000))
    model.add(Dense(np.prod(shingle_dim)))
    model.add(Activation('sigmoid'))

    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model

def conv2_model( shingle_dim=(56,56) ):

    model = Sequential()
    model.add(Convolution2D(64, 6, 6,
                            border_mode='valid',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))

    model.add(Convolution2D(128, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Dense(np.prod(shingle_dim)))
    model.add(Activation('sigmoid'))

    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model

def conv2p_model( shingle_dim=(56,56) ):

    model = Sequential()
    model.add(Convolution2D(64, 6, 6,
                            border_mode='valid',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(128, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Dense(np.prod(shingle_dim)))
    model.add(Activation('sigmoid'))
    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model

def conv3p_model( shingle_dim=(56,56) ):

    model = Sequential()
    model.add(Convolution2D(64, 6, 6,
                            border_mode='valid',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(128, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Convolution2D(64, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu')) 
    model.add(Dense(np.prod(shingle_dim)))
    model.add(Activation('sigmoid'))
    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model

def conv4p_model( shingle_dim=(56,56) ):

    model = Sequential()
    model.add(Convolution2D(128, 6, 6,
                            border_mode='valid',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(128, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Convolution2D(128, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    
    model.add(Convolution2D(64, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu')) 
    
    model.add(Dense(2048))
    model.add(Activation('relu')) 
    
    model.add(Dense(np.prod(shingle_dim)))
    model.add(Activation('sigmoid'))
    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model

def conv4p2_model( shingle_dim=(120,120) ):

    model = Sequential()
    model.add(Convolution2D(64, 6, 6,
                            border_mode='valid',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(128, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Convolution2D(64, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu')) 

    model.add(Convolution2D(64, 4, 4,
                            border_mode='valid'))
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu')) 
    model.add(Dense(np.prod(shingle_dim)))
    model.add(Activation('sigmoid'))
    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model

def conv4p2c_model( shingle_dim=(120,120) ):

    model = Sequential()
    model.add(Convolution2D(64, 4, 4,
                            border_mode='same',
                            input_shape=(1, shingle_dim[0], shingle_dim[1])))
    model.add(Activation('relu'))

    model.add(Convolution2D(128, 8, 8,
                            border_mode='same'))
    model.add(Activation('relu')) 
    
    model.add(Convolution2D(64, 8, 8,
                            border_mode='same'))
    model.add(Activation('relu')) 

    model.add(Convolution2D(8, 32, 32,
                            border_mode='same'))
    model.add(Activation('relu'))
    
    model.add(Convolution2D(1, 120, 120, border_mode='same'))
    model.add(Activation('sigmoid'))
    print "Compiling model"
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.7, nesterov=False)
    model.compile(loss='mse', optimizer=sgd)
    print "Finished compilation"

    return model
