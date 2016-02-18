import numpy as np
import h5py
import sys
sys.path.append('..')

# d-script imports
from class_icdar_iterator import *
from data_iters.minibatcher import MiniBatcher
from fielutil import verbatimnet, loadparams

# Required neural network libraries
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

from noisenet import basic_model, conv2_model

# Shingle, horizontal, and vertical step sizes
ss = (56,56)
hs = 30
vs = 30

def load_verbatimnet( layer, input_shape=(1,56,56), params='/fileserver/iam/iam-processed/models/fiel_1k.hdf5' ):

    print "Establishing Fiel's verbatim network"
    vnet = verbatimnet(layer=layer, input_shape=input_shape)
    loadparams( vnet, params )
    vnet.compile( loss='mse', optimizer='sgd' )
    print "Compiled neural network up to FC7 layer"    
    
    return vnet

def load_denoisenet(shingle_dim=(56,56)):
    model=conv2_model()
    model.load_weights('conv2_linet_icdar-ex.hdf5')
    return model

def extract_imfeats( hdf5name, network, shingle_dims=(56,56), steps=(20,20), varthresh=250.0 ):

    # Image files
    hdf5file=h5py.File(hdf5name)

    # Final output of neural network
    imfeatures = np.zeros( (0,4096) )
    
    # Noise network
    noisenet = load_denoisenet()

    # Loop through all the images in the HDF5 file
    for imname in hdf5file.keys():
        img = 1.0 - hdf5file[imname].value /255.0 
        shards = []

        # Collect the inputs for the image
        for shard in StepShingler(img, hstep=steps[1], vstep=steps[0], shingle_size=shingle_dims):
            shard = np.expand_dims(shard,0)
            if varthresh and shard.sum() < varthresh:
                continue
            shards += [shard]
          
        shards = np.array(shards)
        shardsize = shards.shape

        print "Denoising network predicting on shards"
        if len(shards)==0:
            imfeatures = np.concatenate( (imfeatures, np.zeros((1,4096))) )
            print "ERROR: "+imname+" has ZERO shards as input; continuing"
            continue
        sys.stdout.flush()
        shards = noisenet.predict(shards, verbose=1)
        shards = shards.reshape( shardsize )
        if varthresh:
            shards = np.array([ shard for shard in shards if shard.sum() > varthresh ])
        
        print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
        sys.stdout.flush()
        # Predict the neural network and append the mean of features to overall imfeatures
        if len(shards)!=0:
            features = network.predict( shards, verbose=1 )
            imfeatures = np.concatenate( (imfeatures, np.expand_dims(features.mean(axis=0),0)) )
        else:
            imfeatures = np.concatenate( (imfeatures, np.zeros((1,4096))) )
        
    return imfeatures



# From author format to flat format
def author2flatformat( hdf5_input_name, hdf5_output_name ):
    
    h5in = h5py.File(hdf5_input_name, 'r')
    h5out = h5py.File(hdf5_output_name, 'w')
    
    for author in h5in:
        for filename in h5in[author]:
            data = h5in[author][filename]
            data_group = h5out.create_dataset( filename, data=data.value.astype(np.uint8) )
            data_group.attrs['author']=author
    
    h5in.close()
    h5out.close()
    

if __name__ == "__main__":
    
    # Step 1: This is the filename of the HDF5 file with the original images (forms)
    hdf5name='icdar13data/experimental-processed/icdar13_ex.hdf5'
    hdf5name='icdar13data/benchmarking-processed/icdar_be.hdf5'
    
    # Step 2: Load the neural network in for feature extraction
    vnet = load_verbatim( 'fc7' )
    
    # Step 3: Extract image features by averaging shard features
    imfeats = extract_imfeats( hdf5name, vnet )
