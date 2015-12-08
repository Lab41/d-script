from PIL import Image
import numpy
import glob
from os import listdir
import matplotlib.pylab as plt

benchmark='/fileserver/icdar13/benchmarking/'
evaluation='/fileserver/icdar13/experimental/'

benchfiles = glob.glob(benchmark+'*.tif')
evalfiles = glob.glob(evaluation+'*.tif')

def readtif(imname):
    im = Image.open(imname)
    return numpy.array( im.getdata(), numpy.uint8).reshape(im.size[1], im.size[0])

im = readtif(benchfiles[0])
