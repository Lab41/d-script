import pickle
import numpy
import keras

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

datafile='/work/iam-data/output_shingles_sample.pkl'
CreateModel_k=False
CreateModel_m=True
Compile=True
LoadData=True
split = 0.8

if CreateModel_k:
    # Define the model
    model = Sequential()
    # model.add(Convolution2D(48, 12, 12, border_mode = 'full', input_shape=(1,120,120)))
    model.add(Convolution2D(48, 12, 12, border_mode = 'full', input_shape=(1,28,28)))
    model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    
    model.add(Convolution2D(48, 6, 6, border_mode = 'full'))
    model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
   
    model.add(Convolution2D(128, 6, 6, border_mode = 'full'))
    model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(128, 3, 3, border_mode = 'full'))
    model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(128, 3, 3, border_mode = 'full'))
    model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
 
    model.add(Flatten())
    model.add(Dense(256))
    # model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(256))
    # model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(5))
    model.add(Activation('softmax'))

if CreateModel_m:
    model = Sequential()
    model.add(Convolution2D(48, 12, 12,
                        border_mode='full',
                        input_shape=(1, 120, 120)))
    model.add(Activation('relu'))
    model.add(Convolution2D(48, 6, 6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Convolution2D(128, 6, 6, border_mode = 'full'))
    model.add(BN(epsilon=1e-6))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    
    
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(5))
    model.add(Activation('softmax'))
  
if Compile: 
    print "Compiling model" 
    # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    # sgd = SGD(lr=0.0001)
    # model.compile(loss='categorical_crossentropy', optimizer=sgd)
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    print "Finished compilation"

if LoadData:
    data = pickle.load(open(datafile))
    authors = data.keys()

    # Thought this would help with speed by pre-initializing data matrix
    imcount = 0
    imcount += sum( len(data[author]) for author in authors )
    randomdata = numpy.zeros( (imcount, 120, 120) )
    randomclass = numpy.zeros( imcount )

    # Load in all the data into matrix to pass to Keras
    imcount = 0
    authorcount = 0
    for author in authors:
        for shard in data[author]:
            randomdata[imcount,:,:] = shard
            randomclass[imcount] =authorcount
            imcount+=1
        authorcount+=1
    randomorder = numpy.random.permutation(imcount)
    randomdata = randomdata[ randomorder, :, : ]
    randomclass = randomclass[ randomorder ]

    realsplit = int(split*imcount)
    X_train = randomdata[0:realsplit,:,:]
    Y_train = randomclass[0:realsplit]

    X_train = numpy.expand_dims(X_train, 1)
    Y_train = to_categorical(Y_train, authorcount)

    X_test = randomdata[realsplit:,:,:]
    Y_test = randomclass[realsplit:]

    X_test = numpy.expand_dims(X_test, 1)
    Y_test = to_categorical(Y_test, authorcount)

    X_train/=255.0
    X_test/=255.0
    X_train = 1.0 - X_train
    X_test = 1.0 - X_test

    # trainmean=X_train.mean()
    # X_train -= trainmean
    # X_test -= trainmean
    # X_train *= 128
    # X_test *= 128

# model.fit(X_train, Y_train, batch_size=32, nb_epoch=100)
model.fit(X_train, Y_train, batch_size=128, nb_epoch=100, show_accuracy=True, verbose=1, validation_data=(X_test, Y_test))
