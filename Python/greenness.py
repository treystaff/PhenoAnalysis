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
