"""
Functions for processing landsat data
Included functions:
	-read_metadata(metapath)
	-unpack_landsat(inpath,outpath,bands=None)
	-unpack_dir(indir,outdir,bands=None)
	-stack_layers(inDir,outPath,bands=None)
	-world2Pixel(geoMatrix, x, y)
	-Pixel2World(geoMatrix,x,y)
	-clip_raster(inRaster,outRaster,inShape)
	-batch_stack_clip(indir,outdir,shape)
	
Dependencies: gdal, numpy, scipy
"""

#MOST ALL OF THIS CODE DERIVED FROM: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
import tarfile
import glob
import gdal
import osr
import ogr
import Image
import ImageDraw
import gdalnumeric
import os
import pdb
import numpy as np

def read_metadata(metapath):
	"""
	Returns a dict of metadata read from landsat MTL.txt files
	Inspired by http://stackoverflow.com/questions/17183122/convert-contents-of-metadata-file-into-variables-list
	
	Arguments:
		metapath: Full path to landsat metadata file.
	Output:
		Dictionary of metadata read from landsat MTL.txt file. 
	"""
	with open(metapath) as metaFile:
		metadata = {}
		for line in metaFile.readlines():
			if "=" in line: #Get only key-value pairs
				l = line.split("=")
				metadata[l[0].strip()] = l[1].strip()
	
	return metadata
		


def unpack_landsat(inpath,outpath,bands=None):
	"""
	Function to unpack a landsat archive (.tar.gz) to a 
	 specified output directory. 
	 
	 This function makes the assumption that the archive is 
	 ordered by band and that the last file is a metadata file.
	 
	 Arguments:
		inpath: Full path to landsat archive (.tar.gz extention)
		outpath: Full path to an outup directory in which to place the
			extracted files from the inpath archive.
		bands: list of bands to extract from the archive. Default = all.
		
	 Output: 
		Unpacked landsat archive to the outpath directory
	 
	"""
	tfile = tarfile.open(inpath,'r:gz')
	if bands is None:
		#Extract all of the bands. 
		tfile.extractall(outpath);
	else:
		#Extract just the bands specified. 
		bands = list(bands)
		bands.append(len(tfile.getnames())) #Also get the metadata file.
		
		members = tfile.getmembers()
		tfile.extractall(outpath,members = [members[i-1] for i in bands])
		
	
	'''
	Note: the below section was written with the intention of 
	adding valuable metadata info to the .TIF files themselves. 
	This theoretically allows easy retreival of key metadata info, 
	but the method to set new metadata seems unreliable. Appears to 
	be an open issue, but there may be a solution. For now, assume 
	this does not work.
	
	#Now we loop through each output, adding important metadata.
	#Fetch metadata and make sure there is only one file. 
	meta = glob.glob(outpath + '/*_MTL.txt')
	if len(meta) > 1:
		raise('MORE THAN ONE METADATA FILE FOUND!')
	
	metadata = read_metadata(meta[0])
	
	#Add the metadata.
	for tif in glob.glob(outpath + '*.TIF'):
		#Open the tif file
		ras = gdal.Open(tif)
		
		#Preserve any existing metadata & add important metadata from file 
		meta = ras.GetMetadata()
		meta['SCENE_CENTER_TIME'] = metadata['SCENE_CENTER_TIME']
		meta['DATE_ACQUIRED'] = metadata['DATE_ACQUIRED']
		meta['LANDSAT_SCENE_ID'] = metadata['LANDSAT_SCENE_ID']
		
		#Now write the new metadata back to the tif. 
		ras.SetMetadata(meta)
		ras.FlushCache()
		ras = None
	'''
		
def unpack_dir(indir,outdir,bands=None):
	"""
	This function unpacks all landsat archives in a directory. 
	Resulting files are placed in subfolders named after 
	base filename in the specified outdir.

	arguments: 
		indir: Directory in which landsat archives are located
		outdir: Directory to which archives will be unpacked. 
			Each archive will be unpacked into a subfolder of 
			outdir named after the archive. 
		bands: List of bands to unpack from the archives. 
		
	output: 
		Unpacked landsat archives to subfolders of outdir named after the
			landsat base filename. 
	"""
	archives = glob.glob(indir + '*.tar.gz')
	count = len(archives)
	for idx, archive in enumerate(archives):
		#Determine the outpath directory name for the unpacked landsat archive
		unpackDir = outdir + os.path.splitext(os.path.split(
			os.path.splitext(archive)[0])[1])[0]
		
		#Check if the directory already exists and make it if it doesn't
		if not os.path.exists(unpackDir):
			os.makedirs(unpackDir)
		
		#Unpack the current archive.
		unpack_landsat(archive,unpackDir,bands=bands)
		
		#Let the user know how progress is going. 
		print(archive + ' unpacked (' + str(idx+1) + ' of ' + str(count) + ')')
		
		
