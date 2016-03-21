import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def compute_distance(x,y):
    if len(x)==0 or len(y)==0:
        return sys.maxint
    m = np.empty([len(y),len(x)])
    for i in range(len(y)):
        # m[i] = np.linalg.norm(A-B[i], 1, axis=1)
        m[i] = np.abs( x - y[i] ).sum(axis=1)
    return np.min(m, axis = 0).sum() / len(x)

def print_percentage(n, t):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('=' * ((n * 20/t) + 1) , n * 100/t + 1 ))
    sys.stdout.flush()

def loadfeats(corpdir):
    files = os.listdir(corpdir)
    files.sort()
    feature_map = []
    for i, filename in enumerate(files):
        path = corpdir + "/" + filename
        if os.path.isfile(path):
            feature_file = open(path, 'r').read().splitlines()
            alphabet = np.array([np.fromstring(line, dtype=np.float32, sep=' ')[1:129] for line in feature_file])
            feature_map.append(alphabet)
        print_percentage(i,len(files))
    return np.array(feature_map)

def calcadjacency(feature_map):
    if type(feature_map)!=str:
        metric = []
        for i, image in enumerate(feature_map):
            metricline = [np.array([compute_distance(image, other) for other in feature_map])]
            metric += metricline
            print_percentage(i, len(feature_map))
        metric = np.array(metric)
        F = -metric
        np.fill_diagonal(F, -sys.maxint)
    else:
        F = np.load(feature_map)
        print ""
    return F
        
def print_accuracy( F, k=10, g=8, max_top=3, comparea=False, verbose=False ):

    for comparej in xrange(8):
        soft_correct = 0
        hard_correct = 0
        total_num = 0
        for j, i in enumerate(F):
            if j%8==comparej or comparea: 
                total_num += 1
                topk = i.argsort()[-k:]
                if j/g in topk/g:
                    soft_correct += 1
                hardsample = sum([1 for jj in (j/g == topk[-max_top:]/g) if jj])
                if hardsample == max_top:
                    hard_correct += 1
                    if verbose:
                        print files[j][3:10]+": "+files[topk[-1]][3:10]+", "+files[topk[-2]][3:10]+", "+files[topk[-3]][3:10]
                elif verbose:
                    print "INCOR "+files[j][3:10]+": "+files[topk[-1]][3:10]+", "+files[topk[-2]][3:10]+", "+files[topk[-3]][3:10]
        print "Doc %d Top %d = %f" %(comparej, k, (soft_correct + 0.0) / total_num)
        print "Doc %d Top %d = %f" %(comparej, max_top, (hard_correct + 0.0) / total_num)
        if comparea:
            break
       
outsave = 'CleanJainVert.npy'
    
# corpdir = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/seamfeats/FR'
#corpdir = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/vertfeats/FR'
corpdir = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/jaincleanfeats/vertfeats'
#corpdir = '/fileserver/nmec-handwriting/stil-writing-corpus-processed/jaincleanfeats/seamfeats'
#knownfeats = 'CleanJainSeam.npy'

print outsave
corpfeats = loadfeats(corpdir)
F = calcadjacency(corpfeats)
if outsave:
    np.save(outsave, F)
print_accuracy(F)
