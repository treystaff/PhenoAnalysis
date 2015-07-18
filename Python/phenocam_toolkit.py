"""
phenocam_toolkit.py

A collection of routines for processing images from the PhenoCam
Network (http://phenocam.sr.unh.edu/).  For the latest version and
documentation on this library see: http://phenocam.sr.unh.edu/webcam/tools.

Depends: numpy, PIL

"""

import numpy as np
import os, sys, re, glob
import datetime

###############################################################################

def get_dn_means(im, roimask):
    
    """
    function to return mean DN values for an image / mask pair.
    """
 
    # split into bands
    (im_r, im_g, im_b) = im.split()

    # create numpy arrays with bands
    r_array = np.asarray(im_r, dtype=np.float)
    g_array = np.asarray(im_g, dtype=np.float)
    b_array = np.asarray(im_b, dtype=np.float)
    brt_array = r_array + g_array + b_array

    # try applying mask to brightness image ... if mask and image don't
    # have same size this will raise an exception.
    try:
        brt_ma = np.ma.array(brt_array,mask=roimask)
    except:
        errstr = "Error applying mask to: %s\n" % (imgfile,)
        sys.stderr.write(errstr)
        sys.exit

    # make masked arrays for R,G,B
    g_ma = np.ma.array(g_array,mask=roimask)
    r_ma = np.ma.array(r_array,mask=roimask)
    b_ma = np.ma.array(b_array,mask=roimask)

    # find mean values to store
    g_mean_roi = np.mean(g_ma)
    r_mean_roi = np.mean(r_ma)
    b_mean_roi = np.mean(b_ma)

    return [r_mean_roi, g_mean_roi,  b_mean_roi]

###############################################################################

def fn2datetime(sitename, filename, irFlag=False):
    """
    Function to extract the datetime from a "standard" filename based on a
    sitename.  Here we assume the filename format is the standard:

          sitename_YYYY_MM_DD_HHNNSS.jpg

    So we just grab components from fixed positions.  If irFlag is 
    True then the "standard" format is:

          sitename_IR_YYYY_MM_DD_HHNNSS.jpg

    """    
    
    if irFlag:
        prefix=sitename+"_IR"
    else:
        prefix=sitename

    # set start of datetime part of name
    nstart=len(prefix)+1
    
    # assume 3-letter extension e.g. ".jpg"
    dtstring=filename[nstart:-4]
    
    # extract date-time pieces
    year=int(dtstring[0:4])
    mon=int(dtstring[5:7])
    day=int(dtstring[8:10])
    hours=int(dtstring[11:13])
    mins=int(dtstring[13:15])
    secs=int(dtstring[15:17])
    
    # return list
    return datetime.datetime(year, mon, day, hours, mins, secs)

###############################################################################

def doy2date(year, doy, out='tuple'):
    '''
    Convert year and yearday into calendar date. Output is a tuple
    (out='tuple': default) ISO string (out='iso'), julian date
    (out='julian'), or python date object (out='date')
    '''
    year=int(year)
    doy=int(doy)
    thedate = datetime.date(year, 1, 1) + datetime.timedelta(doy-1)

    if out=='tuple':
        return thedate.timetuple()[:3]
    elif out=='iso':
        return thedate.isoformat()
    elif out=='julian':
        return thedate.toordinal()
    elif out=='date':
        return thedate
    else:
        return None

###############################################################################

def date2doy(year, month, day):
    """
    Convert calendar date into year and yearday.
    """
    year=int(year)
    month=int(month)
    day=int(day)
    thedate = datetime.date(year, month, day)
    return (year, thedate.timetuple()[7])

##############################################################################

def datetime2fdoy(myDateTime):
    """
    Given a datetime object return the fractional day-of-year.
    """
    
    myDate=myDateTime.date()
    myYear=myDate.year
    jan1=datetime.datetime(myYear,1,1,0,0,0)
    tdel=myDateTime-jan1

    # ignore microseconds
    doy=tdel.days+tdel.seconds/86400.

    # add a day so that doy 1.5 is Jan 1 at noon.  This matches
    # sample output of Steve K. and Michael T. ???? Probably
    # needs some attention! DOY is really integer in range 1-366.
    # Here we get decimal between 1 and 367.
    doy = doy + 1

    return doy

###############################################################################

def getsiteimglist(archive_dir,sitename,
                   startDT=datetime.datetime(1990,1,1,0,0,0),
                   endDT=datetime.datetime.now(),
                   getIR=False):
    """
    Returns a list of imagepath names for ALL images in 
    archive for specified site.  Optional arguments:
      getIR   : If set to true only return IR images.
      startDT : Start datetime for image list
      endDT   : End datetime for image list

    NOTE: This might be lots faster if we just do a glob.glob()
    on a pattern.  Might not be quite as robust since we're skipping
    the check the .jpg file being a regular file.  See, getImageCount()
    below for how this would work!
    """

    STARTDIR = archive_dir
    
    # get startyear and endyear
    startYear = startDT.year
    endYear = endDT.year

    # get startmonth and endmonth
    startMonth = startDT.month
    endMonth = endDT.month

    imglist = []
    sitepath = os.path.join(STARTDIR, sitename)
    if not os.path.exists(sitepath):
        return imglist

    # get a list of files in the directory
    yeardirs = os.listdir(sitepath)
        
    # loop over all files
    for yeardir in yeardirs:

            # check that its a directory
            yearpath = os.path.join(sitepath,yeardir)
            if not os.path.isdir(yearpath): 
                continue

            # check if this yeardir could be a 4-digit year.  if not skip
            if not re.match('^\d\d\d\d$',yeardir):
                continue

            # check if we're before startYear
            if (int(yeardir) < startYear) | (int(yeardir) > endYear) :
                continue

            # get a list of all files in year directory
            mondirs = os.listdir(yearpath)

            # loop over all files
            for mondir in mondirs:

                # check that its a directory
                monpath = os.path.join(yearpath,mondir)
                if not os.path.isdir(monpath): 
                    continue

                # check if this mondir could be a 2-digit month.  if not skip
                if not re.match('^\d\d$',mondir):
                    continue

                # check month range
                if (int(mondir) < 1) | (int(mondir) > 12):
                    continue

                # check start year/month
                if (int(yeardir) == startYear) & (int(mondir) < startMonth):
                    continue

                # check end year/month
                if (int(yeardir) == endYear) & (int(mondir) > endMonth):
                    continue

                try:
                    imgfiles = os.listdir(monpath)
                    if getIR:
                        image_re="^%s_IR_%s_%s_.*\.jpg$" % (sitename, yeardir, mondir)
                    else:
                        image_re="^%s_%s_%s_.*\.jpg$" % (sitename, yeardir, mondir)

                    for imgfile in imgfiles:
                        # check for pattern match
                        if not re.match(image_re,imgfile):
                            continue

                        # get image time
                        img_dt = fn2datetime(sitename, imgfile, irFlag=getIR)

                        if img_dt < startDT:
                            continue

                        if img_dt > endDT:
                            continue
                        
                        # only add regular files
                        imgpath=os.path.join(monpath,imgfile)
                        if not os.path.isdir(imgpath):
                            imglist.append(imgpath)

                except OSError, e:
                    if e.errno==20:
                        continue                        
                    else:
                        errstring = "Python OSError: %s" % (e,)
                        print errstring

    imglist.sort()
    return imglist

##########################################################################################
