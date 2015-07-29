@echo off

for /F "tokens=2,3,4 delims=/ " %%i in ('date/t') do set y=%%k
for /F "tokens=2,3,4 delims=/ " %%i in ('date/t') do set d=%%k%%i%%j
for /F "tokens=5-8 delims=:. " %%i in ('echo.^| time ^| find "current" ') do set t=%%i%%j
set t=%t%_
if "%t:~3,1%"=="_" set t=0%t%
set t=%t:~0,4%
set "theFilename=%d%%t%"
echo %theFilename%

@echo off & setlocal
set dt=%date%
set /a m=1%dt:~4,2%-100
:: wanted to try this. it seemed to work.
set /a leap=(%dt:~10%"%%"4*1+2)/3,dd=(m-1)*31+1%dt:~7,2%-100,x=2+leap
for %%a in (2 4 6 9 11) do (
if %m% gtr %%a set /a dd-=x
set x=1
)
echo julian date: %dd%

set paddedX=0%dd%
if "%dd%" equ "%dd:~-3%" set "x=%paddedX:~-3%"

echo %paddedX%

set digit=%DATE:~12,2%
echo %digit%

md "D:\MODIS\MODIS_%theFilename%"

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://ge.ssec.wisc.edu/modis-today/index.php?gis=true&filename=t1_%digit%%dd%_USA2_721_250m&product=false_color&resolution=250m" --output-document D:\MODIS\MODIS_%theFilename%\MODIS_USA2_FalseColor_%paddedX%_%digit%.zip
cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://ge.ssec.wisc.edu/modis-today/index.php?gis=true&filename=t1_%digit%%dd%_USA2_143_250m&product=true_color&resolution=250m" --output-document D:\MODIS\MODIS_%theFilename%\MODIS_USA2_TrueColor_%paddedX%_%digit%.zip

cd "C:\Program Files (x86)\GnuWin32\bin"
7za e D:\MODIS\MODIS_%theFilename%\MODIS_USA2_FalseColor_%paddedX%_%digit%.zip -oD:\MODIS\MODIS_%theFilename%
cd "C:\Program Files (x86)\GnuWin32\bin"
7za e D:\MODIS\MODIS_%theFilename%\MODIS_USA2_TrueColor_%paddedX%_%digit%.zip -oD:\MODIS\MODIS_%theFilename%

DEL D:\MODIS\MODIS_%theFilename%\MODIS_USA2_FalseColor_%paddedX%_%digit%.zip
DEL D:\MODIS\MODIS_%theFilename%\MODIS_USA2_TrueColor_%paddedX%_%digit%.zip

cd "C:\Python27\ArcGIS10.3"
Python.exe r"C:\Program Files (x86)\GnuWin32\bin\MODISCalc4Band.py" r"D:\MODIS\MODIS_%theFilename%\t1.%digit%%dd%.USA2.143.250m.jpg" r"D:\MODIS\MODIS_%theFilename%\t1.%digit%%dd%.USA2.721.250m.jpg" r"D:\MODIS\MODIS_%theFilename%\Composite.%digit%%dd%.USA2.250m.tif"