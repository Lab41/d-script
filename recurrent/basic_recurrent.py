
# coding: utf-8

# # Basic Recurrent Neural Network
# 
# Testing out original code for a simple LSTM to understand the sequential writing of an author from left to right. (To do: bi-directional recurrent LSTMs.)
# 
# Details: 
# We require two additional layers that I've written to make the dimensions of the input to other layers consistent. 

# ### Imports

# In[1]:

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
from keras.layers.core import Layer
from keras.layers.recurrent import LSTM

import theano.tensor as T

import h5py
import random
import numpy as np
from collections import defaultdict
from minibatcher import MiniBatcher
import matplotlib.pylab as plt
# get_ipython().magic(u'matplotlib inline')


# ### New Keras layers for use in the recurrent network

# In[2]:

class Squeeze(Layer):
    '''
        Get rid of any dimensions of size 1.
        First dimension is assumed to be nb_samples.
    '''
    def __init__(self, **kwargs):
        super(Squeeze, self).__init__(**kwargs)

    @property
    def output_shape(self):
        input_shape = self.input_shape
        data_shape = tuple( np.array(input_shape)[ np.array(input_shape) > 1 ] )
        return (input_shape[0],)+ data_shape

    def get_output(self, train=False):
        X = self.get_input(train)
        # size = T.prod(X.shape) // X.shape[0]
        # nshape = (X.shape[0], size)
        # return T.reshape(X, output_shape)
        return X.squeeze()
    
class Transpose3(Layer):
    '''
        Get rid of any dimensions of size 1.
        First dimension is assumed to be nb_samples.
    '''
    def __init__(self, transpose_order, **kwargs):
        self.transpose_order = transpose_order
        super(Transpose3, self).__init__(**kwargs)

    @property
    def output_shape(self):
        input_shape = self.input_shape
        data_shape = ()
        for j in self.transpose_order:
            data_shape+=(input_shape[j],)
        return data_shape

    def get_output(self, train=False):
        X = self.get_input(train)
        # size = T.prod(X.shape) // X.shape[0]
        # nshape = (X.shape[0], size)
        # return T.reshape(X, output_shape)
        return X.transpose(self.transpose_order)


# ### Data (40 authors, 15 forms per author)

# In[3]:

num_authors=40
num_forms_per_author=15


hdf5_file = '/work/data/output_shingles_sparse.hdf5'

fIn = h5py.File(hdf5_file, 'r')
authors = []

# Filter on number of forms per author
for author in fIn.keys():
    if len(fIn[author]) > num_forms_per_author:
        authors.append(author)

if len(authors) < num_authors:
    raise ValueError("There are only %d authors with more than %d forms"%(len(authors), num_forms_per_author))
keys = []
# Get all the keys from our hdf5 file
for author in authors[:num_authors]: # Limit us to num_authors
    forms = list(fIn[author])
    for form in forms[:num_forms_per_author]: # Limit us to num_form_per_author
        for line_name in fIn[author][form].keys():
            for shingle in range(fIn[author][form][line_name].shape[0]):
                keys.append([(author,form,line_name), shingle])

# Normalization function which scales values from 0 (white) to 1 (black)
normalize = lambda x: 1.0 - x.astype(np.float32)/255.0

m = MiniBatcher(fIn, keys,normalize=normalize, batch_size=32, min_shingles=20*7*num_forms_per_author)

m.batch_size = 32*20
m.set_mode(MiniBatcher.TEST)
[X_test, Y_test] = m.get_batch()
X_test = np.expand_dims(X_test, 1)
Y_test = to_categorical(Y_test, num_authors)
print 'test_size:', X_test.shape, Y_test.shape

m.batch_size = 32*100
m.set_mode(MiniBatcher.TRAIN)


# ### Define the neural network
# 
# #### Current architecture
# 1. Convolution2D (48, 12, 12) + Relu + MaxPool (2,2)
# 2. Convolution2D (48, 6, 6 ) + Relu + MaxPool (2,2)
# 3. Convolution2D->1D (48, 6, 35) + Relu

# In[4]:

model = Sequential()
model.add(Convolution2D(48, 12, 12,
                    border_mode='full',
                    input_shape=(1, 120, 120),
                    activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Convolution2D(48, 6, 6,
                       border_mode='full',
                       activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(MaxPooling2D(pool_size=(70,2)))

model.add(Convolution2D(48, 6, 35, activation='relu'))
model.add(Squeeze())
model.add(Transpose3((0,2,1)))

model.add(LSTM(output_dim=48, activation='sigmoid', inner_activation='hard_sigmoid'))
model.add(Dense(40, activation='softmax'))

sgd = SGD(lr=0.015, decay=1e-6, momentum=0.5, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)
print "Finished compilation with optimization set to SGD"

model.load_weights('basic_recurrent.hd5')

m.batch_size = 32*100
m.set_mode(MiniBatcher.TRAIN)
for i in range(500):
    print 'Starting Epoch: ', i
    start_time = time.time()
    (X_train, Y_train) = m.get_batch()
    X_train = np.expand_dims(X_train, 1)
    Y_train = to_categorical(Y_train, num_authors)
    print X_train.shape, Y_train.shape
    model.fit(X_train, Y_train, batch_size=32, nb_epoch=1, show_accuracy=True, verbose=1, validation_data=(X_test, Y_test))
    print 'Elapsed Time: ', time.time() - start_time
    if numpy.mod(i,50)==0:
	print "Checkpoint at"+str(i)
	model.save_weights('basic_recurrent'+str(i)+'.hd5')
