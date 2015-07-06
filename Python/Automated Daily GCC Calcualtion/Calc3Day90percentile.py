"""

This script is to be used for the phenocam project.
Created by Morgen Burke

This script is to be used to calcualte 3 day 90th percentile GCC values,
it uses datetime to calcualte today, yesterday, and twodays ago and using correct
folder names with folder_yearmonthday\pervious_day_GCC_Array.npy it can be used
to automaticaly calcualte yesterdays GCC 3 day 90th percentile.
"""
import numpy # used to compute arrays
from arcpy.sa import * # sys arguments
import datetime # calcualte the current date to be used in folder naming structure

today = datetime.date.today() # calcualte todays date
print 'Today    :', today

one_day = datetime.timedelta(days=1) # used to calculate yesterday and two days ago date
print 'One day  :', one_day

yesterday = today - one_day # yesterdays date
print 'Yesterday:', yesterday

twodays = yesterday - one_day # two days ago date
print 'Two days ago :', twodays

# list of inputs, using date naming structure for folder to automate file locations each day
Input = (sys.argv[1]) # the file path and folder with the saved arrays excluding the ending yearmonthday of the folder name (this is an input argument)
PArray = Input+str(today.year)+str('%02d' % (today.month))+str('%02d' % (today.day))+"/Daily_GCC_90Perc_Array.npy"
CArray = Input+str(yesterday.year)+str('%02d' % (yesterday.month))+str('%02d' % (yesterday.day))+"/Daily_GCC_90Perc_Array.npy"
NArray = Input+str(twodays.year)+str('%02d' % (twodays.month))+str('%02d' % (twodays.day))+"/Daily_GCC_90Perc_Array.npy"
output = Input+str(yesterday.year)+str('%02d' % (yesterday.month))+str('%02d' % (yesterday.day))+"/"

# load in the arrays for the last three days
PArray = numpy.load(PArray, mmap_mode='r')
CArray = numpy.load(CArray, mmap_mode='r')
NArray = numpy.load(NArray, mmap_mode='r')

# append the arrays from the last three days together into a single array
threedayperc = numpy.array(PArray)
threedayperc = numpy.float32(numpy.append(CArray,threedayperc))
threedayperc = numpy.float32(numpy.append(NArray,threedayperc))

#calcualte the 90th percentile
threedayperc = float(numpy.percentile(threedayperc, 90))

#print the 90th percentile to the user
print ("90th percentile: " + str(threedayperc)+ "\n") #print daily GCC 90th percentile to user

# output daily 90th percentile GCC calcualtion
textfile = open(output+"/Three Day GCC Calcualtion.txt","w")
textfile.write("GCC: " + str(threedayperc))
textfile.close()
