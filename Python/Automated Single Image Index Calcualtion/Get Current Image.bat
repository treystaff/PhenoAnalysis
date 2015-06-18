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

md "D:\Phenocam\EROS\EROS_%theFilename%"
md "D:\Phenocam\Oakville\Oakville_%theFilename%"

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Oakville\Oakville_%theFilename%\Oakville_%paddedX%_%digit%_%t%.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville_IR.jpg" --output-document D:\Phenocam\Oakville\Oakville_%theFilename%\Oakville_IR_%paddedX%_%digit%_%t%.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\EROS\EROS_%theFilename%\EROS_%paddedX%_%digit%_%t%.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros_IR.jpg" --output-document D:\Phenocam\EROS\EROS_%theFilename%\EROS_IR_%paddedX%_%digit%_%t%.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Calc4Band.py D:/Phenocam/Oakville/Oakville_%theFilename%/Oakville_%paddedX%_%digit%_%t%.jpg D:/Phenocam/Oakville/Oakville_%theFilename%/Oakville_IR_%paddedX%_%digit%_%t%.jpg D:/Phenocam/Oakville/Oakville_%theFilename%/Oakville_Comp_%paddedX%_%digit%_%t%.tif D:/Phenocam/Oakville/Oakville_%theFilename%/

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Calc4Band.py D:/Phenocam/EROS/EROS_%theFilename%/EROS_%paddedX%_%digit%_%t%.jpg D:/Phenocam/EROS/EROS_%theFilename%/EROS_IR_%paddedX%_%digit%_%t%.jpg D:/Phenocam/EROS/EROS_%theFilename%/EROS_Comp_%paddedX%_%digit%_%t%.tif D:/Phenocam/EROS/EROS_%theFilename%/
