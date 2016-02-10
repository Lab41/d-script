import numpy as np
from scipy.fftpack import dct

# dct1d = np.expand_dims( np.linspace(1,56,56), 1 )
def dct2( patch ):
  return dct(dct(patch,axis=0),axis=1)
  
