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

inras = rin+"0700.tif;"+rin+"0730.tif;"+rin+"0800.tif;"+rin+"0830.tif;"+rin+"0900.tif;"+rin+"0930.tif;"+rin+"1000.tif;"+rin+"1030.tif;"+rin+"1100.tif;"+rin+"1130.tif;"+rin+"1200.tif;"+rin+"1230.tif;"+rin+"1300.tif;"+rin+"1330.tif;"+rin+"1400.tif;"+rin+"1430.tif;"+rin+"1500.tif;"+rin+"1530.tif;"+rin+"1600.tif;"+rin+"1630.tif;"+rin+"1700.tif;"+rin+"1730.tif;"+rin+"1800.tif;"+rin+"1830.tif"
outGCC = dout+"DailyMean.tif"

arcpy.CompositeBands_management(inras,outGCC)

RMeanGCC1 = arcpy.GetRasterProperties_management(rz1, "MEAN")
RSTDGCC1 = arcpy.GetRasterProperties_management(rz1, "STD")
MeanGCC1 = RMeanGCC1.getOutput(0)
STDGCC1 = RSTDGCC1.getOutput(0)

RMeanGCC2 = arcpy.GetRasterProperties_management(rz2, "MEAN")
RSTDGCC2 = arcpy.GetRasterProperties_management(rz2, "STD")
MeanGCC2 = RMeanGCC2.getOutput(0)
STDGCC2 = RSTDGCC2.getOutput(0)

RMeanGCC3 = arcpy.GetRasterProperties_management(rz3, "MEAN")
RSTDGCC3 = arcpy.GetRasterProperties_management(rz3, "STD")
MeanGCC3 = RMeanGCC3.getOutput(0)
STDGCC3 = RSTDGCC3.getOutput(0)

RMeanGCC4 = arcpy.GetRasterProperties_management(rz4, "MEAN")
RSTDGCC4 = arcpy.GetRasterProperties_management(rz4, "STD")
MeanGCC4 = RMeanGCC4.getOutput(0)
STDGCC4 = RSTDGCC4.getOutput(0)

RMeanGCC5 = arcpy.GetRasterProperties_management(rz5, "MEAN")
RSTDGCC5 = arcpy.GetRasterProperties_management(rz5, "STD")
MeanGCC5 = RMeanGCC5.getOutput(0)
STDGCC5 = RSTDGCC5.getOutput(0)

RMeanGCC6 = arcpy.GetRasterProperties_management(rz6, "MEAN")
RSTDGCC6 = arcpy.GetRasterProperties_management(rz6, "STD")
MeanGCC6 = RMeanGCC6.getOutput(0)
STDGCC6 = RSTDGCC6.getOutput(0)

RMeanGCC7 = arcpy.GetRasterProperties_management(rz7, "MEAN")
RSTDGCC7 = arcpy.GetRasterProperties_management(rz7, "STD")
MeanGCC7 = RMeanGCC7.getOutput(0)
STDGCC7 = RSTDGCC7.getOutput(0)

RMeanGCC8 = arcpy.GetRasterProperties_management(rz8, "MEAN")
RSTDGCC8 = arcpy.GetRasterProperties_management(rz8, "STD")
MeanGCC8 = RMeanGCC8.getOutput(0)
STDGCC8 = RSTDGCC8.getOutput(0)

RMeanGCC9 = arcpy.GetRasterProperties_management(rz9, "MEAN")
RSTDGCC9 = arcpy.GetRasterProperties_management(rz9, "STD")
MeanGCC9 = RMeanGCC9.getOutput(0)
STDGCC9 = RSTDGCC9.getOutput(0)

RMeanGCC10 = arcpy.GetRasterProperties_management(rz10, "MEAN")
RSTDGCC10 = arcpy.GetRasterProperties_management(rz10, "STD")
MeanGCC10 = RMeanGCC10.getOutput(0)
STDGCC10 = RSTDGCC10.getOutput(0)

RMeanGCC11 = arcpy.GetRasterProperties_management(rz11, "MEAN")
RSTDGCC11 = arcpy.GetRasterProperties_management(rz11, "STD")
MeanGCC11 = RMeanGCC11.getOutput(0)
STDGCC11 = RSTDGCC11.getOutput(0)

RMeanGCC12 = arcpy.GetRasterProperties_management(rz12, "MEAN")
RSTDGCC12 = arcpy.GetRasterProperties_management(rz12, "STD")
MeanGCC12 = RMeanGCC12.getOutput(0)
STDGCC12 = RSTDGCC12.getOutput(0)

RMeanGCC13 = arcpy.GetRasterProperties_management(rz13, "MEAN")
RSTDGCC13 = arcpy.GetRasterProperties_management(rz13, "STD")
MeanGCC13 = RMeanGCC13.getOutput(0)
STDGCC13 = RSTDGCC13.getOutput(0)

