import matplotlib.pylab as plt

convlayer = model.layers[0].get_weights()
c1 = convlayer[0].squeeze()[0]
c1 = (c1 - c1.min())/(c1.max() - c1.min())
