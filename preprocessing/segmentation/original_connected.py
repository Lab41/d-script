#!/usr/bin/env python

from collections import namedtuple
from itertools import izip
import logging
import time
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


# getter function for Hdf5 iterators
def connected_component_getter(f, key, shingle_dim,
                        rng=None,
                        fill_value=255,
                        cutoff_value=128,
                        preprocess_doc=None,
                        postprocess=None,
                        add_rotation=False,
                        stdev_threshold=None,
                        hdf5_output_path=None):
    if hdf5_output_path is None:
        hdf5_output_path = "/work/cc_features.hdf5"
    author,fragment = key
    key_flat = "{}_{}".format(*key)
    query_img = f[author][fragment][()]
    
    assert stdev_threshold is None
    assert add_rotation==False
    
    with h5py.File(hdf5_output_path, "a") as components:
        # extract components from document if necessary
        if f.filename not in components:
            components.create_group(f.filename)
        corpus_components_hash = components[f.filename]
        # check for this document in corpus or that the corpus was improperly written
        if key_flat not in corpus_components_hash or \
                any([len(cc.attrs)==0 for cc in corpus_components_hash[key_flat].itervalues()]):
            # Preprocess document and shingle (does not offer rng as an argument)
            if preprocess_doc is not None:
                query_img=preprocess_doc(query_img)
            # erase any previous extraction work for this document
            try:
                del corpus_components_hash[key_flat]
            except KeyError:
                pass
            corpus_components_hash.create_group(key_flat)

            # add component info as attributes
            ccomponents, ccinfos = cc_shingler(query_img, fill_value=fill_value, cutoff=cutoff)
            for component_index, (component, info) in enumerate(izip(ccomponents,ccinfos)):
                component_index=str(component_index)
                corpus_components_hash[key_flat].create_dataset(component_index, data=component)  
                for attr_name, attr_val in info._asdict().iteritems():
                    corpus_components_hash[key_flat][component_index].attrs[attr_name] = attr_val
        document_components=corpus_components_hash[key_flat]
        component_keys=document_components.keys()
        # loop until success
        for j in range(10000):
            # pick a random component
            cc_key=rng.choice(component_keys)
            cc_element=document_components[cc_key]

            # fiddle
            cc_element=pad_shingle_top(cc_element, 0.75, pad_value=255)
            
            # try to put it in a shingle (can fail)
            for i in range(10000):
                x_lim = max(1, shingle_dim[1] - cc_element.shape[1])
                y_lim = max(1, shingle_dim[0] - cc_element.shape[0])
                new_location=(rng.randint(x_lim), rng.randint(y_lim)) 
                try:
                    cc_element=put_in_shingle(cc_element, shingle_dim, pad_value=fill_value,
                                     paste_location=new_location)
                except ValueError as e:
                    if str(e)=="Blank shingle":
                        logger = logging.getLogger(__name__)
                        logging.debug("Blank shingle")
                        continue
                    else:
                        raise
                break
            #check that the component was successfully put in a shingle
            if cc_element.shape!=shingle_dim:
                continue
            else:
                break
            
    if postprocess is not None:
        cc_element=postprocess(cc_element, rng=rng)
    
    return cc_element


ShingleInfo=namedtuple('ShingleInfo', ['area',
                                       'aspect_ratio', 
                                       'sum_black', 
                                       'ink_ratio', 
                                       'width', 
                                       'height',
                                       'center_x',
                                       'center_y'])



