#!/usr/bin/env python

import io
# !pip install pypng
import png
import numpy as np
import PIL
from IPython.display import Image, display

def get_png_from_array(data):
    """
    Take a 2D numpy array of 8-bit integer (I think?)
    values (rows x cols) and convert it
    to a grayscale (1-channel) PNG. 
    
    Returns a 1D list of values that can be passed to, for
    example, IPython.display.Image
    """
    buf = io.BytesIO()
    w = png.Writer(*data.shape[::-1], greyscale=True)
    w.write(buf, data)
    return buf.getvalue()

def display_img_array(ima):
    im = PIL.Image.fromarray(ima)
    bio = io.BytesIO()
    im.convert('RGB')
    im.save(bio, format='png')
    display(Image(bio.getvalue(), format='png', retina=True))