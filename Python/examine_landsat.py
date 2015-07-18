"""
This is just a test script for comparing phenocam derived GCC with landsat derived GCC.

This should not really be used. It is for testing only.  
"""
# USER INPUT
phenoDir = '/media/sf_O/PhenoCam/images/rgb/'  # Path to phenocam archives.
sitename = 'ninemileprairie'  # The sitename for comparison.
landsatDir = '/storage/clipped/'  # Should already be clipped. Assumes dir to imgs that have RGB(N) bands


# AUTOMATED PORTION BELOW
from scipy import misc
# Just do an ugly import of other functions for now....
execfile('/home/trey/CODE/PhenoAnalysis/Python/greenness.py')
execfile('/home/trey/CODE/PhenoAnalysis/Python/unpack_landsat.py')
execfile('/home/trey/CODE/PhenoAnalysis/Python/phenocam_toolkit.py')


# Deal w/ phenocam images first
phenoGcc = []
phenodates = []
fns = getsiteimglist(phenoDir, sitename)

for f in fns:
    img = misc.imread(f)
    fn = os.path.split(os.path.splitext(f)[0])[1] + '.jpg'
    date = fn2datetime(sitename, fn)
    phenodates.append(date)
    #_, doy = date2doy(date.year, date.month, date.day)
    #phenoDoys.append(doy)
    phenoGcc.append(mean_gcc(img))


# Now lets get the landsat data.
lsatGcc = []
lsatdates= []

fns = glob.glob(landsatDir + 'LC*_CLIP.TIF')
for f in fns:
    ras = gdal.Open(f)
    '''
    mdPath = landsatDir + os.path.split(os.path.splitext(f)[0])[1].split("_")[0] + '_MTL.txt'
    md = read_metadata(mdPath)
    date = datetime.datetime.strptime(md['DATE_ACQUIRED'], '%Y-%m-%d')
    _, doy = date2doy(date.year, date.month, date.day)
    lsatDoys.append(doy)
    '''
    date = datetime.datetime.strptime(f[-33:-26],'%Y%j')
    lsatdates.append(date)
    # Read the raster and calc gcc
    arr = ras.ReadAsArray()
    arr = np.swapaxes(np.swapaxes(arr, 0, 2), 0, 1)  # swap the axes so that array is [rows,cols,bands]
    lsatGcc.append(mean_gcc(arr))


plt.plot(lsatdates,lsatGcc,'go',ms=10, label='Landsat 8')
plt.plot(phenodates,phenoGcc,'b+',label='PhenoCam')
plt.xlabel('Date')
plt.ylabel('Mean GCC')
plt.title('Nine Mile Prairie PhenoCam VS Landsat 8 GCC')
plt.legend(loc='upper left',numpoints=1)
plt.show()