def stack_layers(inDir,outPath,bands=None):
	"""
	Function to stack layers into a single TIF image.
	Currently only supports landsat bands that end with _B#.TIF
	
	Arguments:
		inDir: Directory containing landsat layers to stack
		outPath: the full path to the output .TIF file
		bands: list of bands to stack. Default is all bands 
			contained in inDir.
	Output:
		A stacked .TIF image 
	"""
	# ONLY SUPPORTS inDir W/ LANDSAT BANDS ENDING /w '_B#.TIF'
	#band = ds.GetRasterBand(1)
	#band.GetStatistics(True,True) - returns min,max,mean,std
	#band.ReadAsArray()
	if bands is None:
		#process all bands in the directory.
		fns = glob.glob(inDir + '*_B*.TIF')	
	else:
		#process the specified bands.
		fns = glob.glob(inDir + '*B[' + ','.join(str(i) for i in a) + '].TIF')

	#Read the first raster & get its band.	
	ras = gdal.Open(fns.pop(0))
	band = ras.GetRasterBand(1)
	
	#rows & cols		
	cols = ras.RasterXSize
	rows = ras.RasterYSize

	#raster info
	geo = ras.GetGeoTransform()
	originX = geo[0]
	originY = geo[3]
	pixelWidth = geo[1]
	pixelHeight = geo[5]
	
	#Create the output raster
	driver = gdal.GetDriverByName('GTiff')		
	outRas = driver.Create(outPath,cols,rows,len(fns) + 1,band.DataType)
	outRas.SetGeoTransform((originX,pixelWidth, 0, originY,0,pixelHeight)) #not sure what the zeros are
	
	#Get the spatial ref info
	outRasterSRS = osr.SpatialReference()
	outRasterSRS.ImportFromWkt(ras.GetProjectionRef())

	#Write the bands to the new file.
	outRas.GetRasterBand(1).WriteArray(band.ReadAsArray())

	#Loop thru any remaining files, adding them to the output. 
	for i in range(0,len(fns)):
		ras = gdal.Open(fns[i])
		band = ras.GetRasterBand(1)
		outRas.GetRasterBand(i+2).WriteArray(band.ReadAsArray())
	
	#Add the spatial ref info at the end.
	#NOTE: NEED TO DO SOMETHING TO FIX THE GEOTRANS MAT
	outRas.SetProjection(outRasterSRS.ExportToWkt())
	#write and close the output file.
	outRas.FlushCache()
	outRas = None

def world2Pixel(geoMatrix, x, y):
	"""
	Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
	the pixel location of a geospatial coordinate
	(NOTE: THIS WAS TAKEN DIRECTLY FROM https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html FOR USE IN clip_raster)
	"""
	ulX = geoMatrix[0]
	ulY = geoMatrix[3]
	xDist = geoMatrix[1]
	yDist = geoMatrix[5]
	rtnX = geoMatrix[2]
	rtnY = geoMatrix[4]
	#pixel = int((x - ulX) / xDist)
	#line = int((ulY - y) / xDist)
	#Floor for x and ceiling for y seems to produce the best looking output
	#	(for one test case, may want to change later to np.round?)
	pixx = np.round((x-ulX) / xDist,decimals=0).astype(np.int)
	pixy = np.round((ulY-y) / xDist,decimals=0).astype(np.int)
	return (pixx, pixy)
  
def Pixel2World(geoMatrix,x,y):
	"""
	Converts pixel coordinates to wold coordinates. 
	NOTE: TAKEN DIRECTLY FROM: http://stackoverflow.com/questions/13444015/python-code-review-for-a-function-to-clip-a-raster-image-with-a-polygon
	"""
	ulX = geoMatrix[0]
	ulY = geoMatrix[3]
	xdist = geoMatrix[1]
	ydist = geoMatrix[5]
	coorX = (ulX + (x * xdist))
	coorY = (ulY + (y * ydist))
	return (coorX, coorY)
    