def connectedcomponents( im, cutoff=128 ):
    ''' Find connected components of value below cutoff
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

def cc_shingler(img, mask=True, fill_value=255, cutoff=128):
    ''' Extract connected components from a shingle
    
    Arguments:
    img -- ndarray-like, extract connected components from this
    mask -- if false, returned connected components are clipped from img using
        bounding boxes and may contain pixels that are not part of the component; if true,
        returned connected components contain only pixels that form part of the component
    fill_value -- if mask is True, out-of-component positions will be filled with this
    cutoff -- values lower than this will be considered candidates for connection
    
    Returns a 2-tuple with:
        - a list of numpy arrays holding connected components extracted from
        img
        - a list with summary statistics about each shingle'''
    connected_component_indices, num_components = connectedcomponents(img, cutoff=cutoff)
    connected_components = []
    component_info = []
    for cc_index in range(num_components):
        cc_slice = boundingboxcc(connected_component_indices, cc_index, as_slices=True)
        cc_shingle = img[cc_slice]
        # mask if needed
        if mask:
            cc_mask = connected_component_indices[cc_slice]==cc_index
            cc_inv_mask = (-cc_mask).astype(cc_shingle.dtype)
            cc_mask = cc_mask.astype(cc_shingle.dtype)
            # combine masked and transformed blank space with passed-through component
            cc_shingle = cc_inv_mask * fill_value + \
                         cc_mask * cc_shingle
        # get info
        shingle_stats = get_shingle_info(cc_shingle)
        # prune
        if shingle_stats.area > 250 and \
            shingle_stats.aspect_ratio < 4 and \
            shingle_stats.aspect_ratio > 0.25 and \
            shingle_stats.area < 10000:
                connected_components.append(cc_shingle)
                component_info.append(shingle_stats)
    return connected_components, component_info

def pad_shingle_top(shingle, midline_target=0.75, pad_value=0.):
    ''' Zero-pad the top of shingle so that the row-wise center of gravity is 
    at or below a predetermined proportion of the number of rows.'''
    shingle_info=get_shingle_info(shingle)
    rows_to_add=int(midline_target * shingle.shape[0] - shingle_info.center_y)
    if rows_to_add > 0:
        new_shingle = np.concatenate((np.ones((rows_to_add,shingle.shape[1])) * pad_value,
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
    #assert paste_location == (0,0)
        
    paste_x, paste_y = paste_location
    img_height, img_width = img.shape
    shingle_height, shingle_width = shingle_size
    img_left, img_right = \
        sorted((0 if paste_x >= 0 else -paste_x,
               img_width if paste_x + img_width <= shingle_width
                   else (shingle_width - paste_x) % img_width))
    img_top, img_bottom = \
        sorted((0 if paste_y >= 0 else -paste_y,
               img_height if paste_y + img_height <= shingle_height
                   else (shingle_height - paste_y) % img_height))
        
    shingle_left, shingle_right = \
        sorted((paste_x if paste_x > 0 else 0,
               paste_x + img_width if paste_x + img_width < shingle_width
                   else shingle_width))
    shingle_top, shingle_bottom = \
        sorted((paste_y if paste_y > 0 else 0,
               paste_y + img_height if paste_y + img_height < shingle_height
                   else shingle_height))
   
    img_slice=(slice(img_top,img_bottom), slice(img_left,img_right))
    shingle_slice=(slice(shingle_top,shingle_bottom), slice(shingle_left,shingle_right))

    if not (img[img_slice] != pad_value).any():
        # aint got nothing in it
        raise ValueError("Blank shingle")
        
    shingle[shingle_slice] = img[img_slice]

    return shingle


def extract_features_for_corpus(hdf5group, outputhdf5, feature_extractor, shingle_dim, transform=None):
    ''' Returns a dictionary of features for each dataset in an hdf5 file/group object,
    with options for transformation. 
    
    Uses shingles over connected components for fewer, less noisy inputs.
    
    Arguments:
    hdf5group -- HDF5 File/Group object
    outputhdf5 -- None or HDF5 Group/File object, for saving generated features
    feature_extractor -- function/callable that outputs a numpy array of features
    shingle_dim -- (rows,cols) for size of shingles to generate for inference
    transform -- optional functional/callable with one argument, should output a numpy array the same size as its input
    
    Returns
    a dictionary if outputhdf5 is None, otherwise a pointer to the HDF5 object that was passed in as outputhdf5
    '''
    
    if outputhdf5 is None:
        imfeatures = {}
    else:
        imfeatures = outputhdf5
    # Loop through all the images in the HDF5 file
    t_start = time.time()
    for imname in hdf5group:
        img = hdf5group[imname][()]


        shards = []
        t1 = time.time()
        connected_components, cc_info = cc_shingler(img)
        t2 = time.time()
        print "Extracted CCs in {}".format(t2-t1)
        shingle_candidates=[put_in_shingle(cc, shingle_size=shingle_dim) for cc in connected_components]
        t3 = time.time()
        print "Made uniform shingles in {}".format(t3-t2)
        # Collect the inputs for the image
        for shard in shingle_candidates:
            shard = np.expand_dims(np.expand_dims(shard, 0), 0)
            if transform is not None:
                shard = transform(shard)
            shards.append(shard)
        t4 = time.time()  
        print "Trasnformed shingles in {}".format(t4-t3)

        if len(shards) > 0:
            shards_array = np.concatenate(shards)

            print "Loaded %d shards in and predicting on image %s" %(len(shards), imname)
            sys.stdout.flush()

            # Predict the neural network and add the shingle-wise mean across features to feature hash
            features = feature_extractor(shards_array)
            feature=np.expand_dims(features.mean(axis=0),0)
            t5 = time.time()
            print "Generated features in {}".format(t5-t4)
            if outputhdf5:
                imfeatures.create_dataset(imname,data=features)
            else:
                imfeatures[imname] = features

        else:
            imfeatures[imname] = []

    t_end = time.time()
    print "Total time: {}".format(t_end-t_start)
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
        
        with h5py.File("/work/output_features.hdf5", "w") as feature_file:
            with h5py.File(hdf5file, "r") as data_file:
                features = extract_features_for_corpus(data_file,feature_file,
                                                       featext_func,shingle_dim=(56,56),
                                                       transform=denoising_func)
        
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
