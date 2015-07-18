"""Functions pertaining to calculating and analyzing the 'greenness' of PhenoCam images."""

import numpy as np
import pandas as pd
from scipy import misc
__author__ = 'Trey'

def mean_gcc(img, roi = None):
    """
    Calculates mean gcc from an image represented by a nummpy array
    Assumes array structured as [rows,cols,bands] where the first
    three bands are RGB.
    Mean Gcc = mean(green) / (mean(green)+mean(red)+mean(blue))

    Parameters:
        img - a PIL image object of a PhenoCam image.
        roi - (optional) a PIL image object of a PhenoCam image region of interest (roi).
    Returns:
        mean gcc value for non-masked portions of the input image.
    """
    # Extract mean RGB values
    red, green, blue = img.split()
    red = np.asarray(red, dtype=float)
    green = np.asarray(green, dtype=float)
    blue = np.asarray(blue, dtype=float)

    if roi:
        roi = np.asarray(roi, dtype=bool)
        red = np.ma.array(red, mask=roi)
        green = np.ma.array(green, mask=roi)
        blue = np.ma.array(blue, mask=roi)

    # Calculate mean of pixels
    red = red.mean()
    green = green.mean()
    blue = blue.mean()

    # Calculate GCC
    gcc = green / (red + green + blue)

    # Return the calculated value.
    return gcc


def per90(dates, gcc, label='Per90', period=3):
    """
    Calculates the 90th percentile GCC from a numpy array of GCC values, over a
    given period.

    Supports arbitrarily long time series.

    Parameters:
        dates - An array of datetime objects corresponding to the calculated GCC values.
        gcc - An array of gcc values, each of which corresponds to a date in x
        label - A string for which to label the per90 calculated dataframe column.
        period - the period (number of days) over which the per90 gcc value will be calculated.
            The default value is 3 days
    Returns:
        A pandas dataframe containng the resampled per90 data.

    Note:
        This will likely change as the pandas dataframe is incorporated into
        more of the codebase (i.e., the dates and gcc arguments will be replaced
        by a pandas dataframe, and this function will simply resample the dataframe,
        without initializing one from date and gcc arrays...)
    """
    # Create a pandas dataframe for the data. (useful timeseries functions builtin)

    df = pd.DataFrame(data=gcc, index=dates, columns=[label])


    # Define a 90th percentile function that can be used by pandas' resample method
    #per = lambda x: np.percentile(x, 90)

    def per(x):
        return np.percentile(x, 90)


    # Resample the dataframe to period number of days
    pdb.set_trace()
    df = df.resample(str(period) + 'D', how=per)

    # Return the resampled dataframe
    return df

def mean_ndvi(rgb, ir, roi=None):
    """
    Calculates the mean NDVI for the rgb/ir image pair

    Parameters:
        rgb - PIL image object of PhenoCam RGB image with same timestamp as ir
        ir -  PIL image object of PhenoCam IR image with same timestamp as rgb
        roi - PIL image object of PhenoCam roi image.

    Returns:
        The mean NDVI value.
    """
    # Extract the red and infrared bands
    red, _, _ = rgb.split()
    ir, _, _ = ir.split()

    red = np.asarray(red, dtype=float)
    ir = np.asarray(ir, dtype=float)

    # optionally use roi
    if roi:
        roi = np.asarray(roi, dtype=bool)
        red = np.ma.array(red, mask=roi)
        ir = np.ma.array(ir, mask=roi)

    # Get the mean red and ir values
    red = red.mean()
    ir = ir.mean()

    # Calculate and return NDVI
    return (ir - red) / (ir + red)

def create_ndvi(rgb, ir, saveto=None):
    """
    Create an NDVI image

    Parameters:
        rgb - PhenoCam RGB image with same timestamp as ir
        ir - PhenoCam IR image with same timestamp as rgb
        saveto - Path to save NDVI image to (optional)

    Returns:
        ndvi - A numpy matrix representing an NDVI image.
    """
    # Extract the necessary bands
    red = rgb[:,:,0].astype(np.int16)
    ir = ir[:,:,0].astype(np.int16)

    # Create a new numpy matrix to contain the ndvi image.
    ndvi = np.zeros(red.shape)  # Should be same shape as red band

    ndvi = np.true_divide(np.subtract(ir, red), np.add(ir, red))

    if saveto:
        misc.imsave(saveto, ndvi)

    return ndvi

def create_cir(rgb, ir, saveto=None):
    """
    Create a color infrared image.

    Parameters:
        rgb - PhenoCam RGB image with same timestamp as ir
        ir - PhenoCam IR image with same timestamp as rgb
        saveto - Path to save the image to (optional)

    Returns:
        A color infrared image (a numpy array), optionally saved to file.
    """
    # Extract the necessary bands
    red = rgb[:,:,0]
    green = rgb[:,:,1]
    ir = ir[:,:,0]

    # Create a new numpy matrix to contain the cir image.
    cir = np.zeros(rgb.shape)  # Should be same shape as rgb image.

    # Compose the cir image
    cir[:,:,0] = ir
    cir[:,:,1] = red
    cir[:,:,2] = green

    # Optionally, save the result to file.
    if saveto:
        misc.imsave(saveto, cir)

    # Return the result
    return cir
