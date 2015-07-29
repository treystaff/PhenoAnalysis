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

Dependencies: gdal, numpy, scipy, ogr
"""

# MOST ALL OF THIS CODE DERIVED FROM: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
import tarfile
import glob
import gdal
import osr
import ogr
import Image
import ImageDraw
import os
import pdb
import numpy as np
import re
import traceback
import datetime
import tempfile

# Make this globally true. GDAL only prints error messages otherwise.
gdal.UseExceptions()


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
            if "=" in line:  # Get only key-value pairs
                l = line.split("=")
                metadata[l[0].strip()] = l[1].strip()

    return metadata


def unpack_landsat(inpath, outpath, bands=None, clouds=None):
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

        #Get the names of the members of the archive
        names = tfile.getnames()

        #Make sure the bands are given as a list
        bands = list(bands)

        #Find those elements of the archive that match the bands specified
        #	(plus metadata file)
        members = tfile.getmembers()
        elements = []
        blist = ''.join(str(i) for i in bands)
        if clouds:
            patternStr = '.*_B[' + blist + ']\.TIF|.*_MTL.txt|.*_band[' + blist + \
                         ']\.tif|.*_cfmask.*\.tif|.*\.xml|.*cloud.*\.tif'
        else:
            patternStr = '.*_B[' + blist + ']\.TIF|.*_MTL.txt|.*_band[' + blist + \
                         ']\.tif|.*_cfmask.*\.tif|.*\.xml'

        pattern = re.compile(patternStr)
        for i, name in enumerate(names):
            if pattern.match(name):
                    elements.append(members[i])
        tfile.extractall(outpath,members = elements)

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


def unpack_dir(indir, outdir, bands=None, clouds=None):
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
        # Determine the outpath directory name for the unpacked landsat archive
        unpackDir = outdir + os.path.splitext(os.path.split(
            os.path.splitext(archive)[0])[1])[0]

        # Check if the directory already exists and make it if it doesn't
        if not os.path.exists(unpackDir):
            os.makedirs(unpackDir)

        # Unpack the current archive.
        unpack_landsat(archive, unpackDir, bands=bands,clouds=clouds)

        # Let the user know how progress is going.
        print(archive + ' unpacked (' + str(idx + 1) + ' of ' + str(count) + ')')


def stack_layers(inDir, outPath, bands=None):
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
    # band = ds.GetRasterBand(1)
    # band.GetStatistics(True,True) - returns min,max,mean,std
    # band.ReadAsArray()
    try:
        fns = []
        if bands is None:
            # process all bands in the directory.
            bandtypes = ('*_B*.TIF','*band*.tif')
            for bandtype in bandtypes:
                fns.extend(glob.glob(inDir + bandtype))
        else:
            # process the specified bands.
            blist = '[' + ','.join(str(i) for i in bands) + ']'
            bandtypes = ('*B' + blist + '.TIF', '*band' + blist + '.tif')
            for bandtype in bandtypes:
                fns.extend(glob.glob(inDir + bandtype))

        # Read the first raster & get its band.
        fns.sort()
        fn = fns.pop(0)

        ras = gdal.Open(fn)

        band = ras.GetRasterBand(1)

        # rows & cols
        cols = ras.RasterXSize
        rows = ras.RasterYSize

        # raster info
        geo = ras.GetGeoTransform()
        originX = geo[0]
        originY = geo[3]
        pixelWidth = geo[1]
        pixelHeight = geo[5]

        # Create the output raster
        driver = gdal.GetDriverByName('GTiff')
        outRas = driver.Create(outPath, cols, rows, len(fns) + 1, band.DataType)
        outRas.SetGeoTransform(geo)
        #outRas.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))  # not sure what the zeros are

        # Get the spatial ref info
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromWkt(ras.GetProjectionRef())

        # Write the bands to the new file.
        outRas.GetRasterBand(1).WriteArray(band.ReadAsArray())

        # Loop thru any remaining files, adding them to the output.
        for i in range(0, len(fns)):
            ras = gdal.Open(fns[i])
            band = ras.GetRasterBand(1)
            outRas.GetRasterBand(i + 2).WriteArray(band.ReadAsArray())

        # Add the spatial ref info at the end.
        outRas.SetProjection(outRasterSRS.ExportToWkt())
        # write and close the output file.
        outRas.FlushCache()
        outRas = None
    except RuntimeError:
        print 'ERROR PROCESSING ' + fn
        traceback.print_exc()
        return


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
    # pixel = int((x - ulX) / xDist)
    # line = int((ulY - y) / xDist)
    # Floor for x and ceiling for y seems to produce the best looking output
    #	(for one test case, may want to change later to np.round?)
    pixx = np.round((x - ulX) / xDist, decimals=0).astype(np.int)
    pixy = np.round((ulY - y) / xDist, decimals=0).astype(np.int)

    return pixx, pixy


def Pixel2World(geoMatrix, x, y):
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


def clip_raster(inRaster, outRaster, inShape):
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
    # Open the raster dataset
    ras = gdal.Open(inRaster)

    # Get metadata
    md = ras.GetMetadata()

    # Get the nodata value
    nodata = ras.GetRasterBand(1).GetNoDataValue()

    # Get the raster's geotransformation info
    geoTrans = ras.GetGeoTransform()

    # Open the shapefile & extract the layer.
    if not os.path.isfile(inshape):
        raise IOError('SHAPEFILE DOES NOT EXIST.')
    shp = ogr.Open(inShape)
    shpName = os.path.split(os.path.splitext(inShape)[0])[1]
    lyr = shp.GetLayer(shpName)

    # Get the polygon from the shapefile's first layer
    poly = lyr.GetNextFeature()

    # Now get the geometry
    geom = poly.GetGeometryRef()

    # Transform the shapefile to the raster's projection.
    destSrs = osr.SpatialReference()
    destSrs.ImportFromWkt(ras.GetProjectionRef())
    geom.TransformTo(destSrs)

    # Get the layer's extent. This will be the size of the output raster.
    xs = []
    ys = []
    pts = geom.GetGeometryRef(0)
    for p in range(pts.GetPointCount()):
        xs.append(pts.GetX(p))
        ys.append(pts.GetY(p))

    minX = min(xs)
    maxX = max(xs)
    minY = min(ys)
    maxY = max(ys)
    ulX, ulY = world2Pixel(geoTrans, minX, maxY)
    lrX, lrY = world2Pixel(geoTrans, maxX, minY)

    # Give a bit of extra room for shapes that approximate the layer's extent (squares).
    ulX -= 1
    ulY -= 1
    lrX += 1
    lrY += 1

    # Now get the raster values as numpy array
    rasArray = ras.ReadAsArray()  # [bands, rows, columns]

    # Clip the raster array to the shape layer's extent
    if len(rasArray.shape) == 2:
        clip = rasArray[ulY:lrY, ulX:lrX]
        rows = clip.shape[0]
        cols = clip.shape[1]
        bands = 1
    else:
        clip = rasArray[:, ulY:lrY, ulX:lrX]
        rows = clip.shape[1]
        cols = clip.shape[2]
        bands = clip.shape[0]

    # Create a new geomatrix for the image
    minXPixel, maxYPixel = Pixel2World(geoTrans, ulX, ulY)
    geoTrans = list(geoTrans)
    geoTrans[0] = minXPixel
    geoTrans[3] = maxYPixel

    # Rasterize the polygon layer to create a mask
    mask = rasterize_vector(inShape, rows, cols, geoTrans, transform=destSrs)

    # Now clip the image to the mask.
    if nodata:
        clip = np.choose(mask, (clip, nodata))
    else:
        print('WARNING: NO DEFINED NODATA VALUE. USING -9999 INSTEAD.')
        clip = np.choose(mask, (clip, -9999))
        nodata = -9999

    # Save the clipped raster.
    driver = gdal.GetDriverByName('GTiff')
    outRas = driver.Create(outRaster, cols, rows, bands, ras.GetRasterBand(1).DataType)
    if bands > 1:
        for i in range(1, bands + 1):
            outRas.GetRasterBand(i).WriteArray(clip[i - 1, :, :])
            if nodata:
                outRas.GetRasterBand(i).SetNoDataValue(nodata)
    else:
        outRas.GetRasterBand(1).WriteArray(clip)
        if nodata:
            outRas.GetRasterBand(1).SetNoDataValue(nodata)

    outRas.SetProjection(destSrs.ExportToWkt())
    outRas.SetGeoTransform(geoTrans)
    outRas.SetMetadata(md)
    # Write and close the clipped raster.
    outRas.FlushCache()
    outRas = None


def batch_stack_clip(indir, outdir, shape,bands=None,mask_band=False, remove_stack=False):
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
        bands: List of bands to clip and stack (numbers, e.g., [1,2,3,4])
        mask_band: Clip the cf_mask band included with surface reflectance product.
        remove_stack: (optional). removes the unclipped stacked image (saves space if only using clipped version.

    Output:
        Landsat images that have been stacked and clipped, placed in
            subfolders of the outdir directory named after the original
            landsat base filename.

    """
    walk = os.walk(indir)
    names = walk.next()[1]
    for name in names:
        # Clip and stack the specified bands
        stackpath = outdir + name + '.TIF'
        clippath = outdir + name + '_CLIP.TIF'
        stack_layers(indir + name + '/', stackpath, bands=bands)
        clip_raster(stackpath, clippath, shape)
        # Optionally move the stacked raster
        if remove_stack:
            os.remove(stackpath)

        # Optionally clip the mask band.
        if mask_band:
            cloud_path = os.path.join(indir, name)
            try:
                cloud_path = glob.glob(cloud_path + '/*cfmask.tif')[0]
                cloud_clip_path = outdir + name + '_cfmask_CLIP.tif'
                clip_raster(cloud_path, cloud_clip_path, shape)
            except IndexError:
                print('WARNING: NO CFMASK FOUND FOR ' + cloud_path)

        print(name + ' stacked and clipped')


