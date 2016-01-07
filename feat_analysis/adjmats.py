import h5py
import numpy as np
import matplotlib.pylab as plt
import networkx

'''
 Analyzing the features extracted by Pat to create an adjacency matrix
'''

def get_features(datapath):
    origfile = datapath+ '/icdar13/benchmarking-processed/author_icdar_be.hdf5'
    featfile = datapath+ '/icdar13/benchmarking-processed/fiel_feat_icdar13.hdf5'
    # featfile = datapath+ '/icdar13/benchmarking-processed/fiel_feat_icdar13_TH0.2.hdf5'

    feats = h5py.File(featfile,'r')
    origs = h5py.File(origfile,'r')

    auths = feats['authors']
    authsfrags = feats['fragments']

    # Matrix representation of all author features
    A = np.zeros( (0, 128) )
    for auth in auths:
        a = auths[auth] / np.linalg.norm(auths[auth])
        A = np.concatenate( (A, a) )
        
    # Matrix representation of all features
    F = np.zeros( (0, 128) )
    for auth in authsfrags:
        for frag in authsfrags[auth]:
            f = authsfrags[auth][frag] / np.linalg.norm(authsfrags[auth][frag])
            F = np.concatenate( (F, f ) )
    return A, F

# Enrich square matrix with file id's etc, write to HDF5
# The below functions get ICDAR13 ID's from indices into a 
# list where authors are continuously nubmered and each have four
# documents, e.g. the benchmarking dataset
def get_author_id(i):
    author_id = "{0:03}".format(1+ (i/4))
    return author_id

def get_fragment_id(i):
    file_id = 1 + (i % 4)
    return file_id

def get_full_id(i):
    full_id = "{0}_{1}.tif".format(get_author_id(i), get_fragment_id(i))
    return full_id

def reverse_full_id(full_id):
    author_id, file_id = full_id.split(".")[0].split("_")
    author_int = int(author_id)
    file_int = int(file_id)
    return 4*(author_int - 1) + (file_int - 1)

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
           
def demo(A,F): 
    print "Computing adjacency matrices"
    AAT = adjmat( A )
    FFT = adjmat( F )
    print "Computing difference matrices"
    dA = diffmat( A )
    dF = diffmat( F )

    # Leave one out cross-validation with average author feature for top k authors
    print "Cross validation from feature to authors"
    diffa = np.zeros((1000,250))
    softkA = []
    k = 10
    for i, f in enumerate(F):
        nf = f / np.linalg.norm(f)
        # corra[i] = f.dot( nA.T )
        diffa[i] = np.power( f - A, 2 ).sum(axis=1)
        topk = diffa[i].argsort()[:k]+1
        softkA.append( (i/4+1) in topk )
    numcorrectA = np.array(softkA).astype(int).sum()
    print "Percent in the top %d is %f" %( k, float(numcorrectA)/len(F)*100 )

    # Greek or not?
    print "Discriminating Greek versus English"
    numcorrecteg=0
    for i, f in enumerate(F):
        diffeg = np.power( f - F, 2 ).sum(axis=1)
        topk = diffeg.argsort()[:k]
        #         English                        Greek
        if (i%4 < 2 and topk[1]%4<2) or (i%4 >= 2 and topk[1]%4 >= 2):
            numcorrecteg+=1
        else:
            break
            
