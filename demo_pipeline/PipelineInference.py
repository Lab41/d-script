import numpy as np
import h5py
import sys
import logging
sys.path.append('..')

# Neural network stuff
from fielutil import load_verbatimnet
from featextractor import extract_imfeats

# ### Parameters

# Do you want to load the features in? Or save them to a file?
load_features = False

# All the images that you require extraction should be in this HDF5 file
# hdf5images='icdar13data/benchmarking-processed/icdar_be.hdf5'
# hdf5images = 'icdar13data/experimental-processed/icdar13_ex.hdf5'
# hdf5images='nmecdata/nmec_scaled_flat.hdf5'
hdf5images='nmecdata/flat_nmec_bin_uint8.hdf5'

# This is the file that you will load the features from or save the features to
# featurefile = 'icdar13data/benchmarking-processed/icdar13be_fiel657.npy'
# featurefile = 'icdar13data/experimental-processed/icdar13ex_fiel657.npy'
# featurefile = 'nmecdata/nmec_bw_fiel657_features_steps5_thresh.0025.npy'
featurefile = 'nmecdata/nmec_bw_fiel657_features_steps5_thresh.15.npy'

# This is the neural networks and parameters you are deciding to use
paramsfile = '/fileserver/iam/iam-processed/models/fiel_657.hdf5'


# ### Full image HDF5 file
# 
# Each entry in the HDF5 file is a full image/form/document

labels = h5py.File(hdf5images).keys()


# ### Load feature extractor neural network
if not load_features:
   vnet = load_verbatimnet( 'fc7', paramsfile=paramsfile )
   vnet.compile(loss='mse', optimizer='sgd')


# ### Image features
# 
# Currently taken as averages of all shard features in the image. You can either load them or extract everything manually, depending on if you have the .npy array.

if load_features:
    print "Loading features in from "+featurefile
    imfeats = np.load(featurefile)
    print "Loaded features"
else:
    print "Begin extracting features from "+hdf5images
    imfeats = extract_imfeats( hdf5images, vnet, steps=(5,5), varthresh=0.15 )
    print h5py.File(hdf5images).keys()
    np.save( featurefile, imfeats )


# ### Build classifier

imfeats = ( imfeats.T / np.linalg.norm( imfeats, axis=1 ) ).T
F = imfeats.dot(imfeats.T)
np.fill_diagonal( F , -1 )


# ### Evaluate classifier on HDF5 file (ICDAR 2013)

# Top k (soft criteria)
k = 10
# Max top (hard criteria)
maxtop = 2
# Number of examples per image
g = 4

# Run through the adjacency matrix
softcorrect = 0
hardcorrect = 0
totalnum = 0
for j, i in enumerate(F):
    topk = i.argsort()[-k:]
    # Soft criteria
    if j/g in topk/g:
        softcorrect += 1
    totalnum +=1
    # Hard criteria
    hardcorrect+= sum([1 for jj in (j/g == topk[-maxtop:]/g) if jj])
    
# Print out results    
print "Top %d (soft criteria) = %f" %( k, (softcorrect+0.0) / totalnum )
print "Top %d (hard criteria) = %f" %( k, (hardcorrect+0.0) / totalnum / maxtop )