RMeanGCC14 = arcpy.GetRasterProperties_management(rz14, "MEAN")
RSTDGCC14 = arcpy.GetRasterProperties_management(rz14, "STD")
MeanGCC14 = RMeanGCC14.getOutput(0)
STDGCC14 = RSTDGCC14.getOutput(0)

RMeanGCC15 = arcpy.GetRasterProperties_management(rz15, "MEAN")
RSTDGCC15 = arcpy.GetRasterProperties_management(rz15, "STD")
MeanGCC15 = RMeanGCC15.getOutput(0)
STDGCC15 = RSTDGCC15.getOutput(0)

RMeanGCC16 = arcpy.GetRasterProperties_management(rz16, "MEAN")
RSTDGCC16 = arcpy.GetRasterProperties_management(rz16, "STD")
MeanGCC16 = RMeanGCC16.getOutput(0)
STDGCC16 = RSTDGCC16.getOutput(0)

RMeanGCC17 = arcpy.GetRasterProperties_management(rz17, "MEAN")
RSTDGCC17 = arcpy.GetRasterProperties_management(rz17, "STD")
MeanGCC17 = RMeanGCC17.getOutput(0)
STDGCC17 = RSTDGCC17.getOutput(0)

RMeanGCC18 = arcpy.GetRasterProperties_management(rz18, "MEAN")
RSTDGCC18 = arcpy.GetRasterProperties_management(rz18, "STD")
MeanGCC18 = RMeanGCC18.getOutput(0)
STDGCC18 = RSTDGCC18.getOutput(0)

RMeanGCC19 = arcpy.GetRasterProperties_management(rz19, "MEAN")
RSTDGCC19 = arcpy.GetRasterProperties_management(rz19, "STD")
MeanGCC19 = RMeanGCC19.getOutput(0)
STDGCC19 = RSTDGCC19.getOutput(0)

RMeanGCC20 = arcpy.GetRasterProperties_management(rz20, "MEAN")
RSTDGCC20 = arcpy.GetRasterProperties_management(rz20, "STD")
MeanGCC20 = RMeanGCC20.getOutput(0)
STDGCC20 = RSTDGCC20.getOutput(0)

RMeanGCC21 = arcpy.GetRasterProperties_management(rz21, "MEAN")
RSTDGCC21 = arcpy.GetRasterProperties_management(rz21, "STD")
MeanGCC21 = RMeanGCC21.getOutput(0)
STDGCC21 = RSTDGCC21.getOutput(0)

RMeanGCC22 = arcpy.GetRasterProperties_management(rz22, "MEAN")
RSTDGCC22 = arcpy.GetRasterProperties_management(rz22, "STD")
MeanGCC22 = RMeanGCC22.getOutput(0)
STDGCC22 = RSTDGCC22.getOutput(0)


RMeanGCC23 = arcpy.GetRasterProperties_management(rz23, "MEAN")
RSTDGCC23 = arcpy.GetRasterProperties_management(rz23, "STD")
MeanGCC23 = RMeanGCC23.getOutput(0)
STDGCC23 = RSTDGCC23.getOutput(0)

RMeanGCC24 = arcpy.GetRasterProperties_management(rz24, "MEAN")
RSTDGCC24 = arcpy.GetRasterProperties_management(rz24, "STD")
MeanGCC24 = RMeanGCC24.getOutput(0)
STDGCC24 = RSTDGCC24.getOutput(0)


coutMeanGCC = ((float(MeanGCC1)+float(MeanGCC2)+float(MeanGCC3)+float(MeanGCC4)+float(MeanGCC5)+float(MeanGCC6)+float(MeanGCC7)+float(MeanGCC8)+float(MeanGCC9)+float(MeanGCC10)+float(MeanGCC11)+float(MeanGCC12)+float(MeanGCC13)+float(MeanGCC14)+float(MeanGCC15)+float(MeanGCC16)+float(MeanGCC17)+float(MeanGCC18)+float(MeanGCC19)+float(MeanGCC20)+float(MeanGCC21)+float(MeanGCC22)+float(MeanGCC23)+float(MeanGCC24))/24)

coutSTDGCC = ((float(STDGCC1)+float(STDGCC2)+float(STDGCC3)+float(STDGCC4)+float(STDGCC5)+float(STDGCC6)+float(STDGCC7)+float(STDGCC8)+float(STDGCC9)+float(STDGCC10)+float(STDGCC11)+float(STDGCC12)+float(STDGCC13)+float(STDGCC14)+float(STDGCC15)+float(STDGCC16)+float(STDGCC17)+float(STDGCC18)+float(STDGCC19)+float(STDGCC20)+float(STDGCC21)+float(STDGCC22)+float(STDGCC23)+float(STDGCC24))/24)

textfile = open(dout+"Index.txt","w")
textfile.write("GCC: "+"Mean: "+str(coutMeanGCC)+" STD: "+str(coutSTDGCC))
textfile.close()

