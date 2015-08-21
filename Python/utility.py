"""Utility functions"""
from PIL import Image, ImageFilter
from pytesseract import image_to_string
import re
from warnings import warn
import numpy as np
import math
from scipy.optimize import curve_fit
import datetime
from scipy.misc import imsave
import pdb

def charCorrect(inStr):
    """
    Support function for read_header(). Borrowed with some minor edits from
    Joe M. Krienert's (jkrienert@siu.edu) PhenoCamStats-OCR.py
    """
    if '?' in inStr: inStr = inStr.replace('?','7')
    if 'D' in inStr: inStr = inStr.replace('D','0')
    if 'E!' in inStr: inStr = inStr.replace('E!','8')
    if 'EI' in inStr: inStr = inStr.replace('EI','8')
    if 'El' in inStr: inStr = inStr.replace('El','8')
    if 'EH' in inStr: inStr = inStr.replace('EH','8')
    if ' I' in inStr: inStr = inStr.replace(' I','1')
    if 'S' in inStr: inStr = inStr.replace('S','5')
    if '4-' in inStr: inStr = inStr.replace('4-','4')
    return inStr


def read_header(img):
    """
    Reads the header from PhenoCam images using OCR.

    Parameters:
        img: a PIL image object.

    Returns:
        Exposure and temperature values

    Note:
        inspired by Joe M. Krienert's (jkrienert@siu.edu) PhenoCamStats-OCR.py,
         which batch processes PhenoCam images and records results to csv file.

         This will probably end up changing significantly. This was quickly thrown together
         and suffers from poor error handling. Also, tesseract can be trained to read
         PhenoCam font family, which should significantly increase accuracy. See e.g.,
         http://tomsik.eu/train_tesseract
    """
    img = Image.fromarray(img)
    # Crop the image to the approximate area of the header
    #   (leave larger than necessary for variable-length headers)
    crop = img.crop((0, 0, 1296, 200))

    # Filter the image with an edge detector to highlight character edges
    edges = crop.filter(ImageFilter.FIND_EDGES)
    '''
    # Make the image grayscale
    gray = edges.convert('L')

    # Finally, threshold the grayscale image
    bw = gray.point(lambda x: 0 if x<150 else 255, 'L')
    '''
    # Read text from the image
    text = image_to_string(edges)
    if not text:
        raise ValueError('No text was found in image')

    # Extract the relevant values
    temperature = None
    exposure = None

    header_list = text.split('\n')
    for text in header_list:
        text = charCorrect(text)
        text = text.lower()
        if 'temperature' in text or  'temp' in text or 'ature' in text:
            temperature = re.findall(r'[-+]?\d+[.\d+]?', text)
            # temperature = re.findall(r'[-+]?\d+.\d+', text)  # Ideal regex
            if len(temperature) > 1:
                # Check if there is more than one decimal
                dec_idxes = []
                for idx, val in enumerate(temperature):
                    if '.' in val:
                        dec_idxes.append(idx)
                # If there's a stray decimal, fix it (assumes first decimal is wrong)
                if len(dec_idxes) > 2:
                    raise ValueError('More than one temperature value detected')
                elif len(dec_idxes) == 2:
                    min_idx = min(dec_idxes)
                    # Seems to be this stray decimal is followed by 7. Warn user if without trailing 7.
                    if not temperature[min_idx + 1].startswith('7'):
                        warn('Unexpected number of decimals without trailing 7: ' + str(temperature))

                    temperature[min_idx] = temperature[min_idx].replace('.', '')

                fixed_temp = ''
                for val in temperature:
                    fixed_temp += val
                temperature = fixed_temp
                try:
                    float(temperature)
                except ValueError:
                    raise ValueError('Could not read temperature value.')
            elif len(temperature) == 0:
                raise ValueError('Could not read temperature value.')
            else:
                temperature = temperature[0]
                try:
                    float(temperature)
                except ValueError:
                   raise ValueError('Could not read temperature value')

        if 'exposure' in text or 'expo' in text or 'sure' in text:
            exposure = re.findall(r'\d+[.\d+]?', text)
            if len(exposure) > 1:
                if "3'9" in text and len(exposure)==2:
                    # May be a 3'9, should be 79
                    exposure = '79'
                else:
                    raise ValueError('More than one exposure value detected')
            else:
                try:
                    exposure = exposure[0]
                except IndexError:
                    raise ValueError('Could not read exposure value')
                try:
                    float(exposure)
                except ValueError:
                    raise ValueError('Could not read exposure value.')

    # Return exposure and temp values.
    return exposure, temperature

