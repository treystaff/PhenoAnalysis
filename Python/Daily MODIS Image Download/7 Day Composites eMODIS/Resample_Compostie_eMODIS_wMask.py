
print "Import needed elements"
import arcpy
import sys
import os
import glob
import shutil
arcpy.CheckOutExtension("Spatial") #requires ArcGIS spatial analyst extension
from arcpy.sa import *

print "Read sys args"
inputarg = (sys.argv[1])
mask = (sys.argv[2])
Julianday = (sys.argv[3])

eMODISdir = r""+inputarg
os.chdir(eMODISdir)

print "Find Bands"
SearchBand = glob.glob("*/*REFL*QKM*B1*REFL*.tif")
Band1 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band1 = Band1.replace('\\', '/')

SearchBand = glob.glob("*/*REFL*QKM*B2*REFL*.tif")
Band2 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band2 = Band2.replace('\\', '/')

SearchBand = glob.glob("*/*REFL*HKM*B3*REFL*.tif")
Band3 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band3 = Band3.replace('\\', '/')

SearchBand = glob.glob("*/*REFL*HKM*B4*REFL*.tif")
Band4 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band4 = Band4.replace('\\', '/')

SearchBand = glob.glob("*/*REFL*HKM*B5*REFL*.tif")
Band5 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band5 = Band5.replace('\\', '/')

SearchBand = glob.glob("*/*REFL*HKM*B6*REFL*.tif")
Band6 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band6 = Band6.replace('\\', '/')

SearchBand = glob.glob("*/*REFL*HKM*B7*REFL*.tif")
Band7 = str(eMODISdir)+"\\"+str(SearchBand[0])
Band7 = Band7.replace('\\', '/')

TempDir = r""+eMODISdir+"\\temp_Resample_eMODIS"
TempDir = TempDir.replace('\\', '/')

print "Make temp directory"
if not os.path.exists(TempDir):
    os.makedirs(TempDir)

print "resample Band 3"
arcpy.Resample_management(Band3,TempDir+"/B3.tif","250","NEAREST")
print "resample Band 4"
arcpy.Resample_management(Band4,TempDir+"/B4.tif","250","NEAREST")
print "resample Band 5"
arcpy.Resample_management(Band5,TempDir+"/B5.tif","250","NEAREST")
print "resample Band 6"
arcpy.Resample_management(Band6,TempDir+"/B6.tif","250","NEAREST")
print "resample Band 7"
arcpy.Resample_management(Band7,TempDir+"/B7.tif","250","NEAREST")

print "composite bands 1-7"
BandToComp = Band1+";"+Band2+";"+TempDir+"/B3.tif"+";"+TempDir+"/B4.tif"+";"+TempDir+"/B5.tif"+";"+TempDir+"/B6.tif"+";"+TempDir+"/B7.tif"
eMODISdir = eMODISdir.replace('\\', '/')
FinalImage = eMODISdir+"/eMODIS_Composite_"+str(Julianday)+".tif"
arcpy.CompositeBands_management(BandToComp,FinalImage)

print "remove zip files"
shutil.rmtree(TempDir)
SearchZip = glob.glob("*.zip")
SZip = eMODISdir+"/"+str(SearchZip[0])
os.remove(SZip)
SZip = eMODISdir+"/"+str(SearchZip[1])
os.remove(SZip)

print "remove uneeded directories"
SearchDir = glob.glob("*REFL*")
SDir = eMODISdir+"/"+str(SearchDir[0])
shutil.rmtree(SDir)
SDir = eMODISdir+"/"+str(SearchDir[1])
shutil.rmtree(SDir)

print "extract by mask"
mrz1 = ExtractByMask(FinalImage,mask) 
SaveImage = eMODISdir+"/eMODIS_Composite_"+str(Julianday)+"_Mask.tif"
mrz1.save(SaveImage)

print "remove uneeded files"
SearchDir = glob.glob("*info*")
SDir = eMODISdir+"/"+str(SearchDir[0])
shutil.rmtree(SDir)

#delete
arcpy.Delete_management(FinalImage)


