import h5py
import numpy as np
import matplotlib.pylab as plt

'''
 Analyzing the features extracted by Pat to create an adjacency matrix
'''

origfile = '/data/fs4/datasets/icdar13/benchmarking-processed/author_icdar_be.hdf5'

featfile = '/data/fs4/datasets/icdar13/benchmarking-processed/fiel_feat_icdar13.hdf5'
# featfile = '/data/fs4/datasets/icdar13/benchmarking-processed/fiel_feat_icdar13_TH0.2.hdf5'

feats = h5py.File(featfile,'r')
origs = h5py.File(origfile,'r')

auths = feats['authors']
authsfrags = feats['fragments']

# Matrix representation of all author features
A = np.zeros( (0, 128) )
for auth in auths:
    a = auths[auth] / np.linalg.norm(auths[auth])
    A = np.concatenate( (A, auths[auth]) )

# Matrix representation of all features
F = np.zeros( (0, 128) )
for auth in authsfrags:
    for frag in authsfrags[auth]:
        f = authsfrags[auth][frag] / np.linalg.norm(authsfrags[auth][frag])
        F = np.concatenate( (F, f ) )

# Adjacency matrices
AAT = A.dot(A.T)
FFT = F.dot(F.T)

# Leave one out cross-validation with average author feature
diffa = np.zeros((1000,250))
softkA = []
nA = np.array( [ f / np.linalg.norm(f) for f in A ])
k = 1
for i, f in enumerate(F):
    nf = f / np.linalg.norm(f)
    # corra[i] = f.dot( nA.T )
    diffa[i] = np.power( nf - nA, 2 ).sum(axis=1)
    topk = diffa[i].argsort()[:k]+1
    softkA.append( (i/4+1) in topk )
numcorrectA = np.array(softkA).astype(int).sum()
