import numpy as np
import logging
import PIL

def sample_with_rotation(x, center, angle, 
                         box_dim=(120,120), 
                         fill_value=255, 
                         wraparound=True,
                         stdev_threshold=None,
                         test_stdev=False):
    """ Get a patch from x, with rotation, without having to rotate the
    whole image. (Turns out this is really slow)
    
    """
    rows, cols=box_dim
    img_rows, img_cols = x.shape    
    
    if test_stdev:
        l,b,r,t = sample_bounds = center[0] - cols/2, \
                        center[1] + rows/2, \
                        center[0] + cols/2, \
                        center[1] - rows/2
        if t < 0:
            t = 0
        if l < 0:
            l = 0
        if r > img_cols:
            r = img_cols
        if b > img_rows:
            b = img_rows
        sample_stdev = np.std(x[t:b, l:r])
        if sample_stdev < stdev_threshold:
            raise ValueError
        
    
    # subtract half box width and height from translation vector to center it on sampling point
    # epsilon to avoid naughty numpy rounding behavior
    epsilon = 10e-4
    translation_matrix = np.zeros((3,3),dtype=np.float32)
    np.fill_diagonal(translation_matrix, 1)
    translation_matrix[0,2] = -cols/2. + epsilon
    translation_matrix[1,2] = -rows/2. + epsilon
    
    # rotation matrix for sampling box centered on 0,0
    if angle != 0:
        rotation_matrix = np.zeros((3,3),dtype=np.float32)
        rotation_matrix[0,0] = np.cos(angle)
        rotation_matrix[1,1] = np.cos(angle)
        rotation_matrix[1,0] = np.sin(angle)
        rotation_matrix[0,1] = -np.sin(angle)
        rotation_matrix[2,2] = 1
    
    # second translation, into image coordinates
    back_translation_matrix = np.zeros((3,3),dtype=np.float32)
    np.fill_diagonal(back_translation_matrix, 1)
    back_translation_matrix[0,2] = center[0] + epsilon
    back_translation_matrix[1,2] = center[1] + epsilon

    xforms = []

    # translation
    xforms.append(translation_matrix) 
    # rotation in homogeneous coords
    if angle != 0:
        xforms.append(rotation_matrix)
    # translation back
    xforms.append(back_translation_matrix) 
 
    # sampling grid in image coordinates
    sample = (np.ones(shape=(box_dim)) * fill_value).astype(x.dtype)
    x_coords = np.tile(np.arange(cols, dtype=np.float32), rows).reshape(-1)
    y_coords = np.repeat(np.arange(rows, dtype=np.float32), cols).reshape(-1)
    xy_coords = np.dstack((x_coords, y_coords, np.ones_like(x_coords))).transpose((0,2,1))
    new_xy_coords = xy_coords[:,:,:]
    for xform in xforms:
        new_xy_coords = np.dot(xform, new_xy_coords).transpose(1,0,2)

    new_xy_coords = np.around(new_xy_coords).astype(np.int32)
    
    # sample according to new coordinates
    for i in xrange(new_xy_coords.shape[2]):
        orig_x, orig_y, _ = orig_xy = np.around(xy_coords[0,:,i]).astype(np.int32)
        sample_x, sample_y, _ = sample_xy = new_xy_coords[0,:,i]
        try:
            img_col = sample_x
            img_row = sample_y
            if wraparound:
                img_col = img_col % img_cols
                img_row = img_row % img_rows
            else:
                if img_col < 0 or img_row < 0:
                    raise IndexError
            sample[orig_y,orig_x] = x[img_row,img_col]
        except IndexError:
            # out-of-bounds, just leave blank
            pass    
    return sample

def rescale_array(x, scale_factor=0.25):
    logger = logging.getLogger(__name__)
    img = PIL.Image.fromarray(x)
    new_w = int(x.shape[1] * scale_factor)
    new_h = int(x.shape[0] * scale_factor)
    img = img.resize((new_w,new_h),PIL.Image.NEAREST)
    x = np.array(img.getdata()).reshape(new_h, new_w)
    return x