def IRview_to_NIR(rgb, irview,cir=None, saveto=None):
    """
    Converts PhenoCam IR view to a NIR image according to the method described by
    Petach 2014.

    Parameters:
        rgb: PIL image object representing a PhenoCam RGB image with same timestamp as irview
        irview: PIL image object representing a PhenoCam IR image with same timestamp as rgb
        saveto: Path to save new NIR image to.

    Returns:
        nir: a near-infrared image (PIL object)
        red: an adjusted red image (PIL object), for use in calculating NDVI.
    """
    # Obtain bands from rgb image
    red, green, blue = get_image_bands(rgb)

    # Obtain one of the bands from the IR image
    ir, _, _ = get_image_bands(irview)

    # Calculate the 'visible component' of the image pair
    visible = 0.3 * red + 0.59 * green + 0.11 * blue

    # Obtain the exposure values from the images
    rgb_exp, _ = read_header(rgb)
    ir_exp, _ = read_header(irview)
    if rgb_exp is None or ir_exp is None:
        raise ValueError('EXPOSURE VALUES NOT READ FROM IMAGES. COULD NOT CORRECT.')

    if rgb_exp != ir_exp:
        # Correct for exposure
        ir = np.true_divide(ir, math.sqrt(float(ir_exp)))
        red = np.true_divide(red, math.sqrt(float(rgb_exp)))
        green = np.true_divide(green, math.sqrt(float(rgb_exp)))
        visible = np.true_divide(visible, math.sqrt(float(rgb_exp)))

    pdb.set_trace()
    # Optionally, return a cir image and ndvi
    if cir is not None:
        cir = np.ones(rgb.shape)
        cir[:,:,0] = ir
        cir[:,:,1] = red
        cir[:,:,2] = green

        ndvi = np.ones(red.shape)
        ndvi = np.true_divide(np.subtract(ir, red), np.add(ir, red))


    # Calculate the NIR component:
    nir = ir - visible

    # Create a new PIL image (Problem w/ PIL, so don't use)
    # nir_image = Image.fromarray(nir)
    # red = Image.fromarray(red)

    # Optionally, save
    if saveto:
        imsave(saveto, nir)

    # Return the result.
    return nir, red, cir, ndvi

def corrected_mean_ndvi(rgb, irview, roi):
    """Experimental function"""
    # Obtain the exposure values from the images
    rgb_exp, _ = read_header(rgb)
    ir_exp, _ = read_header(irview)

    # Obtain bands from rgb image
    red, green, blue = get_image_bands(rgb, roi=roi)


    # Obtain one of the bands from the IR image
    ir, _, _ = get_image_bands(irview, roi=roi)

    red = np.ma.average(red)
    green = np.ma.average(green)
    blue = np.ma.average(blue)
    ir = np.ma.average(ir)

    # Calculate the 'visible component' of the image pair
    visible = 0.3 * red + 0.59 * green + 0.11 * blue

    if rgb_exp != ir_exp:
        # Correct for exposure
        ir = np.true_divide(ir, math.sqrt(float(ir_exp)))
        red = np.true_divide(red, math.sqrt(float(rgb_exp)))
        visible = np.true_divide(visible, math.sqrt(float(rgb_exp)))

    # Calculate the NIR component:
    nir = ir - visible

    # Now calculate NDVI
    ndvi = (nir - red) / (nir + red)

    return ndvi


def limit_data_tod(dates, data, startTOD=datetime.time(10,0), stopTOD=datetime.time(14,0)):
    """limit gcc time of day"""
    mod_data = [cc for cc, dt in zip(data,dates) if dt.time() >= startTOD and dt.time() <= stopTOD]
    mod_dates = [dt for cc, dt in zip(data,dates) if dt.time() >= startTOD and dt.time() <= stopTOD]
    return mod_dates, mod_data


def get_image_bands(img, roi=None):
    """
    Returns the RGB bands from PhenoCam, optionally masked
    """
    # Extract RGB values
    try:
        red, green, blue = img.split()
        red = np.asarray(red, dtype=float)
        green = np.asarray(green, dtype=float)
        blue = np.asarray(blue, dtype=float)
    except AttributeError:
        red = img[:, :, 0].astype(float)
        green = img[:, :, 1].astype(float)
        blue = img[:, :, 2].astype(float)

    if roi is not None:
        roi = np.asarray(roi, dtype=bool)
        red = np.ma.array(red, mask=roi)
        green = np.ma.array(green, mask=roi)
        blue = np.ma.array(blue, mask=roi)

    return red, green, blue
