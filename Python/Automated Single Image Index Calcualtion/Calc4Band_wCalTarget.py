import arcpy
import sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

rx = (sys.argv[1]) # color image
ry = (sys.argv[2]) # IR image
rz = (sys.argv[3]) # Output 4 Band Image
outd = (sys.argv[4]) # Output Directory\

inras = rx+";"+ry+"/Band_1"

arcpy.CompositeBands_management(inras,rz)

rz1 = arcpy.Raster(rz+"/Band_1")
rz2 = arcpy.Raster(rz+"/Band_2")
rz3 = arcpy.Raster(rz+"/Band_3")
rz4 = arcpy.Raster(rz+"/Band_4")

mask = "C:/Phenocam/Mask/Oakville_Mask.shp" #Extraction mask for imagery
calmask = "C:/Phenocam/Mask/Oakville_CalibrationTarget_Mask.shp" # Extraction mask of calibration target

mrz1 = ExtractByMask(rz1,mask)
mrz2 = ExtractByMask(rz2,mask)
mrz3 = ExtractByMask(rz3,mask)
mrz4 = ExtractByMask(rz4,mask)

calmrz1 = ExtractByMask(rz1,calmask)
calmrz2 = ExtractByMask(rz2,calmask)
calmrz3 = ExtractByMask(rz3,calmask)
calmrz4 = ExtractByMask(rz4,calmask)

CalRedMean = arcpy.GetRasterProperties_management(calmrz1, "MEAN")
CalGreenMean = arcpy.GetRasterProperties_management(calmrz2, "MEAN")
CalBlueMean = arcpy.GetRasterProperties_management(calmrz3, "MEAN")
CalIRMean = arcpy.GetRasterProperties_management(calmrz4, "MEAN")

CalRedMean = CalRedMean.getOutput(0)
CalGreenMean = CalGreenMean.getOutput(0)
CalBlueMean = CalBlueMean.getOutput(0)
CalIRMean = CalIRMean.getOutput(0)

mrz1 = mrz1/float(CalRedMean)*27.738
mrz2 = mrz2/float(CalGreenMean)*28.172
mrz3 = mrz3/float(CalBlueMean)*26.562
mrz4 = mrz4/float(CalIRMean)*23.670

textfile = open(outd+"Log Cal Target Value.txt","w")
textfile.write("Red: "+str(float(CalRedMean))+"\nGreen: "+str(float(CalGreenMean))+"\nBlue: "+str(float(CalBlueMean))+"\nIR: "+str(float(CalIRMean)))
textfile.close()

SaveBand1 = outd+"Band1.tif"
mrz1.save(SaveBand1)
SaveBand2 = outd+"Band2.tif"
mrz2.save(SaveBand2)
SaveBand3 = outd+"Band3.tif"
mrz3.save(SaveBand3)
SaveBand4 = outd+"Band4.tif"
mrz4.save(SaveBand4)

mrz1 = arcpy.Raster(SaveBand1)
mrz2 = arcpy.Raster(SaveBand2)
mrz3 = arcpy.Raster(SaveBand3)
mrz4 = arcpy.Raster(SaveBand4)

CalibratedImage = outd+"CalibratedImage.tif"

inras = SaveBand1+";"+SaveBand2+";"+SaveBand3+";"+SaveBand4
arcpy.CompositeBands_management(inras,CalibratedImage)

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
textfile.write("NDVI: "+"Mean: "+str(float(MeanNDVI))+" STD: "+str(float(STDNDVI))+"\nEVI: "+"Mean: "+str(float(MeanEVI))+" STD: "+str(float(STDEVI))+"\nGCC: "+"Mean: "+str(float(MeanGCC))+" STD: "+str(float(STDGCC)))
textfile.close()

arcpy.Delete_management(SaveBand1)
arcpy.Delete_management(SaveBand2)
arcpy.Delete_management(SaveBand3)
arcpy.Delete_management(SaveBand4)
