import numpy as np
import h5py
import sys
from scipy.fftpack import dct
sys.path.append('..')

# d-script imports
from class_icdar_iterator import *
from data_iters.minibatcher import MiniBatcher
from fielutil import verbatimnet, loadparams

# Shingle, horizontal, and vertical step sizes
ss = (56,56)
hs = 30
vs = 30

## Patch filters --------------------------
# Two dimensional discrete cosine transform
def dct2filt( patch, varthresh ):
    return dct(dct(patch,axis=0),axis=1)
def varfilt( patch, varthresh ):
    return np.var(shard) < varthresh


## Neural Networks --------------------------
# Load the verbatim neural network feature extractor (up to FC7 layer)
def load_verbatimnet( layer, params='/fileserver/iam/iam-processed/models/fiel_1k.hdf5' ):

    print "Establishing Fiel's verbatim network"
    vnet = verbatimnet(layer)
    loadparams( vnet, params )
    vnet.compile( loss='mse', optimizer='sgd' )
    print "Compiled neural network up to FC7 layer"    
    
    return vnet

## Corpus operator --------------------------
# Extract features over the entire corpus. Takes in the flat hdf5 file.
def extract_imfeats( hdf5name, network, shingle_dims=(56,56), steps=(20,20), varthresh=None ):

    # Image files
    hdf5file=h5py.File(hdf5name)

    # Final output of neural network
    imfeatures = np.zeros( (0,4096) )

    # Loop through all the images in the HDF5 file
    for imname in hdf5file.keys():
        img = 1.0 - hdf5file[imname].value /255.0 
        shards = []

        # Collect the inputs for the image
        for shard in StepShingler(img, hstep=steps[1], vstep=steps[0], shingle_size=shingle_dims):
            if varthresh and np.var(shard) < varthresh:
                continue
            shard = np.expand_dims(shard,0)
            shards += [shard]
        shards = np.array(shards)
        print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
        sys.stdout.flush()

        # Predict the neural network and append the mean of features to overall imfeatures
        if len(shards)!=0:
            features = network.predict( shards, verbose=1 )
            imfeatures = np.concatenate( (imfeatures, np.expand_dims(features.mean(axis=0),0)) )
        else:
            imfeatures = np.concatenate( (imfeatures, np.zeros((1,4096))) )
        
    return imfeatures

## File formatting --------------------------
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
