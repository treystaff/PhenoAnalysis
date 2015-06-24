CAUTION!
 >>This groupo release is windows 32b specific<<

Installation:
[Function requires python module PIL (Pillow Fork)]

-Copy/Move included pytesser folder into the current working python directory '...\Lib\site-packages\**here**'

-Open file titled '__init__.py' within new pytesser folder and edit values within the header bounds 'Primary inputs below/above' to fit your needs

-Open 'PhenoCamStats-OCR.py' and edit values within the header bounds 'Primary inputs below/above' to fit your needs

-Run 'PhenoCamStats-OCR.py' and have some experimental/analytical fun!

Please note:
Large image directories can take significant time to process.  Please be paitent.

Errors are almost garunteed to arise - this was written overnight, thus has minimal checksums incorperated at current.  The Tesseract-OCR backbone has capabilities to be 'trained' specific to the type of font used in the phenocam images.  This might be the best option to improve results (rather then the current method of post-process character error corrections).

Feel free to contact (see script headers) with concerns, and the best possible effort to resolve will be made.