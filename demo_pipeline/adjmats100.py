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
    
# Matrix representation of all features
F = np.zeros( (0, 128) )
A = np.zeros( (0, 128) )
fg = np.zeros( (1, 128) )
for i, auth in enumerate(authsfrags):
    fg[:] = 0
    for frag in authsfrags[auth]:
        f = authsfrags[auth][frag].value.mean(axis=0)
        f = f / np.linalg.norm(f)
        fg += f
        F = np.concatenate( (F, f ) )
    A = np.concatenate( (A, fg/4.0) )

# Adjacency matrices
def adjmat( A, B=None ):
    if B == None:
        B=A
    return A.dot(B.T)

# Difference matrices
def diffmat( A, B=None ):
    if not B:
        B = A
    diffmat = np.zeros( (len(A), len(B)) )
    for i,Ai in enumerate(A):
        for j, Bj in enumerate(B):
            diffmat[i,j] = np.linalg.norm(A[i] - B[j])
    return diffmat
            
# Compute adjacency matrices
AFT = adjmat( F, A )
FFT = adjmat( F )

# Do the nearest neighbor
np.fill_diagonal( FFT, 0 )  # don't cheat!
FFT = FFT.argsort(axis=1)/4+1 
AFT = AFT.argsort(axis=1)+1

# Top k for nearest neighbor
k = 5
softA = 0.0
softF = 0.0
hardA = 0.0
hardF = 0.0
for i in xrange(len(AFT)):
    # Soft criterion if query is in top k
    if (i/4+1) in FFT[i,-k:]:
        softF += 1
    if (i/4+1) in AFT[i,-k:]:
        softA += 1
    # Hard criterion determining how many returned are correct
    for j in xrange(3):
        if i/4+1 == FFT[i,-j-1]:
            hardF += 1
        if i/4+1 == AFT[i,-j-1]:
            hardA += 1

softA /= 1000
softF /= 1000
hardA /= 3000
hardF /= 3000

print "P/R & S/H results for top %d are: " %k
print "softavg=%f%%, softnn=%f%%, hardavg=%f%%, hardnn=%f%%" %(softA, softF, hardA, hardF)




