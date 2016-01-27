import numpy as np
import h5py
import sys
sys.path.append('..')

# d-script imports
from class_icdar_iterator import *
from data_iters.minibatcher import MiniBatcher
from fielutil import verbatimnet, loadparams

# Shingle, horizontal, and vertical step sizes
ss = (56,56)
hs = 30
vs = 30

def load_verbatimnet( layer, params='/fileserver/iam/iam-processed/models/fiel_1k.hdf5' ):

    print "Establishing Fiel's verbatim network"
    vnet = verbatimnet(layer)
    loadparams( vnet, params )
    vnet.compile( loss='mse', optimizer='sgd' )
    print "Compiled neural network up to FC7 layer"    
    
    return vnet

def extract_imfeats( hdf5name, network, shingle_dims=(56,56) ):

    # Image files
    hdf5file=h5py.File(hdf5name)

    # Final output of neural network
    imfeatures = np.zeros( (0,4096) )

    # Loop through all the images in the HDF5 file
    for imname in hdf5file.keys():
        img = 1.0 - hdf5file[imname].value /255.0 
        shards = np.zeros( (0, 1, shingle_dims[0], shingle_dims[1]) )

        # Collect the inputs for the image
        for shard in StepShingler(img, hstep=20, vstep=20, shingle_size=(56,56)):    
            shard = np.expand_dims(np.expand_dims(shard, 0),0)
            shards = np.concatenate( (shards, shard) )
        print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
        sys.stdout.flush()

        # Predict the neural network and append the mean of features to overall imfeatures
        features = network.predict( shards, verbose=1 )
        imfeatures = np.concatenate( (imfeatures, np.expand_dims(features.mean(axis=0),0)) )
        
    return imfeatures

if __name__ == "__main__":
    
    # Step 1: This is the filename of the HDF5 file with the original images (forms)
    hdf5name='icdar13data/experimental-processed/icdar13_ex.hdf5'
    hdf5name='icdar13data/benchmarking-processed/icdar_be.hdf5'
    
    # Step 2: Load the neural network in for feature extraction
    vnet = load_verbatim( 'fc7' )
    
    # Step 3: Extract image features by averaging shard features
    imfeats = extract_imfeats( hdf5name, vnet )
