import cPickle
from collections import OrderedDict
import numpy as np
from sklearn.ensemble import RandomForestClassifier as rfc

def pickleModels(trainedClassifier, file2save2 = None, fileName = 'myModels'):
    
    if file2save2 == None:
        f=file(fileName+'.save', 'wb')
    else:
        f=file(file2save2, 'wb')
        
    cPickle.dump(trainedClassifier, f, protocol=cPickle.HIGHEST_PROTOCOL)

    f.close()
    
def loadModels(filePath):
    file2open = file(filePath, 'rb')
    model = cPickle.load(file2open)
    file2open.close()
    
    return model

def authorPrediction(pickledModelPath, testData, numAuthors = 250):
    '''
    testData is a (1,128) vector needing to be predicted. Output is an ordered dictionary
    with authors as the keys and probabilities of match as values.
    '''
    
    model = loadModels(pickledModelPath)
    probs = model.predict_proba(testData.reshape(1,128))
    
    #where we collect output, key=authors and value=probabilities
    authPreds = OrderedDict()
    
    for auth in range(numAuthors):
        authPreds['author'+str(auth + 1)] = probs[:,auth][0]
    
    return authPreds

