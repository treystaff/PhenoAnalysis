import arcpy
import sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

rin = (sys.argv[1])
dout = (sys.argv[2])

rz1 = arcpy.Raster(rin+"0700.tif")
rz2 = arcpy.Raster(rin+"0730.tif")
rz3 = arcpy.Raster(rin+"0800.tif")
rz4 = arcpy.Raster(rin+"0830.tif")
rz5 = arcpy.Raster(rin+"0900.tif")
rz6 = arcpy.Raster(rin+"0930.tif")
rz7 = arcpy.Raster(rin+"1000.tif")
rz8 = arcpy.Raster(rin+"1030.tif")
rz9 = arcpy.Raster(rin+"1100.tif")
rz10 = arcpy.Raster(rin+"1130.tif")
rz11 = arcpy.Raster(rin+"1200.tif")
rz12 = arcpy.Raster(rin+"1230.tif")
rz13 = arcpy.Raster(rin+"1300.tif")
rz14 = arcpy.Raster(rin+"1330.tif")
rz15 = arcpy.Raster(rin+"1400.tif")
rz16 = arcpy.Raster(rin+"1430.tif")
rz17 = arcpy.Raster(rin+"1500.tif")
rz18 = arcpy.Raster(rin+"1530.tif")
rz19 = arcpy.Raster(rin+"1600.tif")
rz20 = arcpy.Raster(rin+"1630.tif")
rz21 = arcpy.Raster(rin+"1700.tif")
rz22 = arcpy.Raster(rin+"1730.tif")
rz23 = arcpy.Raster(rin+"1800.tif")
rz24 = arcpy.Raster(rin+"1830.tif")

coutGCC = ((rz1+rz2+rz3+rz4+rz5+rz6+rz7+rz8+rz9+rz10+rz11+rz12+rz13+rz14+rz15+rz16+rz17+rz18+rz19+rz20+rz21+rz22+rz23+rz24)/24)

outGCC = dout+"DailyMean.tif"

coutGCC.save(outGCC)

RMeanGCC = arcpy.GetRasterProperties_management(outGCC, "MEAN")
RSTDGCC = arcpy.GetRasterProperties_management(outGCC, "STD")

MeanGCC = RMeanGCC.getOutput(0)
STDGCC = RSTDGCC.getOutput(0)

textfile = open(dout+"Index.txt","w")
textfile.write("GCC: "+"Mean: "+MeanGCC+" STD: "+STDGCC)
textfile.close()

