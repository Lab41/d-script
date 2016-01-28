#!/usr/bin/env python

import io
import logging
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
    return bio.getvalue()

def display_img_array(ima):
    bio=get_png_from_array(ima)
    display(Image(bio, format='png', retina=True))
    
def rescale_img_array(x, scale_factor):
    logger = logging.getLogger(__name__)
    img = PIL.Image.fromarray(x)
    new_w = int(x.shape[1] * scale_factor)
    new_h = int(x.shape[0] * scale_factor)
    img = img.resize((new_w,new_h),PIL.Image.NEAREST)
    x = np.array(img.getdata(), dtype=x.dtype).reshape(new_h, new_w)
    return x