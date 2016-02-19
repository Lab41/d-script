import convolve_crop
import scipy
import scipy.misc
import h5py

nmecdata = h5py.File('nmecdata/flat_nmec_bin_uint8.hdf5')

for im in nmecdata.keys():
    imval = nmecdata[im].value
    crop, i, discard = convolve_crop.create_cropped_np_arr_from_orig(imval)
    scipy.misc.imsave('/fileserver/nmec-handwriting/stil-writing-corpus-processed/cropped_png2/'+im+'.convcrop.png', crop)