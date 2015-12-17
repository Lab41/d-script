import time
import random
import numpy as np
from collections import defaultdict
from optparse import OptionParser

# Required libraries
import h5py
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

# d-script imports
from data_iters.minibatcher import MiniBatcher
from data_iters.iam_hdf5_iterator import IAM_MiniBatcher


def create_model(num_authors, shingle_dim, lr):
    model = Sequential()
    model.add(Convolution2D(48, 12, 12,
                        border_mode='valid',
                        input_shape=(1, shingle_dim[0], shingle_dim[1]),
                        activation='relu'))

    model.add(Convolution2D(48, 6, 6, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    #model.add(Convolution2D(128, 6, 6, border_mode = 'full', activation='relu'))
    model.add(Convolution2D(128, 6, 6, border_mode = 'valid', activation='relu'))
    #model.add(BN(epsilon=1e-6))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(Dropout(0.5))

    #model.add(Convolution2D(128, 3, 3, border_mode = 'full', activation='relu'))
    model.add(Convolution2D(128, 3, 3, border_mode = 'valid', activation='relu'))
    #model.add(BN(epsilon=1e-6))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_authors))
    model.add(Activation('softmax'))

    print "Compiling model"
    sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd)
    print "Finished compilation"

    return model

def run_model(hdf5_file, num_authors, num_forms_per_author, shingle_dim, num_iters=10, batch_size=32,
              use_form=False, lr=0.03):
    # Create Keras model
    model = create_model(num_authors, shingle_dim, lr)

    # Create a mini_batcher for
    iam_m = IAM_MiniBatcher(hdf5_file, num_authors, num_forms_per_author, shingle_dim=shingle_dim,
                            use_form=use_form, default_mode=MiniBatcher.TRAIN, batch_size=batch_size)


    # Get validation dataset
    [X_test, Y_test] = iam_m.get_test_batch(batch_size*20)
    X_test = np.expand_dims(X_test, 1)
    Y_test = to_categorical(Y_test, num_authors)
    print 'test_size:', X_test.shape, Y_test.shape


    for i in range(num_iters):
        print 'Starting Epoch: ', i
        start_time = time.time()
        # Get training batch
        (X_train, Y_train) = iam_m.get_train_batch(batch_size*100)
        X_train = np.expand_dims(X_train, 1)
        Y_train = to_categorical(Y_train, num_authors)

        # TODO: Maybe we should only validate every N iters since right now we are doing 20% extra work every iter
        model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=1,
                  show_accuracy=True, verbose=2, validation_data=(X_test, Y_test)) # verbose=1
        print 'Elapsed Time: ', time.time() - start_time

        # Set checkpoint every 500 iterations
        if i %500 == 0 and i != 0:
            fname = 'authors_%d_forms_per_author_%d_epoch_%d.hdf5'%(num_authors, num_forms_per_author, i)
            model.save_weights('%s.hdf5'%fname, overwrite=True)

    fname = 'authors_%d_forms_per_author_%d_final.hdf5'%(num_authors, num_forms_per_author)
    model.save_weights('%s.hdf5'%fname, overwrite=True)

def run_model_tuple(input_tuple):
    hdf5_file, num_authors, num_forms_per_author, shingle_dim, num_iters = input_tuple
    run_model(hdf5_file, num_authors, num_forms_per_author, shingle_dim, num_iters)

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Log file to read")
    parser.add_option("--num_authors", dest='num_authors', type=int, help="Number of authors to include")
    parser.add_option("--num_forms_per_author", dest='num_forms_per_author',
                      type=int, help="Number of forms per author required")
    parser.add_option("--shingle_dim", dest='shingle_dim', help="Shingle dimensions, comma separated i.e. 120,120")
    parser.add_option("--num_iters", dest="num_iters", type=int, help="Number of iterations to run model")
    parser.add_option("--batch_size", dest="batch_size", type=int, default=32, help="Iteration Batch Size")
    parser.add_option("--lr", dest="lr", type=float, default=0.03, help="Learning rate (e.g. 0.03)")
    parser.add_option("--from_form", dest="use_form", action='store_true', default=False)
    (options, args) = parser.parse_args()

    shingle_str = options.shingle_dim.split(',')
    shingle_dim = (int(shingle_str[0]), int(shingle_str[1]))

    run_model(options.filename, options.num_authors, options.num_forms_per_author,
              shingle_dim, options.num_iters, options.batch_size, options.use_form, options.lr)

if __name__ == "__main__":
    main()