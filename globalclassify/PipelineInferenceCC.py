#!/usr/bin/env python 
import os
import sys
import numpy as np
import h5py
import logging
sys.path.append('..')

# Neural network stuff
from fielutil import load_verbatimnet, load_denoisenet, patnet_layers, loadparams
from featextractor import extract_imfeats
import preprocessing.segmentation.original_connected as original_connected
from preprocessing.segmentation.original_connected import cc_shingler, pad_shingle_top, put_in_shingle, get_shingle_info

### Parameters
# Do you want to load the features in? Or save them to a file?
load_features = False

# All the images that you require extraction should be in this HDF5 file
# hdf5images='icdar13data/benchmarking-processed/icdar_be.hdf5'
# hdf5images = 'icdar13data/experimental-processed/icdar13_ex.hdf5'
# hdf5images='nmecdata/nmec_scaled_flat.hdf5'
# hdf5images='nmecdata/flat_nmec_bin_uint8.hdf5'
hdf5images='/fileserver/nmec-handwriting/flat_nmec_cropped_bin_uint8.hdf5'
hdf5base=os.path.basename(hdf5images)

# This is the file that you will load the features from or save the features to
featurefile = '/fileserver/nmec-handwriting/globalfeatures/nmec_bw_crop.deNNam_fiel657.steps5_mean250.hdf5'
outdir='/fileserver/nmec-handwriting/localfeatures/nmec_bw_crop.deNNiam_fiel657.steps5_mean250/'
components_outpath='/work/d-script/nmec_ccs.hdf5'
features_outpath='/fileserver/nmec-handwriting/localfeatures/nmec_clean56_overlap10_patnet.npy'

# This points to the neural networks and saved weights
paramsfile = '/work/d-script/weights/patnet-iam-480.hdf5'


### Full image HDF5 file
# Each entry in the HDF5 file is a full image/form/document
# labels = h5py.File(hdf5images).keys()


# ### Load feature extractor neural network
print "Making patnet"
if not load_features:
    patnet = patnet_layers(None, (1, 56, 56))
    patnet.compile(loss='mse', optimizer='sgd')

    

### Already extracted features for each document?
# If saved, then use saved feature vectors, otherwise, run extractor
if load_features:
    print "Loading features in from "+featurefile
    imfeats = np.load(featurefile)
    print "Loaded features"
else:
    print "Begin extracting features from "+hdf5images
    feat_size = 150
    with h5py.File(hdf5images, "r") as flat_images:
        num_docs = len(flat_images)
        
        imfeats = np.zeros((num_docs, feat_size))
        for img_index, (img_id, img) in enumerate(flat_images.iteritems()):
            print "Getting components for {}".format(img_id)
            # get components
            try:
                with h5py.File(components_outpath, "r") as get_ccs:
                    img_path = "{}/{}".format(hdf5base, img_id)
                    cnxd_components = [ cc[()] for cc in get_ccs[img_path].itervalues() ]
            except (IOError, KeyError):
                # extract connected components
                cnxd_components, cc_infos = cc_shingler(img)
            # save components
            if components_outpath:
                with h5py.File(components_outpath, "a") as out_ccs:
                    num_components = len(cnxd_components)
                    cnxd_components = sorted(cnxd_components, key=lambda x: np.prod(x.shape))
                    for component_i, component in enumerate(cnxd_components):
                        component_path = "{}/{}/{}".format(hdf5base, img_id, component_i)
                        try:
                            out_ccs.require_dataset(component_path, 
                                                    shape=component.shape, 
                                                    dtype=component.dtype, 
                                                    data=component)
                        except TypeError:
                            del out_ccs[component_path]
                            out_ccs.create_dataset(component_path, data=component)
    
            # transform, normalize, and put components in evenly sized things
            component_shingles = cnxd_components[:]
            # extract features from components
            doc_features = []
            print "{}: Extracting for {}".format(img_index, img_id)
            for shin_i, shingle in enumerate(component_shingles):
                
                shingle_info = get_shingle_info(shingle)
                translate_coords = (23-int(shingle_info.center_x), 23-int(shingle_info.center_y))
                #print "New center: ", translate_coords
                #print "Shape: ", shingle.shape
                try:
                    shingle=put_in_shingle(shingle, (56,56), pad_value=255, paste_location=translate_coords)
                except ValueError as e:
                    if "Blank shingle" in e:
                        continue
                shingle=1 - shingle/255.
                shingle=shingle.reshape(1, 1, 56, 56)
                #print shin_i,
                shingle_features = patnet.predict(shingle, verbose=0)
                doc_features.append(shingle_features)
            
            doc_feature_vector = np.mean(doc_features, axis=0)
            print "Norm of feature vector: ", np.linalg.norm(doc_feature_vector)
            imfeats[img_index, :] = doc_feature_vector
            
    np.save(features_outpath, imfeats)
                


# ### Build classifier
# nearest-neighbors: compute a num_imgs x num_imgs adjacency matrix
# based on the distance of each feature vector (row) from every other
imfeats = ( imfeats.T / np.linalg.norm( imfeats, axis=1 ) ).T
F = imfeats.dot(imfeats.T)
# do not compare with self
np.fill_diagonal( F , -1 )


### Evaluate classifier on HDF5 file (ICDAR 2013)
# Top k (soft criteria)
# Is an image from the same author in the top k returned for a query?
k = 10
# Max top (hard criteria)
# Are the top few results for a query all from the correct author?
maxtop = 3
assert maxtop < k, "Hard criterion way too hard"
# Number of examples per image
# [PRC: Does this correspond to number of documents per author?]
g = 8
assert maxtop < g

# Run through the adjacency matrix
softcorrect = 0
hardcorrect = 0
totalnum = 0
for j, similarity_vector in enumerate(F):
    topk = similarity_vector.argsort()[-k:]
    # Soft criterion
    author_truth = j/g
    author_predicted = topk/g
    if author_truth in author_predicted:
        softcorrect += 1
    totalnum +=1
    # Hard criterion
    top_predictions = (author_truth == author_predicted[-maxtop:])
    if all(top_predictions):
        hardcorrect += 1
    
# Print out results    
print "Top %d (soft criteria) = %f" %( k, (softcorrect+0.0) / totalnum )
print "Top %d (hard criteria) = %f" %( k, (hardcorrect+0.0) / totalnum / maxtop )

