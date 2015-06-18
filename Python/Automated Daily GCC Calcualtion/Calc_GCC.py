import arcpy
import sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

rin = (sys.argv[1])
rout = (sys.argv[2])

rz1 = arcpy.Raster(rin+"/Band_1")
rz2 = arcpy.Raster(rin+"/Band_2")
rz3 = arcpy.Raster(rin+"/Band_3")

mask = "D:/Phenocam/Mask/Mask.shp"

mrz1 = ExtractByMask(rz1,mask)
mrz2 = ExtractByMask(rz2,mask)
mrz3 = ExtractByMask(rz3,mask)

outGCC = rout

coutGCC = (mrz2/(mrz1+mrz2+mrz3))

coutGCC.save(outGCC)
