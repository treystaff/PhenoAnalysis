import arcpy
import sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

rx = (sys.argv[1])
ry = (sys.argv[2])
rz = (sys.argv[3])
outd = (sys.argv[4])

inras = rx+";"+ry+"/Band_1"

arcpy.CompositeBands_management(inras,rz)

rz1 = arcpy.Raster(rz+"/Band_1")
rz2 = arcpy.Raster(rz+"/Band_2")
rz3 = arcpy.Raster(rz+"/Band_3")
rz4 = arcpy.Raster(rz+"/Band_4")

mask = "D:/Phenocam/Mask/Mask.shp"

mrz1 = ExtractByMask(rz1,mask)
mrz2 = ExtractByMask(rz2,mask)
mrz3 = ExtractByMask(rz3,mask)
mrz4 = ExtractByMask(rz4,mask)

outNDVI = outd+"NDVI.tif"
outEVI = outd+"EVI.tif"
outGCC = outd+"GCC.tif"

coutNDVI = ((mrz4-mrz1)/(mrz4+mrz1))

coutEVI = ((mrz4-mrz1)/(mrz4+6*mrz1-7.5*mrz3+1))

coutGCC = (mrz2/(mrz1+mrz2+mrz3))

coutNDVI.save(outNDVI)
coutEVI.save(outEVI)
coutGCC.save(outGCC)

RMeanNDVI = arcpy.GetRasterProperties_management(outNDVI, "MEAN")
RSTDNDVI = arcpy.GetRasterProperties_management(outNDVI, "STD")

MeanNDVI = RMeanNDVI.getOutput(0)
STDNDVI = RSTDNDVI.getOutput(0)

RMeanEVI = arcpy.GetRasterProperties_management(outEVI, "MEAN")
RSTDEVI = arcpy.GetRasterProperties_management(outEVI, "STD")

MeanEVI = RMeanEVI.getOutput(0)
STDEVI = RSTDEVI.getOutput(0)

RMeanGCC = arcpy.GetRasterProperties_management(outGCC, "MEAN")
RSTDGCC = arcpy.GetRasterProperties_management(outGCC, "STD")

MeanGCC = RMeanGCC.getOutput(0)
STDGCC = RSTDGCC.getOutput(0)

textfile = open(outd+"Index.txt","w")
textfile.write("NDVI: "+"Mean: "+MeanNDVI+" STD: "+STDNDVI+"\nEVI: "+"Mean: "+MeanEVI+" STD: "+STDEVI+"\nGCC: "+"Mean: "+MeanGCC+" STD: "+STDGCC)
textfile.close()
