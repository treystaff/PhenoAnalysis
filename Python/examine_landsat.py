"""
This is just a test script for comparing phenocam derived GCC with landsat derived GCC.

This should not really be used. It is for testing only.  
"""
# USER INPUT
phenoDir = '/media/Storage/CODE/phenocam/' #Path to phenocam archives. 
sitename = 'ninemileprairie' #The sitename for comparison. 
landsatDir = '/media/Storage/CODE/phenocam/clipped/' #Should already be clipped. Assumes dir to imgs that have RGB(N) bands


#AUTOMATED PORTION BELOW
from scipy import misc
#Just do an ugly import of other functions for now....
execfile('/media/Storage/CODE/phenocam/greenness.py')
execfile('/media/Storage/CODE/phenocam/unpack_landsat.py')
execfile('/media/Storage/CODE/phenocam/python/phenocam_toolkit.py')


#Deal w/ phenocam images first 
phenoGcc= []
phenoDoys = []
fns = getsiteimglist(phenoDir,sitename)

for f in fns:
	img = misc.imread(f)
	fn = os.path.split(os.path.splitext(f)[0])[1]  + '.jpg'
	date = fn2datetime(sitename,fn)
	_,doy = date2doy(date.year,date.month,date.day)
	phenoDoys.append(doy)
	phenoGcc.append(mean_gcc(img))


#Now lets get the landsat data.
lsatGcc = []
lsatDoys = []
 
fns = glob.glob(landsatDir + '*_CLIP.TIF')
for f in fns:
	ras = gdal.Open(f)
	#md = ras.GetMetadata()
	mdPath = landsatDir + os.path.split(os.path.splitext(f)[0])[1].split("_")[0] + '_MTL.txt'
	md = read_metadata(mdPath)
	date = datetime.datetime.strptime(md['DATE_ACQUIRED'],'%Y-%m-%d')
	_, doy = date2doy(date.year,date.month,date.day)
	lsatDoys.append(doy)
	
	#Read the raster and calc gcc
	arr = ras.ReadAsArray()
	arr = np.swapaxes(np.swapaxes(arr,0,2),0,1) #swap the axes so that array is [rows,cols,bands]
	lsatGcc.append(mean_gcc(arr))
