#!/usr/bin/env python

import io
# !pip install pypng
#import png
import numpy as np
import PIL
from IPython.display import Image, display

def get_png_from_array(data):
    """
    Take a 2D numpy array of 8-bit integer (I think?)
    values (rows x cols) and convert it
    to a grayscale (1-channel) PNG in memory. 
    
    Returns a 1D list of values that can be passed to, for
    example, IPython.display.Image
    """
    im = PIL.Image.fromarray(data)
    bio = io.BytesIO()
    im.convert('RGB')
    im.save(bio, format='png')
    return img.getvalue()

def display_img_array(ima):
    bio=get_png_from_array(ima)
    display(Image(bio, format='png', retina=True))