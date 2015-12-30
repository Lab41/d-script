import os
import re
import matplotlib.pylab as plt
import PIL.Image as Image
import numpy

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


def iam_get_text_block(form_id, data_root):
    """Recover coordinates of the handwriting part of an IAM form
    
    Arguments:
        form_id -- IAM form ID, XNN-NNNNN
    
        data_root -- path to the root of the IAM distribution (with forms,
            lines, etc. folders and .txt files as its children)
            
    Returns:
        the left, top, right, and bottom of a bounding box around the 
        handwriting portion of the form denoted by form_id

    """
    forms_path_template = os.path.join(data_root, 'forms/{}.png')
    lines_txt_path = os.path.join(data_root, 'lines.txt')
    eight_space_re=re.compile(r'(([^s]+\s){7}).*')
    form_left, form_top, form_right, form_bottom = None, None, None, None
    with open(lines_txt_path, 'r') as lines_data:
        for line_line in lines_data:
            if line_line.startswith(form_id):
                line_line_chopped = eight_space_re.sub('\\1', line_line).strip()
                try:
                    line_id, errcode, graylvl, num_components, left, top, width, height = line_line_chopped.split(' ')
                except ValueError:
                    # malformed line
                    pass
                left = int(left); top = int(top); width = int(width); height=int(height)
                if form_top is None: # or top < form_top_left[1]:
                    form_top = top
                    form_left = left
                    form_bottom = top+height
                    form_right = left+width
                else:
                    form_top = min(top, form_top)
                    form_left = min(left, form_left)                
                    form_bottom = max(top+height, form_bottom)
                    form_right = max(left+width, form_right)
                 
    return form_left, form_top, form_right, form_bottom

def readtif(imname):
    im = Image.open(imname)
    return numpy.array( im.getdata(), numpy.uint8 ).reshape(im.size[1], im.size[0])

def readcolim(imname):
    im = Image.open(imname)
    return numpy.array( im.getdata(), numpy.uint8).reshape(im.size[1], im.size[0],3)
