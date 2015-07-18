"""Script for creating GCC plots of the Kansas and Nebraska PhenoCam sites. For experimental use only."""
from PIL import Image
import numpy as np
import pandas as pd
import greenness as grn
from phenocam_toolkit import *
import pickle
import pdb


# USER INPUT
phenoDir = '/storage/phenocamdata/'  # Path to phenocam archives.
#sitename = 'ninemileprairie'  # The sitename of the PhenoCam site.
sitename = 'kansas'
roi_path = '/storage/kansas_mask.tif'
#roi_path = '/storage/ninemile_mask.tif'
saved_data_path = None
save_data_path = '/tmp/gcc_data.pickle'

'''***AUTOMATED SECTION BELOW***'''
# Calculate data from images, or load?
if not saved_data_path:
    # Open the mask if exists
    if roi_path:
        roi = Image.open(roi_path)
    else:
        roi = None

    # Get all of the image filepaths
    paths = getsiteimglist(phenoDir, sitename)
    total = len(paths)
    # Loop thru each filename, calculating mean gcc for each:
    gcc = []
    dates = []
    count = 0

    progress = []
    for path in paths:
        fn = os.path.split(os.path.splitext(path)[0])[1] + '.jpg'
        date = fn2datetime(sitename, fn)
        dates.append(date)
        img = Image.open(path)
        gcc.append(grn.mean_gcc(img, roi=roi))

        # Track progress
        percent = count / float(total)
        if percent > 0.9 and 0.9 not in progress:
            print('About 90% Done...')
            progress.append(0.9)
        elif percent > 0.7 and 0.7 not in progress:
            print('About 70% Done...')
            progress.append(0.7)
        elif percent > 0.5 and 0.5 not in progress:
            print('About 50% Done...')
            progress.append(0.5)
        elif percent > 0.3 and 0.3 not in progress:
            print('About 30% Done...')
            progress.append(0.3)
        elif percent > 0.1 and 0.1 not in progress:
            print ('About 10% Done...')
            progress.append(0.1)

        count += 1

    if save_data_path:
        # Save the gcc/dates calculations for later use.
        data_dict = {'gcc': gcc, 'dates': dates}
        with open(save_data_path, 'w') as savefile:
            pickle.dump(data_dict, savefile)

# Open/load the existing data
else:
    with open(saved_data_path) as savefile:
        data_dict = pickle.load(savefile)
    gcc = data_dict['gcc']
    dates = data_dict['dates']

# Now we have the gcc and dates, calculate per90
per90_gcc = grn.per90(dates, gcc)