def cfmask_to_mask(raster):
    """Converts a landsat cfmask raster to a numpy mask that can be used w/ maskedarray"""
    mask = raster.ReadAsArray()
    # A value of 0 is clear of clouds/water. Make all other values = 1.
    mask[mask != 0] = 1

    # That's it, just return the result...
    return mask


def filename2date(filename):
    """
    Extracts date from Landsat SURFACE REFLECTANCE filenames and returns datetime object.
    Only SR filenames currently supported.
    """
    # Find the '-SC' in the filename.
    dash = filename.find('-SC')
    if dash:
        return datetime.datetime.strptime(filename[dash-7:dash], '%Y%j')
    else:
        raise ValueError('Landsat filename does not conform to expected format.')


def rasterize_vector(shp, rows, cols, geoTrans=None, saveto=None, method='within', transform=None):
    """
    Function for rasterizing a vector layer. Currently limited functionality
    Arguments:
        shp: Path to a shapefile containing polygon.
        rows: Number of rows the resulting raster will have
        cols: Number of columns the resulting raster will have
        geoTrans: (Eventually optional, but not yet...) GeoTransformation matrix for output raster
        saveto: (optional) path to save the raster as a .tif file to.
        method: (optional: default='within'). Determines method for rasteriziation. 'within' includes
            pixels that have centers that fall within the polygon. 'touches' includes all pixels that touch
            the vector layer.
    Returns:
        A numpy array representing the rasterized vector layer
    """
    # Open the shapefile
    shp = ogr.Open(shp)

    # Get the layer from the shape
    layer = shp.GetLayer()

    # Get the layer's information
    lyrSrs = layer.GetSpatialRef().ExportToWkt()

    # Optionally transform to specified transformation
    if transform and transform.ExportToWkt() != lyrSrs:
        # Get the layer geometry
        poly = layer.GetNextFeature()
        geom = poly.GetGeometryRef()

        # Transform the geometry.
        geom.TransformTo(transform)

        # Create a new layer.
        lyr_driver = ogr.GetDriverByName('ESRI Shapefile')

        lyr_driver_name = tempfile.NamedTemporaryFile(suffix='.shp').name
        lyr_source = lyr_driver.CreateDataSource(lyr_driver_name)
        new_lyr = lyr_source.CreateLayer(lyr_driver_name, transform, geom_type=ogr.wkbPolygon)

        # Add an ID field to tie the geometry to
        id_field = ogr.FieldDefn('id', ogr.OFTInteger)
        new_lyr.CreateField(id_field)

        # Set the transformed geometry
        feature_defn = new_lyr.GetLayerDefn()
        feature = ogr.Feature(feature_defn)
        feature.SetGeometry(geom)
        feature.SetField('id',1)
        new_lyr.CreateFeature(feature)

        # Set the existing layer to be the new layer
        layer = new_lyr
        lyrSrs = transform.ExportToWkt()

    # Create the raster's name
    if not saveto:
        remove = True
        saveto = tempfile.NamedTemporaryFile(suffix='.tif')
        saveto = saveto.name
    else:
        remove = False

    # Create the new raster
    driver = gdal.GetDriverByName('GTiff')
    outRas = driver.Create(saveto, cols, rows, 1)
    outRas.SetProjection(lyrSrs)
    outRas.SetGeoTransform(geoTrans)
    outRas.GetRasterBand(1).Fill(1)

    # Rasterize the layer
    if method.lower() == 'touches':
        gdal.RasterizeLayer(outRas,[1],layer,None, None, [0], ['ALL_TOUCHED=TRUE'])
    else:  # Just default to this.
        gdal.RasterizeLayer(outRas,[1],layer,None, None, [0])
    arr = outRas.ReadAsArray()
    if remove:
        os.remove(saveto)

    # Return the numpy array
    return arr
