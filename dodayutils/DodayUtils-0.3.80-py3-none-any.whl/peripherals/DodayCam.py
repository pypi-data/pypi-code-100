import cv2
import time
import pyzbar.pyzbar as pyzbar

from DodayUtils._exceptions import *
from DodayUtils._dwrappers import *

# Dependency cv2, pyzbar
# Be reponsible for the dependencies
# if you want to use this peripheral. 

class DodayCam:
	"""
	This is the object for doday camera. 
	Currently, it is for doday DDA01 
	qr code scanner. 
	"""
	@dutils
	def __init__(self, video_source=0, **kwargs):
		"""
		Input: 
			- video source from the 
			device. video0, video1 etc. 
		"""
		self.video_source = video_source
		self.terminate_qr_process = False

	@dutils
	def decodeDisplay(self, imagex1, **kwargs):
		# Convert to grayscale image
		gray = cv2.cvtColor(imagex1, cv2.COLOR_BGR2GRAY)
		barcodes = pyzbar.decode(gray)

		try:
			barcode = barcodes[0]
		except:
			return ""

		barcodeData = barcode.data.decode("utf-8")
		
		return barcodeData

	@dutils
	def get_qr_scan_data(self, tout, **kwargs):
		"""
		This is the main function that the checkin front end should
		call. It turns on the camera and scan the qr code and extract
		the data for checkin functionality. 
		- Output:
			data = string: "", "{LegitData}", "Terminated"
		"""
		self.terminate_qr_process = False

		# Capture frame
		cap = cv2.VideoCapture(0, cv2.CAP_V4L)
		cv2.waitKey(10)
		data = None

		tout_start_time = time.time()
		while True:
			_, inputImage = cap.read()
			cv2.waitKey(50)

			data = self.decodeDisplay(inputImage)

			if self.terminate_qr_process:
				logging.warn("[Inside Qr Code Scan] Manual Terminate Process")
				cv2.waitKey(1)
				cap.release()
				data = "Terminated"

			# payment timeout -> set to timeout
			if time.time() - tout_start_time >= tout:
				break

			if len(data)>0:
				break

			cv2.waitKey(1)

		cap.release()
		return data

	@dutils
	def terminate_qr_scan(self, **kwargs):
		"""
		This is the helper function that terminates
		qr scan. 
		"""
		self.terminate_qr_process = True