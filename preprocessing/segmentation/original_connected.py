#!/usr/bin/env python

from collections import namedtuple

import h5py
from scipy import ndimage
import matplotlib.pylab as plt
import numpy as np
import pdb
import sys

sys.path.append('../..')
print sys.path

# d-script imports
from globalclassify.fielutil import load_verbatimnet
from denoiser.noisenet import conv4p_model

#from globalclassify.featextractor import load_verbatimnet, load_denoisenet

ShingleInfo=namedtuple('ShingleInfo', ['area',
                                       'aspect_ratio', 
                                       'sum_black', 
                                       'ink_ratio', 
                                       'width', 
                                       'height',
                                       'center_x',
                                       'center_y'])



def connectedcomponents( im, cutoff=128 ):
    ''' Find connected components of value above cutoff
    in image '''
    im = im[()] < cutoff
    return ndimage.label(im > 0.5)

def boundingboxcc(ccis, cc_index, as_slices=False):
    ''' Find bunding box around connected component
    by rowwise and colwise zerofinding'''
    cc = ccis==cc_index
    cols=np.any(cc, axis=0)
    rows=np.any(cc, axis=1)

    nonzero_cols=np.nonzero(cols)
    left=np.min(nonzero_cols)
    right=np.max(nonzero_cols)
    nonzero_rows=np.nonzero(rows)
    top=np.min(nonzero_rows)
    bottom=np.max(nonzero_rows)
    if as_slices:
        return slice(top, bottom),slice(left, right)
    else:
        return top, bottom, left, right

def show_patch(cc):
    ''' Visualize an image patch with summary statistics
    '''
    shingle_stats = get_shingle_info(cc)
    patch_info='''w={width},h={height}\narea={area}\nar={aspect_ratio:0.3f}\nink_ratio={ink_ratio}\nsum0={sum_black:.0f}
    cog={center_x:.1f},{center_y:.1f}'''.format(**shingle_stats.__dict__)
    ax=plt.gca()
    ax.imshow(cc, cmap='gray')
    ax.scatter(shingle_stats.center_x, shingle_stats.center_y, color='red')
    tx, ty = 0.75 * np.diff(ax.get_xlim()) + ax.get_xlim()[0], \
             1.1 * np.diff(ax.get_ylim()) + ax.get_ylim()[0]
    ax.text(tx, ty, patch_info, ha='right')

def get_shingle_info(shingle):
    ''' Generate summary statistics for an image, including dimensions,
    area, center of gravity, etc. 
    
    Returns ShingleInfo namedtuple instance'''
    area=area=np.prod(shingle.shape)
    try:
        ar=float(shingle.shape[1])/float(shingle.shape[0])
    except ZeroDivisionError:
        ar=np.inf
    sum0=np.sum(shingle)
    center_x=np.sum(np.arange(shingle.shape[1]) * np.sum(shingle, axis=0))/np.sum(shingle)
    center_y=np.sum(np.arange(shingle.shape[0]) * np.sum(shingle, axis=1))/np.sum(shingle)
    return ShingleInfo(area=area, 
                       aspect_ratio=ar, 
                       sum_black=sum0, 
                       ink_ratio=np.log(sum0/area), 
                       width=shingle.shape[1],
                       height=shingle.shape[0],
                       center_x=center_x,
                       center_y=center_y)

def cc_shingler(img):
    ''' Extract connected components from a shingle
    
    Returns a 2-tuple with:
        - a list of numpy arrays holding connected components extracted from
        img
        - a list with summary statistics about each shingle'''
    connected_component_indices, num_components = connectedcomponents(img)
    connected_components = []
    component_info = []
    for cc_index in range(num_components):
        cc_slice = boundingboxcc(connected_component_indices, cc_index, as_slices=True)
        cc_shingle = img[cc_slice]
        # normalize
        shingle_stats = get_shingle_info(cc_shingle)
        # prune
        if shingle_stats.area > 250 and \
            shingle_stats.aspect_ratio < 4 and \
            shingle_stats.area < 10000:
                connected_components.append(cc_shingle)
                component_info.append(shingle_stats)
    return connected_components, component_info

def pad_shingle_top(shingle, midline_target=0.75):
    ''' Zero-pad the top of shingle so that the row-wise center of gravity is 
    at or below a predetermined proportion of the number of rows.'''
    
    shingle_info=get_shingle_info(shingle)
    rows_to_add=int(midline_target * shingle.shape[0] - shingle_info.center_y)
    print rows_to_add
    if rows_to_add > 0:
        new_shingle = np.concatenate((np.zeros((rows_to_add,shingle.shape[1])),
                                      shingle))
        return new_shingle
    return shingle
    
