import pandas as pd
import pdb

def mean_gcc(img):
	"""
	Calculates mean gcc from an image represented by a nummpy array
	Assumes array structured as [rows,cols,bands] where the first
	three bands are RGB.
	Mean Gcc = mean(green) / (mean(green)+mean(red)+mean(blue))

	Arguments:
		img: a numpy array, the shape of which is equivalent to (rows,cols,bands)
			For now, a mask is defined by pixels where all bands' value
			is zero.
	Output:
		mean gcc value for non-masked portions of the input image.
	"""
	#Extract mean RGB values
	red = img[:,:,0]
	green = img[:,:,1]
	blue = img[:,:,2]

	#For now, assume [0,0,0] is baddata and should be discarded.
	msk = img[:,:,:] != 0

	#Calculate mean of good pixels
	red = red[msk[:,:,0]].mean()
	green = green[msk[:,:,1]].mean()
	blue = blue[msk[:,:,2]].mean()

	#Calculated GCC
	gcc = green / (red + green + blue)

	#Return the calculated value.
	return gcc

def per90(dates,gcc,period=3):
	'''
	Calculates the 90th percentile GCC from a numpy array of GCC values, over a
	given period.

	Supports arbitrarily long time series. 

	Arguments:
		dates: An array of datetime objects corresponding to the calculated GCC values.
		gcc: An array of gcc values, each of which corresponds to a date in x
		period: the period (number of days) over which the per90 gcc value will be calculated.
			The default value is 3 days
	Output:
		df: A pandas dataframe containng the resampled per90 data.

	Notes: This will likely change as the pandas dataframe is incorporated into
		more of the codebase (i.e., the dates and gcc arguments will be replaced
		by a pandas dataframe, and this function will simply resample the dataframe,
		without initializing one from date and gcc arrays...)
	'''
	# Create a pandas dataframe for the data. (useful timeseries functions builtin)
	df = pd.DataFrame(data = gcc, index = dates

	# Define a 90th percentile function that can be used by pandas resample method
	def per(x): return np.percentile(x,90)

	# Resample the dataframe to period number of days
	df = df.resample(str(period)+'D',how=per)

	# Return the resampled dataframe
	return df
