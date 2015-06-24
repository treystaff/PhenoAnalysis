"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

import Image
import subprocess
import util


""" ============================ Primary inputs below! ===================================== """
tesseract_exe_name = r'C:\**-- The duplicated pytesser folder dir --**\tesseract.exe' 
scratch_image_name = r'C:\**-- The duplicated pytesser folder dir --**\Tesseract-OCR\temp.bmp' 
scratch_text_name_root = r'C:\**-- The duplicated pytesser folder dir --**\Tesseract-OCR\temp' 
cleanup_scratch_flag = True  
""" ============================ Primary inputs above! ===================================== """


def call_tesseract(input_filename, output_filename):
	args = [tesseract_exe_name, input_filename, output_filename]
	proc = subprocess.Popen(args)
	retcode = proc.wait()

def image_to_string(im, cleanup = cleanup_scratch_flag):
	try:
		util.image_to_scratch(im, scratch_image_name)
		call_tesseract(scratch_image_name, scratch_text_name_root)
		text = util.retrieve_text(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text
