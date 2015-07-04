"""
This script was created to process imagery for the phenocam project.
Created by Morgen Burke

Used to take and input color and an input IR image and calcualte a composite 4 band image, then using two masks
one for the calibration target and one for the region of interest (ROI), the 4 band image is calibrated based on measured reflectance of the
calibration target. Finally NDVI, GCC, and EVI values are calcualted and output.
"""

import arcpy #requires ArcGIS 
import sys
arcpy.CheckOutExtension("Spatial") #requires ArcGIS spatial analyst extension
from arcpy.sa import *

#The required imput for this script are to be sent into the script as arguments typically from a .bat file
rx = (sys.argv[1]) # color image
ry = (sys.argv[2]) # IR image
rz = (sys.argv[3]) # Output 4 Band Image
outd = (sys.argv[4]) # Output Directory\

#the masks to be used to extract the calibration target and the ROI from the imagery
mask = "D:/Phenocam/Mask/Oakville_Mask.shp" #Extraction mask for imagery
calmask = "D:/Phenocam/Mask/Oakville_CalibrationTarget_Mask.shp" # Extraction mask of calibration target

#the calcualted percent reflectance values for the calibration target (will change from site to site)
RedReflect = float(27.738) # red reflectance 
GreenReflect = float(28.172) # green reflectance
BlueReflect = float(26.562) # blue reflectance
IRReflect = float(23.670) # IR reflectance

inras = rx+";"+ry+"/Band_1" # input color and IR images to composite into 4 band image

arcpy.CompositeBands_management(inras,rz) # ArcGIS composite images function

# Seperate 4 band image into individual bands
rz1 = arcpy.Raster(rz+"/Band_1") # red band
rz2 = arcpy.Raster(rz+"/Band_2") # green band
rz3 = arcpy.Raster(rz+"/Band_3") # blue band
rz4 = arcpy.Raster(rz+"/Band_4") # IR band

# extract the ROI from all four bands
mrz1 = ExtractByMask(rz1,mask) # red band ROI
mrz2 = ExtractByMask(rz2,mask) # green band ROI
mrz3 = ExtractByMask(rz3,mask) # blue band ROI
mrz4 = ExtractByMask(rz4,mask) # IR band ROI

# extract the Calibration Target from all four bands
calmrz1 = ExtractByMask(rz1,calmask) # red band Calibration Target
calmrz2 = ExtractByMask(rz2,calmask) # green band Calibration Target
calmrz3 = ExtractByMask(rz3,calmask) # blue band Calibration Target
calmrz4 = ExtractByMask(rz4,calmask) # IR band Calibration Target

# calcualte mean of the 4 bands calibration target
CalRedMean = arcpy.GetRasterProperties_management(calmrz1, "MEAN") # red band Calibration Target mean
CalGreenMean = arcpy.GetRasterProperties_management(calmrz2, "MEAN") # green band Calibration Target mean
CalBlueMean = arcpy.GetRasterProperties_management(calmrz3, "MEAN") # blue band Calibration Target mean
CalIRMean = arcpy.GetRasterProperties_management(calmrz4, "MEAN") # IR band Calibration Target mean

# get output from mean calcualtion
CalRedMean = CalRedMean.getOutput(0) # red band Calibration Target mean
CalGreenMean = CalGreenMean.getOutput(0) # green band Calibration Target mean
CalBlueMean = CalBlueMean.getOutput(0) # blue band Calibration Target mean
CalIRMean = CalIRMean.getOutput(0) # IR band Calibration Target mean

# correct 4 band imagery with calibration target means and calibration target percent reflectance
mrz1 = mrz1/float(CalRedMean)*float(RedReflect) # red band calibrated
mrz2 = mrz2/float(CalGreenMean)*float(GreenReflect) # green band calibrated
mrz3 = mrz3/float(CalBlueMean)*float(BlueReflect) # blue band calibrated
mrz4 = mrz4/float(CalIRMean)*float(IRReflect) # IR band calibrated

