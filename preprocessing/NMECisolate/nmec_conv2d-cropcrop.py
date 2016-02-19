import convolve_crop
import scipy
import scipy.misc
import h5py
import glob
import numpy as np
from PIL import Image
import os

imagenames = glob.glob('/fileserver/nmec-handwriting/stil-writing-corpus-processed/cropped_png/*.*')
#images = [ Image.open(imname).convert('L') for imname in imagenames ]

for im in imagenames:
    new_im = Image.open(im)
    head, tail = os.path.split(im)
    dest = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/discarded_cropped_png/'+tail+'.discard.png'
    if tail != 'FR-058-004.bin.crop.png' and not os.path.isfile(dest):
        imval = np.asarray(new_im.convert('L').getdata(), np.uint8).reshape(new_im.size[1], new_im.size[0])
        crop, i, discard = convolve_crop.create_cropped_np_arr_from_orig(imval)
        scipy.misc.imsave(dest, crop)