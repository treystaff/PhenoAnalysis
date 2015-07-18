'''
Script for testing per90 calculation.

This should not be used and will eventually be removed.
'''

from scipy import misc
import matplotlib
from matplotlib import pyplot as plt

execfile('/home/trey/CODE/PhenoAnalysis/Python/greenness.py')
execfile('/home/trey/CODE/PhenoAnalysis/Python/unpack_landsat.py')
execfile('/home/trey/CODE/PhenoAnalysis/Python/phenocam_toolkit.py')
phenoDir = '/media/sf_O/PhenoCam/images/rgb/'
sitename = 'ninemileprairie'

gcc = []
dates = []
fns = getsiteimglist(phenoDir,sitename) # Get all of the images associated with the site.

# Loop through each image, calculating mean GCC for each.
for f in fns:
  #Read the current image into memory. 
  img = misc.imread(f)

  #Determine the date from the filename.
  fn = os.path.split(os.path.splitext(f)[0])[1]  + '.jpg'
  date = fn2datetime(sitename,fn)
  dates.append(date)

  #Calculate mean GCC
  gcc.append(mean_gcc(img))

#Calc per90 and get a pandas dataframe in response.
df = per90(dates,gcc)

# Plot the results (compare per90 w/ raw gcc calc)
ax = df.plot(style='go',ms=10, label='Per90 GCC')
ax.plot(dates,gcc,'r*',label='Raw GCC')
ax.title('Raw vs Per90 GCC')
ax.legend(loc='best',numpoints=1)
plt.show()


ax = df.plot(style='go',ms=10, label='Per90 GCC')
ax.plot(phenodates,phenoGcc,'r*',label='Raw GCC')
ax.title('Raw vs Per90 GCC')
ax.legend(loc='best',numpoints=1)
ax.xlabel('Date')
ax.ylabel('Mean GCC')
plt.show()