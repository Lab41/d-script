import matplotlib.pylab as plt

def viz_layer1( model ):
    
    convlayer = model.layers[0].get_weights()
    c1 = convlayer[0].squeeze()[0]
    c1 = (c1 - c1.min())/(c1.max() - c1.min())

def forwardviz(model, mbatch, numbatches, verbosity=1):
    
    ''' def forwardviz(model, mbatch, numbatches, verbosity=1):
          model: the model to be vizualized (can be partial)
          mbatch: minibatcher from Yonas's code
          numbatches: number of batches to run (stopping point)
          verbosity: verbosity in evaluating individual batches
          
          returns activations.
        
        Get the forward activations of model, using
        large scale modeling with data from minibatcher mbatch
    '''
    for i in range(numbatches):
        print "Loading data into memory & GPUs"
        (X_train, Y_train) = mbatch.get_batch()
        X_train = np.expand_dims(X_train, 1)
        Y_train = to_categorical(Y_train, num_authors)
        print "Beginning forward propagation on batch "+str(i)
        activations = model.predict(X_train, verbose=verbosity)
        print "Progress = "+str( (i+0.01-0.01) / numbatches)
        
    return X_train, activations

def forward2viz(model, X_train, verbosity=1):
    
    ''' def forward2viz(model, X_train, verbosity=1):
          model: the model to be vizualized (can be partial)
          X_train: input images to be analyzed
          verbosity: verbosity in evaluating individual batches
          
          returns activations.
    '''
    activations = model.predict(X_train, verbose=verbosity)

    return activations

def partialnetwork(model, layernum):
    ''' def partialnetwork(model, layernum):
          model: the original full model
          layernum: the last layer of the neural network that you want to evaluate
        
          returns partial_model: the resulting neural network
    '''
    
    for i,l in enumerate(model.layers):
        print str(i+1)+": "+str(l)
    print "You are looking at "+str(model.layers[layernum+1])
    
    if len(model.layers) < layernum:
        return model
    
    rmodel = Sequential()
    for i in xrange(layernum):
        rmodel.add(model.layers[i])
        rmodel.layers[i].set_weights( model.layers[i].get_weights() )
    
    rmodel.compile(loss='mse', optimizer='adadelta')
    return rmodel

