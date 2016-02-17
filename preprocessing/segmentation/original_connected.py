import h5py
from scipy import ndimage
import matplotlib.pylab as plt
import numpy as np

# Connected Components
hdf5file='/fileserver/nmec-handwriting/flat_nmec_cropped_bin_uint8.hdf5'
flatnmec=h5py.File(hdf5file,'r')
flk = flatnmec.keys()
im = flatnmec[flk[10]]

def connectedcomponents( im ):
    im = im.value < 128
    return ndimage.label(im > 0.5)
    
print "Thresholding connected components"
for i in xrange(1,ccis[1]):
    if np.array(ccis[0]==i).sum() > 1000:
        ccs+=[i]