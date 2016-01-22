import numpy as np
import h5py
import sys
sys.path.append('../../d-script/')

# d-script imports
from class_icdar_iterator import *
from data_iters.minibatcher import MiniBatcher
from data_iters.iam_hdf5_iterator import IAM_MiniBatcher
from fielutil import verbatimnet, loadparams

# Shingle, horizontal, and vertical step sizes
ss = (56,56)
hs = 30
vs = 30

# Step 1: This is the filename of the HDF5 file with the original images (forms)
hdf5name='icdar13data/experimental-processed/icdar13_ex.hdf5'
hdf5name='icdar13data/benchmarking-processed/icdar_be.hdf5'

hdf5file=h5py.File(hdf5name)
print "Finished load of HDF5 file"

# Step 2: Load neural network in
vnet = verbatimnet('fc7')
loadparams( vnet, '/fileserver/iam/iam-processed/models/verbatimnet.hdf5' )
vnet.compile( loss='mse', optimizer='sgd' )
print "Compiled neural network up to FC7 layer"    

# Final output of neural network
imfeatures = np.zeros( (0,4096) )

# Step 3a: Loop through all the images in the HDF5 file
for imname in hdf5file.keys():
    img = 1.0 - hdf5file[imname].value /255.0 
    shards = np.zeros( (0, 1, 56, 56) )
    
    # Step 3b: Collect the inputs for the image
    for shard in StepShingler(img, hstep=hs, vstep=vs, shingle_size=ss):    
        shard = np.expand_dims(np.expand_dims(shard, 0),0)
        shards = np.concatenate( (shards, shard) )
    print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
    sys.stdout.flush()
    
    # Step 3c: Predict the neural network and append the mean of features to overall imfeatures
    features = vnet.predict( shards, verbose=1 )
    imfeatures = np.concatenate( (imfeatures, np.expand_dims(features.mean(axis=0),0)) )
