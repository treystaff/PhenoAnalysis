@echo off

set a=001
echo %a%
set year=2015
echo %year%

cd "C:\Program Files (x86)\GnuWin32\bin"

wget --no-check-certificate --no-host-directories --no-directories --user=USERNAME --password=YOURPASSWORD -r -l1 --no-parent -A "*REFL*HKM*.zip" "https://dds.cr.usgs.gov/emodis/CONUS/expedited/TERRA/%year%/comp_%a%/" --directory-prefix "D:\MODIS\eMODIS\%year%\%a%"
wget --no-check-certificate --no-host-directories --no-directories --user=USERNAME --password=YOURPASSWORD -r -l1 --no-parent -A "*REFL*QKM*.zip" "https://dds.cr.usgs.gov/emodis/CONUS/expedited/TERRA/%year%/comp_%a%/" --directory-prefix "D:\MODIS\eMODIS\%year%\%a%"

cd "C:\Program Files (x86)\GnuWin32\bin"
"C:\Program Files (x86)\GnuWin32\bin\7za.exe" e "D:\MODIS\eMODIS\%year%\%a%\*.zip" -o"D:\MODIS\eMODIS\%year%\%a%\*"

cd "C:\Python27\ArcGIS10.3"
Python.exe D:\MODIS\eMODIS\bin\Resample_Compostie_eMODIS_wMask.py D:\MODIS\eMODIS\%year%\%a% D:/MODIS/eMODIS/bin/Mask/Mask.shp %a%
