# output log file of clibration target means and percent reflectance values used
textfile = open(outd+"Log Cal Target Value.txt","w")
textfile.write("Calibration Target Mean Pixel Value \nRed: "+str(float(CalRedMean))+"\nGreen: "+str(float(CalGreenMean))+"\nBlue: "
               +str(float(CalBlueMean))+"\nIR: "+str(float(CalIRMean))+"\n \nCalcualted Calibration Target Percent Reflectance \nRed: "
               +str(RedReflect)+"\nGreen: "+str(GreenReflect)+"\nBlue: "
               +str(BlueReflect)+"\nIR: "+str(IRReflect))
textfile.close()

# save calibrated bands
SaveBand1 = outd+"Band1.tif"
mrz1.save(SaveBand1)
SaveBand2 = outd+"Band2.tif"
mrz2.save(SaveBand2)
SaveBand3 = outd+"Band3.tif"
mrz3.save(SaveBand3)
SaveBand4 = outd+"Band4.tif"
mrz4.save(SaveBand4)

# inport save calibrated bands
mrz1 = arcpy.Raster(SaveBand1)
mrz2 = arcpy.Raster(SaveBand2)
mrz3 = arcpy.Raster(SaveBand3)
mrz4 = arcpy.Raster(SaveBand4)

# location to save calibrated 4 band image
CalibratedImage = outd+"CalibratedImage.tif"

#location of the 4 calibrated bands
inras = SaveBand1+";"+SaveBand2+";"+SaveBand3+";"+SaveBand4
arcpy.CompositeBands_management(inras,CalibratedImage) #ArcGIS composite of calibrated image to save to file 

# location to save vegetation indexes
outNDVI = outd+"NDVI.tif"
outEVI = outd+"EVI.tif"
outGCC = outd+"GCC.tif"

coutNDVI = ((mrz4-mrz1)/(mrz4+mrz1)) #calcualte NDVI

coutEVI = ((mrz4-mrz1)/(mrz4+6*mrz1-7.5*mrz3+1)) #calcualte EVI

coutGCC = (mrz2/(mrz1+mrz2+mrz3)) #calcualte GCC

#save NDVI, EVI, and GCC to file
coutNDVI.save(outNDVI)
coutEVI.save(outEVI)
coutGCC.save(outGCC)

#calcualte NDVI mean and standard deviation
RMeanNDVI = arcpy.GetRasterProperties_management(outNDVI, "MEAN")
RSTDNDVI = arcpy.GetRasterProperties_management(outNDVI, "STD")

MeanNDVI = RMeanNDVI.getOutput(0)
STDNDVI = RSTDNDVI.getOutput(0)

#calcualte EVI mean and standard deviation
RMeanEVI = arcpy.GetRasterProperties_management(outEVI, "MEAN")
RSTDEVI = arcpy.GetRasterProperties_management(outEVI, "STD")

MeanEVI = RMeanEVI.getOutput(0)
STDEVI = RSTDEVI.getOutput(0)

#calcualte GCC mean and standard deviation
RMeanGCC = arcpy.GetRasterProperties_management(outGCC, "MEAN")
RSTDGCC = arcpy.GetRasterProperties_management(outGCC, "STD")

MeanGCC = RMeanGCC.getOutput(0)
STDGCC = RSTDGCC.getOutput(0)

#save NDVI, EVI, and GCC to file
textfile = open(outd+"Vegetation Index.txt","w")
textfile.write("NDVI: "+"Mean: "+str(float(MeanNDVI))+" STD: "+str(float(STDNDVI))+"\nEVI: "+"Mean: "+str(float(MeanEVI))+" STD: "+str(float(STDEVI))+"\nGCC: "
               +"Mean: "+str(float(MeanGCC))+" STD: "+str(float(STDGCC)))
textfile.close()

#delete the 4 calibrated bands as a composite image as been made
arcpy.Delete_management(SaveBand1)
arcpy.Delete_management(SaveBand2)
arcpy.Delete_management(SaveBand3)
arcpy.Delete_management(SaveBand4)
