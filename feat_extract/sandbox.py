if False:
    execfile('extractfeats.py')

if False:
    print "Compiling all convolutional model, without dense layers"
    modelconvs = Sequential()
    for i in xrange(15):
        modelconvs.add( model.layers[i] )
    modelconvs.compile( loss='mse', optimizer='sgd' )
    f_convs = modelconvs.predict(X_test)

if False:
    print "Compiling all convolutional model, with dense layers"
    model1dense = Sequential()
    for i in xrange(17):
        model1dense.add( model.layers[i] )
    model1dense.compile( loss='mse', optimizer='sgd' )
    f_1dense= model1dense.predict(X_test)

if False:
    dense_weights = model.layers[16].get_weights()
    modeld2c = Sequential()
    for i in xrange(15):
        modeld2c.add( model.layers[i] )
    modeld2c.add( Convolution2D( 128, 10, 10, border_mode = 'valid' ) )
    modeld2c.add( Activation('relu') )    
    modeld2c.predict( X_test )

wholeimname = '/fileserver/nmec-handwriting/stil-writing-corpus/French/French-Images/FR-092-006.tif'
wholeimname = '/fileserver/iam/forms/d06-082.png'
wholeim = smi.imread(wholeimname)
wholeim = 1.0 - wholeim / 255.0
wholeim = np.expand_dims(wholeim,0)
wholeim = np.expand_dims(wholeim,0)
