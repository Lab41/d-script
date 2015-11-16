import numpy as np
import scipy.misc
import scipy.ndimage
from scipy.stats import linregress
import math

def document_to_lines(img_filename):
    '''
    Algorithm: Use local projection profiles to segment lines per Diem, M., Kleber, F., Sablatnig, R.:
        Text Line Detection for Heterogeneous Documents
    Input:
    img_filename: string filepath

    Output:
    image: list of 2d arrays of line values
    '''
    pass

def normalize_line(line, binarize=False, expected_total_height=120, padding=20):
    '''
    This function takes in an input line and does the following operations:
    1) Convert to grayscale (potentially binarize using Otsu "A Threshold Selection Method from Gray-Level Histograms")
    2) Resize image such that height = expected_total_height-2*padding
    3) Add resized image to padded 2d array (filled with 255
    2) De-skew
        Fit a line to the high points and low points of the line then rotate by the mean slope
    Input:
    2d array of line pixel values

    output:
    2d array of line pixel values
    '''
    if binarize:
        raise NotImplementedError('Binarization not yet implemented')

    resize_height = expected_total_height - 2*padding
    (curr_height, curr_width) = line.shape
    resized_line = scipy.misc.imresize(line, (resize_height, curr_width))

    # Initialize new array
    resized_padded_line = np.empty((expected_total_height, curr_width + 2*padding))
    resized_padded_line.fill(255)
    resized_padded_line[padding:-padding, padding:-padding] = resized_line

    x_highs = []
    y_highs = []
    x_lows = []
    y_lows = []
    for col in range(resized_padded_line.shape[1]):
        high = None
        low = None
        for row in range(resized_padded_line.shape[0]):
            if high is None and resized_padded_line[row, col] < 250:
                high = row
            if resized_padded_line[row, col] < 250:
                low = row
        if high:
            x_highs.append(col)
            y_highs.append(high)
        if low:
            x_lows.append(col)
            y_lows.append(low)

    (high_slope, high_intercept, r_value, p_value, std_err) = linregress(x_highs,y_highs)
    (low_slope, low_intercept, r_value, p_value, std_err) = linregress(x_lows,y_lows)

    mean_slope = (high_slope+ low_slope)/2
    angle_to_rotate = math.atan2(mean_slope, 1)
    resized_padded_rotated_line = scipy.ndimage.rotate(resized_padded_line, angle_to_rotate, cval=255)
    return resized_padded_rotated_line

# # Code to draw line
# for col in range(line.shape[1]):
#     high_row = math.floor(high_slope*col + high_intercept)
#     line[high_row, col] = 0
#     low_row = math.floor(low_slope*col + low_intercept)
# #     line[low_row, col] = 0
#
# imsave('test.png', line)
