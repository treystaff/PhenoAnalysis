"""Functions pertaining to calculating and analyzing the 'greenness' of PhenoCam images."""

import numpy as np
import pandas as pd
from scipy import misc
import datetime
import utility as util
import pdb
import time
import os, sys

__author__ = 'Trey'

def mean_gcc(img, roi = None):
    """
    Calculates mean gcc from an image represented by a nummpy array
    Assumes array structured as [rows,cols,bands] where the first
    three bands are RGB.
    Mean Gcc = mean(green) / (mean(green)+mean(red)+mean(blue))

    Parameters:
        img - a PIL image object or numpy array of a PhenoCam image.
        roi - (optional) a PIL image or numpy array object of a PhenoCam image region of interest (roi).
    Returns:
        mean gcc value for non-masked portions of the input image.
    """
    # Extract RGB values
    red, green, blue = util.get_image_bands(img, roi=roi)

    # For some strange reason, printing red is sometimes the only way
    # to prevent a segfault. Redirect the print to /dev/null so it doesn't
    # hog stdout
    # f = open(os.devnull, 'w')
    # sys.stdout = f
    #print(red)
    #print('didsomething: ' + str(datetime.datetime.now().time()))
    # Calculate mean of pixels
    red = np.ma.average(red)
    green = np.ma.average(green)
    blue = np.ma.average(blue)

    # Calculate GCC
    gcc = green / (red + green + blue)

    # Return the calculated value.
    return gcc


def per90(dates, data):
    """
    Calculates the 90th percentile GCC from a numpy array of GCC values, over a
    given period.

    Supports arbitrarily long time series.

    Parameters:
        dates - An array of datetime objects corresponding to data values.
        data - An array of gcc values, each of which corresponds to a date in x
        period - the period (number of days) over which the per90 gcc value will be calculated.
            The default value is 3 days [NOT CURRENTLY SUPPORTED. ONLY 3 DAY PERIOD.]
    Returns:
        Two lists: per90_dates, per90_data

    Note:
        Now returns two lists instead of dataframe.
    """
    # First, make sure the data is sorted.
    dates, data = zip(*sorted(zip(dates, data)))

    # Get the min/max days of the series.
    startime = dates[0].date()
    endtime = dates[-1].date()

    # Create a timeseries panda's series
    ts = pd.Series(data, index=dates)

    # Compute the 90th percentile of every 3 day period (exclusive rn)
    per90_data = []
    per90_dates = []
    while startime < endtime:
        # Find the end of the window range.
        end = startime + datetime.timedelta(days=3)

        # Obtain the timeseries window of interest.
        window = ts[startime:end]

        # Calculate the 90th percentile
        per90_data.append(window.quantile(0.9))

        # Find the middle day of the 3day period (this will be the reported date associated w/ the 90th percentile...
        middate = startime + datetime.timedelta(days=1)
        per90_dates.append(middate)

        # Set the new startime to be the old end.
        startime = end

    # Return the results as two lists.
    return per90_dates, per90_data


def mean_ndvi(rgb, ir, roi=None):
    """
    Calculates the mean NDVI for the rgb/ir image pair

    Parameters:
        rgb - PIL image object of PhenoCam RGB image with same timestamp as ir. Alternatively, this can be a single-band
            red image. OR numpy array
        ir -  PIL image object of PhenoCam IR image with same timestamp as rgb OR numpy array.
        roi - PIL image object of PhenoCam roi image. OR numpy array

    Returns:
        The mean NDVI value.
    """
    # Extract the red and infrared bands
    try:
        red = rgb.split()
        red = red[0]

        ir = ir.split()
        ir = ir[0]

        red = np.asarray(red, dtype=float)
        ir = np.asarray(ir, dtype=float)
    except AttributeError:
        if len(rgb.shape) == 3:
            red = rgb[:, :, 0].astype(float)
        else:
            red = rgb.astype(float)

    # optionally use roi
    if roi is not None:
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


def mean_exg(img, roi=None):
    """
    Calculates mean EXG of an RBG PhenoCam image
    """
    # Extract mean RGB values
    red, green, blue = util.get_image_bands(img, roi=roi)

    # Calculate mean of pixels
    red = np.ma.average(red)
    green = np.ma.average(green)
    blue = np.ma.average(blue)

    # Calculate EXG
    exg = (2.0 * green) - (red + blue)

    # Return the result
    return exg

def mean_rcc(img, roi=None):
    """
    Calculates mean gcc from an image represented by a nummpy array
    Assumes array structured as [rows,cols,bands] where the first
    three bands are RGB.
    Mean Rcc = mean(red) / (mean(green)+mean(red)+mean(blue))

    Parameters:
        img - a PIL image object or numpy array of a PhenoCam image.
        roi - (optional) a PIL image or numpy array object of a PhenoCam image region of interest (roi).
    Returns:
        mean gcc value for non-masked portions of the input image.
    """
    # Extract RGB values
    red, green, blue = util.get_image_bands(img, roi=roi)

    # Calculate mean of pixels
    red = np.ma.average(red)
    green = np.ma.average(green)
    blue = np.ma.average(blue)

    # Calculate GCC
    gcc = red / (red + green + blue)

    # Return the calculated value.
    return gcc


def mean_bcc(img, roi=None):
    """
    Calculates mean gcc from an image represented by a nummpy array
    Assumes array structured as [rows,cols,bands] where the first
    three bands are RGB.
    Mean Bcc = mean(blue) / (mean(green)+mean(red)+mean(blue))

    Parameters:
        img - a PIL image object or numpy array of a PhenoCam image.
        roi - (optional) a PIL image or numpy array object of a PhenoCam image region of interest (roi).
    Returns:
        mean bcc value for non-masked portions of the input image.
    """
    # Extract RGB values
    red, green, blue = util.get_image_bands(img, roi=roi)

    # Calculate mean of pixels
    red = np.ma.average(red)
    green = np.ma.average(green)
    blue = np.ma.average(blue)

    # Calculate GCC
    gcc = blue / (red + green + blue)

    # Return the calculated value.
    return gcc