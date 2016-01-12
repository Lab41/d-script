import h5py
import numpy as np
import matplotlib.pylab as plt
import networkx

'''
 Analyzing the features extracted by Pat to create an adjacency matrix
'''

datapath = '/fileserver'
datapath = '/data/fs4/datasets'
origfile = datapath+ '/icdar13/benchmarking-processed/author_icdar_be.hdf5'
featfile = datapath+ '/icdar13/benchmarking-processed/fiel_feat_icdar13.hdf5'
# featfile = datapath+ '/icdar13/benchmarking-processed/fiel_feat_icdar13_TH0.2.hdf5'
featfile = datapath+'/icdar13/benchmarking-processed/fiel_feat_icdar13_100shingles.hdf5'

feats = h5py.File(featfile,'r')
origs = h5py.File(origfile,'r')

auths = feats['authors']
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
def adjmat( M ):
    return M.dot(M.T)

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
AFT = adjmat( A, F )
FFT = adjmat( F )

# 
np.fill_diagonal( FFT, 0 )
FFT = FFT.argsort(axis=1)/4+1















docsperauth = 2
if docsperauth == 2:
    AA1 = F[0::4]
    AA2 = F[1::4]
    F = np.zeros( (len(AA1)+len(AA2), 128 ) )
    F[::2] = AA1
    F[1::2] = AA2


# Leave one out cross-validation with average author feature for top k authors
print "Cross validation from feature to authors"
# diffa = np.zeros((1000,999))
softkA = []
softkAc= []
softkF = []
k = 10
nA = np.zeros( (len(A),128) )
na = np.zeros( 128 )
for i, f in enumerate(F):
    nF = np.concatenate( (F[:i], np.zeros((1,128)), F[i+1:]) )
    
    # Author matrix creation
    na[:] = 0
    scalefactor = docsperauth + 0.0
    for j in xrange(len(nF)):
        na += nF[j]
        if i == j:
            scalefactor= docsperauth - 1.0
        if (j+1) % docsperauth:
            nA[ j/docsperauth ] = na / scalefactor
            na[:] = 0
            scalefactor= docsperauth + 0.0
            
    corrF = f.dot( nF.T )
    corrA = f.dot( nA.T )
    corrAc = f.dot( A.T )
    
    # diffa[i] = np.power( f - A, 2 ).sum(axis=1)
    topkF = corrF.argsort()[-k:]
    topkA = corrA.argsort()[-k:]
    topkAc = corrAc.argsort()[-k:]
    softkA.append( (i/docsperauth+1) in (topkA+1) )
    softkF.append( (i/docsperauth+1) in (topkF/docsperauth+1) )
    softkAc.append((i/docsperauth+1) in (topkAc/docsperauth+1) )
    
numcorrectA = np.array(softkA).astype(int).sum()
numcorrectAc= np.array(softkAc).astype(int).sum()
numcorrectF = np.array(softkF).astype(int).sum()

print "Percent in the top %d is %f, averaged author" %( k, float(numcorrectA)/len(F)*100 )
print "Percent in the top %d is %f, cheated averaged author" %( k, float(numcorrectA)/len(F)*100 )
print "Percent in the top %d is %f, full nearest neighbor" %( k, float(numcorrectF)/len(F)*100 )

# Greek or not?


       
# G = networkx.from_numpy_matrix(FFT) 
# networkx.draw(G)
# plt.show()
