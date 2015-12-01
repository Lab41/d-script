import pickle
import numpy
import keras
import time

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

import h5py
import random
import numpy as np
from collections import defaultdict
from minibatcher import MiniBatcher

num_authors=40

model = Sequential()
model.add(Convolution2D(48, 12, 12,
                    border_mode='full',
                    input_shape=(1, 120, 120),
                    activation='relu'))
#model.add(Activation('relu'))

model.add(Convolution2D(48, 6, 6, activation='relu'))
#model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Convolution2D(128, 6, 6, border_mode = 'full', activation='relu'))
#model.add(BN(epsilon=1e-6))
#model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.5))

model.add(Convolution2D(128, 3, 3, border_mode = 'full', activation='relu'))
#model.add(BN(epsilon=1e-6))
#model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))


#model.add(Convolution2D(128, 6, 6, border_mode = 'full', activation='relu'))
#model.add(BN(epsilon=1e-6))
#model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_authors))
model.add(Activation('softmax'))

model.load_weights('/work/data/authors_40_forms_per_author_15_epoch_8100.hdf5.hdf5')
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

def partialnetwork(model, layernum):
    ''' def partialnetwork(model, layernum):
        model: the original full model
        layernum: the last layer of the neural network that you want to evaluate
        
        returns partial_model: the resulting neural network
    '''
    if len(model.layers) < layernum:
        return model
    
    rmodel = Sequential()
    for i in xrange(layernum):
        rmodel.add(model.layers[i])
    
    rmodel.compile(loss='mse', optimizer='adadelta')
    return rmodel

