if False:
    execfile('extractfeats.py')
#    model = fielnet('../convnets/fielnet/fielnet.hdf5')

if False:
    wholeimname = '/fileserver/nmec-handwriting/stil-writing-corpus/French/French-Images/FR-092-006.tif'
    wholeimname = '/fileserver/iam/forms/d06-082.png'
    wholeim = smi.imread(wholeimname)
    wholeim = 1.0 - wholeim / 255.0
    wholeim = np.expand_dims(wholeim,0)
    wholeim = np.expand_dims(wholeim,0)

if False:
    modelc = Sequential()
    modelc.add( Convolution2D( 4, 12, 12, border_mode='valid', input_shape=(1,120,120)) )
    modelc.add( MaxPooling2D( pool_size=(4,4) ) )
    modelc.add( Convolution2D( 5, 27, 27, border_mode='valid') )
    
    modeld = Sequential()
    modeld.add( Convolution2D( 4, 12, 12, border_mode='valid', input_shape=(1,120,120)) )
    modeld.add( MaxPooling2D( pool_size=(4,4) ) )
    modeld.add( Flatten() )
    modeld.add( Dense( 5 ) )

    modelc.compile(loss='mse',optimizer='sgd')
    modeld.compile(loss='mse',optimizer='sgd')

if False:
    modelcw = modelc.layers[0].get_weights()
    modeld.layers[0].set_weights(modelcw)
    modelcw = modelc.layers[-1].get_weights()
    Wc1 = modelcw[0]

if True:
    modeldw = modeld.layers[-1].get_weights()
    Wd1 = modeldw[0]
    # Wd1 = Wd1.T.reshape( 5, 4, 27, 27 )
    # Wd1 = Wd1.transpose(0,3,1,2)
    # Wd1 = Wd1.transpose(0, 1, 3, 2)

    # modelc.layers[-1].set_weights( [Wd1, modeldw[1]] )

c = modelc.predict(X_test).squeeze()
d = modeld.predict(X_test).squeeze()

from itertools import permutations

finalshape = [5,4,27,27]
newtranspose = [0,1,2,3]
for Wdt in [Wd1, Wd1.T]:
  for permutation in permutations(range(4)):
    newshape = [ finalshape[ p ] for p in permutation ]
    for i,p in enumerate(permutation):
      newtranspose[p] = i
    Wdn = Wdt.reshape( *newshape )
    print "Before transpose "+str(Wdn.shape)+" Reperm: "+str(newtranspose)
    Wdn = Wdn.transpose( *newtranspose )

    modelc.layers[-1].set_weights( [Wdn, modeldw[1]] )
    cn = modelc.predict(X_test).squeeze()

    eps = 0.03
    aggregate_error = np.mean( np.square( cn - d ) )
    print "Aggregate Error: "+str(aggregate_error)
    if cn[0,0] <= d[0,0]+eps and cn[0,0] >= d[0,0]-eps:
      print "Success!"
      break
  if cn[0,0] <= d[0,0]+eps and cn[0,0] >= d[0,0]-eps:
    print "Success!"
    break

modele = Sequential()
modele.add( modelc.layers[0] )
modelf = Sequential()
modelf.add(  modeld.layers[0] )
modele.compile( loss='mse', optimizer='sgd')
modelf.compile( loss='mse', optimizer='sgd')