def clip_raster(inRaster,outRaster,inShape):
	"""
	Clips the input raster to the input shapefile and saves the result to the output raster.
	Inspired in part by http://geospatialpython.com/2011/02/clip-raster-using-shapefile.html
	
	Arguments: 
		inRaster: full path to the raster that will be clipped. 
		outRaster: full path to clipped raster
		inShape: full path to shapefile used to clip inRaster.
			inShape should contain one polygon layer.
	Output:
		A clipped .TIF file.
	"""
	#Open the raster datasethttp://www.reuters.com/article/2015/06/05/us-cybersecurity-usa-idUSKBN0OK2IK20150605. 
	ras = gdal.Open(inRaster)
	
	#Get metadata 
	md = ras.GetMetadata()
	
	#Get the nodata value
	nodata = ras.GetRasterBand(1).GetNoDataValue()
	
	#Get the raster's geotransformation info
	geoTrans = ras.GetGeoTransform()
	
	#Open the shapefile & extract the layer.
	shp = ogr.Open(inShape)
	shpName = os.path.split(os.path.splitext(inShape)[0])[1]
	lyr = shp.GetLayer(shpName)
	
	#Get the polygon from the shapefile's first layer	
	poly = lyr.GetNextFeature() 
	
	#Now get the geometry
	geom = poly.GetGeometryRef()
	
	#Transform the shapefile to the raster's projection. 
	destSrs = osr.SpatialReference()
	destSrs.ImportFromWkt(ras.GetProjectionRef())
	geom.TransformTo(destSrs)
	
	#Get the layer's extent. This will be the size of the output raster.
	xs = []; ys = []
	pts = geom.GetGeometryRef(0)
	for p in range(pts.GetPointCount()):
		xs.append(pts.GetX(p))
		ys.append(pts.GetY(p))
		
	minX = min(xs); maxX = max(xs)
	minY = min(ys); maxY = max(ys)
	ulX, ulY = world2Pixel(geoTrans,minX,maxY)
	lrX, lrY = world2Pixel(geoTrans,maxX,minY)

	#Now get the raster values as numpy array
	rasArray = ras.ReadAsArray() #[bands, rows, columns]
	
	#Clip the raster array to the shape layer's extent
	clip = rasArray[:,ulY:lrY,ulX:lrX]  
	
	#Create a new geomatrix for the image
	minXPixel,maxYPixel = Pixel2World(geoTrans,ulX,ulY)
	geoTrans = list(geoTrans)
	geoTrans[0] = minXPixel
	geoTrans[3] = maxYPixel
	
	#Map the polygon's verticies to pixels and create a mask 
	pixels = []
	for p in range(pts.GetPointCount()):
		pixels.append(world2Pixel(geoTrans,xs[p],ys[p]))

	
	#Create the mask.
	rasterPoly = Image.new("L", (int(clip.shape[2]),int(clip.shape[1])),1)
	rasterize = ImageDraw.Draw(rasterPoly)
	rasterize.polygon(pixels,0)

	mask = np.asarray(rasterPoly)
	
	#Now clip the image to the mask. 
	clip = np.choose(mask,(clip,0))#.astype(ras.GetRasterBand(1).DataType)
	
	#Save the clipped raster.
	driver = gdal.GetDriverByName('GTiff')
	outRas = driver.Create(outRaster,clip.shape[2],clip.shape[1],clip.shape[0],ras.GetRasterBand(1).DataType)
	for i in range(1,clip.shape[0] + 1):
		outRas.GetRasterBand(i).WriteArray(clip[i-1,:,:])
		if nodata:
			outRas.GetRasterBand(i).SetNoDataValue(nodata)
		
	outRas.SetProjection(destSrs.ExportToWkt())
	outRas.SetGeoTransform(geoTrans)
	outRas.SetMetadata(md)
	#Write and close the clipped raster.
	outRas.FlushCache()
	outRas = None
	
def batch_stack_clip(indir,outdir,shape):
	"""
	Batch stacks and clips the images found with in a directory 
		to the given shapefile. 
		
	This function was created mostly for testing purposes. 
		probably more efficient to clip then stack? 
		
	Arguments:
		indir: Directory containing subdirectories containing
			unpacked landsat archives.
		outdir: Directory in which to place stacked and clipped .TIF files.
			Stacked TIFs named after landsat ID. Clipped TIFs named ater 
			landsat ID + _CLIP.TIF
			
		shape: Full path to shapefile with which to clip the input rasters
			using clip_raster()
			
	Output:
		Landsat images that have been stacked and clipped, placed in
			subfolders of the outdir directory named after the original 
			landsat base filename. 
			
	"""
	walk = os.walk(indir)
	names = walk.next()[1]
	for name in names:
		stackpath = outdir + name + '.TIF'
		clippath = outdir + name + '_CLIP.TIF'
		stack_layers(indir + name +'/',stackpath)
		clip_raster(stackpath,clippath,shape)
		print(name + ' stacked and clipped')
	
