"""Script for creating GCC plots of the Kansas and Nebraska PhenoCam sites. For experimental use only."""
from PIL import Image
import numpy as np
import pandas as pd
import greenness as grn
from phenocam_toolkit import *
import pickle
import pdb
import matplotlib.pyplot as plt

'''***AUTOMATED SECTION BELOW***'''
# Calculate data from images, or load?
def save_image_data(phenoDir, sitename, save_data_path, roi_path=None):
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

def load_image_data(saved_data_path):
    # Open/load the existing data
    with open(saved_data_path) as savefile:
        data_dict = pickle.load(savefile)
        gcc = data_dict['gcc']
        dates = data_dict['dates']
        return gcc, dates

def create_plots(sitename, saved_data_path):
    # Load the data
    gcc, dates = load_image_data(saved_data_path)
    # Now we have the gcc and dates, calculate per90
    per90_gcc, per90_dates = grn.per90(dates, gcc)

    # Do some plotting
    fig, ax = plt.subplots(1)
    ax.plot(dates, gcc, 'b.', label='Raw GCC')
    ax.plot(per90_dates, per90_gcc, 'go', label='Per90 GCC', markersize=8)
    plt.title(sitename + ' Raw GCC vs 3 Day Per90 GCC')
    plt.xlabel('Date')
    plt.ylabel('GCC')
    plt.legend(loc='best', numpoints=1)
    fig.autofmt_xdate()  # Makes the xaxis dates easier to read.

if __name__ == "__main__":
    # USER INPUT
    # phenoDir = '/storage/PhenoCam/images/phenocamdata/'  # Path to phenocam archives.
    # sitename = 'kansas'
    # roi_path = '/storage/PhenoCam/images/kansas_mask.tif'
    # roi_path = '/storage/PhenoCam/images/ninemile_mask.tif'

    # Nine Mile
    sitename = 'ninemileprairie'
    saved_data_path = '/storage/PhenoCam/data/ninemile_gcc_data.pickle'
    create_plots(sitename, saved_data_path)
    # Kansas
    sitename = 'kansas'
    saved_data_path = '/storage/PhenoCam/data/kansas_gcc_data.pickle'
    create_plots(sitename, saved_data_path)
    # Show the plots!
    plt.show()