import time
import random
import numpy as np
from collections import defaultdict
from optparse import OptionParser
import pickle
import scipy.misc as smi
from PIL import Image
import sys
import os

# Required libraries
import h5py
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical
from keras.layers.normalization import BatchNormalization as BN

import matplotlib.pylab as plt

import sys
sys.path.append('../')
# d-script imports
import data_iters
from data_iters.hdf5_iterator import Hdf5MiniBatcher
from data_iters.archive.iam_iterator import IAM_MiniBatcher
from data_iters.minibatcher import MiniBatcher
from viz_tools.array_to_png import get_png_from_array, display_img_array
from denoiser.noisenet import conv4p56_model, conv4p120_model, conv3p_model, conv2p_model, conv2_model

shingle_dim = (56,56)
write2hdf5 = True
write2png = False
visualize = False
overlap=10

# hdf5ims = h5py.File('/fileserver/nmec-handwriting/nmec_scaled_flat.hdf5','r')
hdf5ims = h5py.File('/fileserver/nmec-handwriting/flat_nmec_bin_uint8.hdf5','r')
outdir = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/denoised56/'
acoh = 'nmec_author_clean56_overlap10.hdf5'
fcoh = 'nmec_flat_clean56_overlap10.hdf5'

def im2bw(origim, thr=0.8):
    immin = origim.min()
    immax = origim.max()
    imthresh = thr*(immax - immin)+immin
    return origim < imthresh

def create_input_buffer( im, input_shape=(None,1,56,56), topbot_overlap = 0 ):
    input_buffer = []
    for i in xrange(0, im.shape[0] - input_shape[2] + 1, input_shape[2] - topbot_overlap*2 ):
        for j in xrange(0, im.shape[1] - input_shape[3] + 1, input_shape[3] - topbot_overlap*2 ):
            input_buffer += [im[i:i+input_shape[2], j:j+input_shape[3]]]
    return input_buffer

def create_output_im( output_buffer, im, input_shape=(None,1,56,56), topbot_overlap = 0 ):
 
    output_im = np.zeros(im.shape)
    shapesize = (input_shape[2], input_shape[3])
    
    k=0
    # Rearrange the output to form an image
    for i in xrange(0, im.shape[0] - input_shape[2] + 1, input_shape[2] - topbot_overlap*2):
        for j in xrange(0, im.shape[1] - input_shape[3] + 1, input_shape[3]-topbot_overlap*2):
            output_im[i:i+input_shape[2],j:j+input_shape[3]] = output_buffer[k].reshape(shapesize)
            k+=1
            
    return output_im

if write2hdf5:
    a_out = h5py.File(acoh,'w')
    f_out = h5py.File(fcoh,'w')
    author_groups = {}

thedir = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/denoised56'
files = os.listdir(thedir)
for imhdf5 in files:
    
    output_im = np.array(Image.open(thedir+'/'+imhdf5))
    the_author = imhdf5.split('-')[1]
        
    # Write image to HDF5 file
    if write2hdf5:
        if not author_groups.has_key(the_author):
            author_groups[the_author] = a_out.create_group(the_author)
        author_groups[the_author].create_dataset( imhdf5, data=output_im.astype(np.uint8) )
        data_group = f_out.create_dataset( imhdf5, data=output_im.astype(np.uint8) )
    if write2png:
        smi.imsave(outdir+imhdf5, output_im)

if write2hdf5:
    a_out.close()


