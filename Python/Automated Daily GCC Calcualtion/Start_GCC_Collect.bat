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

md "D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%"
md "D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp"
md "D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%"
md "D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp"

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_0700.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_0700.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_0700.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_0700.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_0700.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_0700.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_0730.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_0730.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_0730.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_0730.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_0730.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_0730.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_0800.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_0800.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_0800.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_0800.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_0800.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_0800.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_0830.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_0830.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_0830.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_0830.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_0830.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_0830.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_0900.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_0900.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_0900.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_0900.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_0900.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_0900.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_0930.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_0930.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_0930.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_0930.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_0930.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_0930.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1000.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1000.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1000.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1000.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1000.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1000.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1030.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1030.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1030.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1030.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1030.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1030.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1100.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1100.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1100.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1100.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1100.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1100.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1130.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1130.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1130.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1130.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1130.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1130.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1200.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1200.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1200.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1200.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1200.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1200.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1230.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1230.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1230.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1230.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1230.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1230.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1300.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1300.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1300.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1300.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1300.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1300.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1330.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1330.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1330.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1330.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1330.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1330.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1400.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1400.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1400.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1400.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1400.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1400.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1430.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1430.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1430.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1430.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1430.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1430.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1500.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1500.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1500.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1500.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1500.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1500.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1530.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1530.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1530.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1530.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1530.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1530.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1600.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1600.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1600.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1600.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1600.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1600.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1630.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1630.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1630.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1630.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1630.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1630.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1700.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1700.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1700.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1700.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1700.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1700.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1730.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1730.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1730.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1730.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1730.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1730.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1800.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1800.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1800.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1800.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1800.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1800.tif

timeout 1605 /nobreak >nul

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/oakville.jpg" --output-document D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp\Oakville_%paddedX%_%digit%_1830.jpg

cd "C:\Program Files (x86)\GnuWin32\bin"
wget "http://phenocam.sr.unh.edu/data/latest/usgseros.jpg" --output-document D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp\EROS_%paddedX%_%digit%_1830.jpg

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_%paddedX%_%digit%_1830.jpg D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_1830.tif

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_GCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_%paddedX%_%digit%_1830.jpg D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_1830.tif

timeout 10 /nobreak >nul

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_DailyGCC.py D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/temp/Oakville_GCC_%paddedX%_%digit%_ D:/Phenocam/Daily_GCC_Average/Oakville/Oakville_%theFilename%/Oakville_GCC_%paddedX%_%digit%_

cd "C:\Python27\ArcGIS10.3"
Python.exe D:/Phenocam/Daily_GCC_Average/bin/Calc_DailyGCC.py D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/temp/EROS_GCC_%paddedX%_%digit%_ D:/Phenocam/Daily_GCC_Average/EROS/EROS_%theFilename%/EROS_GCC_%paddedX%_%digit%_

timeout 10 /nobreak >nul

rmdir /s /q "D:\Phenocam\Daily_GCC_Average\Oakville\Oakville_%theFilename%\temp"

rmdir /s /q "D:\Phenocam\Daily_GCC_Average\EROS\EROS_%theFilename%\temp"



































