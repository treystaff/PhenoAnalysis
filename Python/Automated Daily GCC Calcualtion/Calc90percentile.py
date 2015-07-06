"""

This script is to be used for the phenocam project.
Created by Morgen Burke

This script is going to calcualte the daily gcc value using 24 color images collected during the day, the input
images must be input as the first agrument correctly so that the script can run through all 24 images
starting with image taken at 7:00 and then every consecutive image every half hour untill image 18:30.

"""
import arcpy # requires ArcGIS
import numpy # used to compute arrays
arcpy.CheckOutExtension("Spatial") # requires spatial analyst in ArcGIS
from arcpy.sa import * 

count = 1 # used to count through the processing of all 24 images
Ntime = "0000" # holds the time of the current image being processed
dailyperc = 0 # holds the 90th percentile value for the day
mask = r"C:\Phenocam\Mask\Mask.shp" # the maks used to extract the imagery region of interest
inputraster = (sys.argv[1]) # the input raster images location using c:/location/filename_Ntime.jpg (Ntime.jpg are calcualted atomatically)
output = (sys.argv[2]) # the output location for output GCC calcualtion

while (count <= 24): # while loops through all 24 images

    if (count == 1):
        Ntime = "0700"
    elif (count == 2):
        Ntime = "0730"
    elif (count == 3):
        Ntime = "0800"
    elif (count == 4):
        Ntime = "0830"
    elif (count == 5):
        Ntime = "0900"
    elif (count == 6):
        Ntime = "0930"
    elif (count == 7):
        Ntime = "1000"
    elif (count == 8):
        Ntime = "1030"
    elif (count == 9):
        Ntime = "1100"
    elif (count == 10):
        Ntime = "1130"
    elif (count == 11):
        Ntime = "1200"
    elif (count == 12):
        Ntime = "1230"
    elif (count == 13):
        Ntime = "1300"
    elif (count == 14):
        Ntime = "1330"
    elif (count == 15):
        Ntime = "1400"
    elif (count == 16):
        Ntime = "1430"
    elif (count == 17):
        Ntime = "1500"
    elif (count == 18):
        Ntime = "1530"
    elif (count == 19):
        Ntime = "1600"
    elif (count == 20):
        Ntime = "1630"
    elif (count == 21):
        Ntime = "1700"
    elif (count == 22):
        Ntime = "1730"
    elif (count == 23):
        Ntime = "1800"
    elif (count == 24):
        Ntime = "1830"
    count = count + 1

    raster = r"" + inputraster + Ntime + ".jpg" #used to determine the file path of the image being computed

    BandRed = raster + "\Band_1" #the red band of the current raster
    BandGreen = raster + "\Band_2" #the green band of the current raster
    BandBlue = raster + "\Band_3" #the blue band of the current raster

    # extract the ROI from the 3 bands
    mBandRed = ExtractByMask(BandRed,mask)
    mBandGreen = ExtractByMask(BandGreen,mask)
    mBandBlue = ExtractByMask(BandBlue,mask)

    # turn 3 bands into arrays of each pixel value
    arrRed = numpy.float32(numpy.ndarray.flatten(arcpy.RasterToNumPyArray(mBandRed,"","","","")))
    arrGreen = numpy.float32(numpy.ndarray.flatten(arcpy.RasterToNumPyArray(mBandGreen,"","","","")))
    arrBlue = numpy.float32(numpy.ndarray.flatten(arcpy.RasterToNumPyArray(mBandBlue,"","","","")))

    # delete the extracted ROI bands
    del mBandRed
    del mBandGreen
    del mBandBlue

    # calcualte GCC for current image
    arrGCC = numpy.float32(arrGreen + arrRed)
    arrGCC = numpy.float32(arrGCC + arrBlue)
    arrGCC = numpy.float32(numpy.divide(arrGreen,arrGCC))

    # find 90th percentile of current image
    arrayperc = float(numpy.percentile(arrGCC, 90))

    #append current image array to a list of all image arrays to calcualte daily GCC 90th percentile from
    dailyperc = numpy.float32(numpy.append(arrGCC,dailyperc))
    print arrayperc # give user output of current image 90th percentile GCC
    print len(dailyperc) # print the number of pixel values in daily GCC array

# output the daily GCC array as a text file to be used in three day averages
textfile = r""+output+"\Daily_GCC_90Perc_Array.npy"
numpy.save(textfile, dailyperc)

# calcualte 90th percentile of daily GCC
dailyperc = float(numpy.percentile(dailyperc, 90))

print ("90th percentile: " + str(dailyperc)+ "\n") #print daily GCC 90th percentile to user

# output daily 90th percentile GCC calcualtion
textfile = open(r""+output+"\GCC Calcualtion.txt","w")
textfile.write("GCC: " + str(dailyperc))
textfile.close()