def put_in_shingle(img, shingle_size, pad_value=0., paste_location=None):
    ''' Put input image into an array of a certain size, clipping
    and padding where necessary '''
    shingle = np.ones(shingle_size,dtype=np.float32) * pad_value
    if paste_location is None:
        paste_location = (0,0)
    # assume that paste_location is the upper lefthand corner
    # haven't done the math otherwise
    assert paste_location == (0,0)
    img_slice=(slice(0,np.min((shingle_size[0], img.shape[0]))), slice(0,np.min((shingle_size[1], img.shape[1]))))
    shingle_slice=img_slice
    shingle[shingle_slice] = img[img_slice]
    return shingle


def extract_features_for_corpus(hdf5group, feature_extractor, shingle_dim, transform=None):
    ''' Returns a dictionary of features for each dataset in an hdf5 file/group object,
    with options for transformation. 
    
    Uses shingles over connected components for fewer, less noisy inputs.
    
    Arguments:
    hdf5group -- HDF5 File/Group object
    feature_extractor -- function/callable that outputs a numpy array of features
    shingle_dim -- (rows,cols) for size of shingles to generate for inference
    transform -- optional functional/callable with one argument, should output a numpy array the same size as its input
    '''


    imfeatures = {}
    # Loop through all the images in the HDF5 file
    for imname in hdf5group:
        img = hdf5group[imname][()]
        
        shards = []
        
        connected_components, cc_info = cc_shingler(img)
        shingle_candidates=[put_in_shingle(cc, shingle_size=shingle_dim) for cc in connected_components]
        # Collect the inputs for the image
        for shard in shingle_candidates:
            shard = np.expand_dims(np.expand_dims(shard, 0), 0)
            if transform is not None:
                shard = transform(shard)
            shards.append(shard)
            
        shards_array = np.concatenate(shards)
        
        print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
        sys.stdout.flush()

        # Predict the neural network and add the shingle-wise mean across features to feature hash
        features = feature_extractor(shards_array)
        feature=np.expand_dims(features.mean(axis=0),0)
        imfeatures[imname] = features

    return imfeatures

def main():
    """ Process NMEC with precompiled denoiser and Fielnet
    """
    def denoising_func(x):
        orig_shape = x.shape

        x = 1. - x/255.
        x = denoiser.predict(x, verbose=0)
        x = x.reshape(orig_shape)
        return x
        
    try:
        featext  = load_verbatimnet('fc7', paramsfile='/fileserver/iam/iam-processed/models/fiel_657.hdf5')
        featext.compile(loss='mse', optimizer='sgd')
        featext_func = lambda x: featext.predict(x, verbose=0.0)
        print "Making the denoiser"
        denoiser = conv4p_model()
        denoiser.load_weights('/fileserver/iam/models/conv4p_linet56-iambin-tifs.hdf5')
        hdf5file='/fileserver/nmec-handwriting/flat_nmec_bin_uint8.hdf5'
        
        with h5py.File(hdf5file, "r") as data_file:
            features = extract_features_for_corpus(data_file,featext_func,shingle_dim=(56,56),transform=denoising_func)
        with h5py.File("output_features.hdf5", "w") as feature_file:
            for document_id, document_features in features.iteritems():
                feature_file.create_dataset(document_id, data=document_features)
    except Exception as e:
        print e
        pdb.post_mortem()
    
    
def demo():
    ''' Some pretty plots from the connected component finder '''
    # Connected Components
    hdf5file='/fileserver/nmec-handwriting/flat_nmec_bin_uint8.hdf5'
    flatnmec=h5py.File(hdf5file,'r')
    flk = flatnmec.keys()
    im = flatnmec[flk[10]]

    ccs, cc_info = cc_shingler(flatnmec[imname])
    
    print len(ccs), "components found"
    for shingle, area in sorted(zip(ccs, cc_info), key=lambda x: -x[1].width):
        # pad top adaptively
        new_shingle = pad_shingle_top(shingle)
        # also pad left a bit
        new_shingle = np.concatenate((np.zeros((new_shingle.shape[0], 5)), new_shingle), axis=1)
        plt.figure(figsize=(6,3))
        plt.subplot(1,2,1)
        show_patch(new_shingle)
        plt.subplot(1,2,2)
        square_shingle=put_in_shingle(new_shingle, shingle_size=(56,56))
        show_patch(square_shingle)
        plt.show()

if __name__=="__main__":
    main()