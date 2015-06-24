
"""============  FOR AMERICA-VIEW/PHENOCAM INTERNAL USE ONLY!  =============="""
#===============================================================================

    # Name:          PhenoCamStats-OCR ver.Beta

    # Purpose:       Produce *.csv containing datetime, temperature,
    #                and exporsure values per PhenoCam image in time-series

    # Orginization:  USGS / NAGT Office
    #                North Central Climate Science Center
    #                Colorado State University

    # Copyright:     (c) June-23-2015
    #                Joseph M. Krienert
    #                jkrienert@siu.edu

    # Credits:       PyTesser v0.0.1 - Michael J.T. O'Kelly
    #                Tesseract v3.0.1 - Ray Smith,Phil Cheatle,Simon Crouch,
    #                Dan Johnson,Mark Seaman,Sheelagh Huddleston,Chris Newton
    #                ... and several others

#===============================================================================

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    For a copy of the GNU General Public License, please refer to:
#                                    <http://www.gnu.org/licenses/>

#===============================================================================

import os
import csv
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps as pilOps
from pytesser import image_to_string as img2Str


""" ============================ Primary inputs below! ===================================== """
directory = r'C:\**-- main PhenoCam image dir housing all year&month sub-dirs --**\someCamera'
outputStatsFile = r'C:\**-- intended output stats file dir --**\someCSV.csv'
timeZone = ' CST'#<= respective of cameras time-zone (text on image), PREFIX SPACE REQUIRED!
""" ============================ Primary inputs above! ===================================== """


# central control function for iterating through all *.jpg images
# within user distinguished directory (above ^)
def compilePhenoCamStats(directory):
    statsThruTime = []
    for dirIdx,(dirpath, dirnames, filenames) in enumerate(os.walk(directory)):
##        if dirIdx>3: break  #<== Dir test-break to confirm accurate outputs
        for fileIdx, filename in enumerate(filenames):
##            if fileIdx>15: break   #<== File-test break to confirm accurate outputs
            if filename.endswith('.jpg'):
                imgFile = os.sep.join([dirpath, filename])
                currentResult = readStats(imgFile)
                statsThruTime.append(currentResult)
##        if idx>1:
##            print "Image directory --"+dirpath+"-- parameters recorded!"
    saveTemps(statsThruTime,outputStatsFile)

# Image header text croping, processing, and conversion to string form
def readStats(imgFile):
    """ inital crop of entire stats-header inset """
    # the crop bounds must be based on consistant camera resolution (thru series)
    # all crops below are for 1296pix x 960pix resolution
    image = Image.open(imgFile)
    rawCrop = image.crop((0,0,800,83))
    statsImg = rawCrop

    """ pre-processing (improves OCR font character edge recognition) """
    # desaturate to black and white
    blkNwhtEnhance = ImageEnhance.Color(rawCrop)
    bwImg = blkNwhtEnhance.enhance(0)
    # invert image
    invtImg = pilOps.invert(bwImg)
    # raise Contrast
    conEnhance = ImageEnhance.Contrast(invtImg)
    conImg = conEnhance.enhance(1.1)
    # raise brightness
    brghtEnhance = ImageEnhance.Brightness(conImg)
    statsImg = brghtEnhance.enhance(1.2)
    # highlight font character edging
    statsImg = statsImg.filter(ImageFilter.DETAIL)

    """ sub-cropping of pre-processed stats-header inset """
    clnTime = statsImg.crop((0,0,780,28))
    clnTemp = statsImg.crop((0,28,306,55))
    clnExpo = statsImg.crop((0,55,148,82))

    """ final text-2-string analysis with anomolous syntax cleanup """
    # establish date-time values and compensate for misread characters
    try:
        timeStr = img2Str(clnTime).split(' IR ')[1].split(timeZone)[0]
        # adjust format from nontext pixels @crop edges (occasionally binary?)
        if '\xe2\x80\x94 ' in timeStr: timeStr = timeStr.split('\xe2\x80\x94 ')[1]
        if '-' in timeStr: timeStr = timeStr.split('- ')[1]
        if '\xe2\x80\x99' in timeStr: timeStr = timeStr.split('\xe2\x80\x99')[0]
        timeStr = timeStr[4:] #<= remove leading day label
        timeStr = timeStr[:-3] #<= remove trailing second values
        timeStr = charCorrect(timeStr)
        try:
            timeStr = datetime.strptime(timeStr, "%b %d %Y %H:%M")
        except ValueError:
            timeStr = timeStr
    except IndexError:
        timeStr = "Read Error"

    # establish temperature values and compensate for misread characters
    try:
        tempStr = img2Str(clnTemp).split('\n\n')[0].split(': ')[1]
        tempStr = tempStr[-5:] #<== retains only temp. value
        tempStr = charCorrect(tempStr)
    except IndexError:
        tempStr = "Read Error"

    # establish exposure values and compensate for misread characters
    try:
        expoStr = img2Str(clnExpo).split(': ')[1] #<= remove leading expo. label
        expoStr = charCorrect(expoStr)
        expoStr = expoStr.split('\n\n')[0]
    except IndexError:
        expoStr = "Read Error"

    return [timeStr,tempStr,expoStr]

""" In reality, the font styles of the PhenoCam Stat overlay
should be post-trained into the tesseract directory.  In the mean
time, post-corrections below are mildly sufficent. """
# replaces consistantly anomolous OCR results with best appropraited values
def charCorrect(inStr):
    if '?' in inStr: inStr = inStr.replace('?','7')
    if 'D' in inStr: inStr = inStr.replace('D','0')
    if 'E!' in inStr: inStr = inStr.replace('E!','8')
    if 'EI' in inStr: inStr = inStr.replace('EI','8')
    if 'El' in inStr: inStr = inStr.replace('El','8')
    if 'EH' in inStr: inStr = inStr.replace('EH','8')
    if ' I' in inStr: inStr = inStr.replace(' I','1')
    if '0ec' in inStr: inStr = inStr.replace('0ec','Dec')
    if 'S' in inStr:
        if not 'un' in inStr and not 'at' in inStr and not 'ep' in inStr:
            inStr = inStr.replace('S','5')
    return inStr

# Save resultant PhenoCamStats dataset to *.csv table
def saveTemps(statsThruTime,outputStatsFile):
    with open(outputStatsFile, 'w') as fileOut:
        writer = csv.writer(fileOut)
        header = ['Time','Temp','Expo']
        writer.writerow(header)
        for data in statsThruTime:
            writer.writerow(data)
##    print 'Success!'

if __name__ == '__main__':
    compilePhenoCamStats(directory)