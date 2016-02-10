import h5py
import numpy as np
import matplotlib.pylab as plt
import networkx

'''
 Analyzing the features extracted by Pat to create an adjacency matrix
'''

datapath = '/fileserver'
datapath = '/data/fs4/datasets'
featfile = datapath+'/icdar13/benchmarking-processed/fiel_feat_icdar13_100shingles.hdf5'

feats = h5py.File(featfile,'r')
authsfrags = feats['fragments']

def hold50thout( authsfrags ):
    # Matrix representation of all features
    F = np.zeros( (0, 128) )
    A = np.zeros( (0, 128) )
    fg = np.zeros( (1, 128) )
    f = np.zeros( (1,128) )
    j = 0
    for i, auth in enumerate(authsfrags):
        fg[:] = 0
        scalefactor = 4.0
        for frag in authsfrags[auth]:
            if (j % 50)==0:
                scalefactor = 3.0
                f[:] = 0.0
                print frag + " is not in the list"
            else:
                f = authsfrags[auth][frag].value.mean(axis=0)
                f = f / np.linalg.norm(f)
            F = np.concatenate( (F, f) )
            fg += f
            j+=1
        A = np.concatenate( (A, fg/scalefactor) )
    return A

def getfeat( featname ):
    authname=featname[:3]
    imfeat = authsfrags[authname][featname].value.mean(axis=0)
    return imfeat

def nnclass( model, imfeat ):

    A = np.load(model)
    imfeat = imfeat / np.linalg.norm(imfeat)
    confidence = A.dot( imfeat.T ).squeeze()

    arglist = confidence.argsort()[::-1]
    confidence.sort()
    confidence = confidence[::-1]
    return arglist, confidence


