import arcpy
import numpy
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

count = 1
Ntime = "0000"
dailyperc = 0
mask = r"D:\Phenocam\Mask\Mask.shp"
inputraster = (sys.argv[1])
output = (sys.argv[2])

while (count <= 24):

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

    raster = r"" + inputraster + Ntime + ".jpg"

    BandRed = raster + "\Band_1"
    BandGreen = raster + "\Band_2"
    BandBlue = raster + "\Band_3"

    mBandRed = ExtractByMask(BandRed,mask)
    mBandGreen = ExtractByMask(BandGreen,mask)
    mBandBlue = ExtractByMask(BandBlue,mask)

    arrRed = numpy.float32(numpy.ndarray.flatten(arcpy.RasterToNumPyArray(mBandRed,"","","","")))
    arrGreen = numpy.float32(numpy.ndarray.flatten(arcpy.RasterToNumPyArray(mBandGreen,"","","","")))
    arrBlue = numpy.float32(numpy.ndarray.flatten(arcpy.RasterToNumPyArray(mBandBlue,"","","","")))

    del mBandRed
    del mBandGreen
    del mBandBlue

    arrGCC = numpy.float32(arrGreen + arrRed)
    arrGCC = numpy.float32(arrGCC + arrBlue)
    arrGCC = numpy.float32(numpy.divide(arrGreen,arrGCC))

    arrayperc = float(numpy.percentile(arrGCC, 90))

    dailyperc = numpy.float32(numpy.append(arrGCC,dailyperc))
    print arrayperc
    print len(dailyperc)

dailyperc = float(numpy.percentile(dailyperc, 90))

print ("90th percentile: " + str(dailyperc)+ "\n")

textfile = open(r""+output+"\GCC Calcualtion.txt","w")
textfile.write("GCC: " + str(dailyperc))
textfile.close()
