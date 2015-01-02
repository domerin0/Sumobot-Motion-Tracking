import io
import time, datetime
import picamera
from SerialThread import *
import cv2
import numpy as np

class MotionDetection:
	def __init__(self):
		self.__image0 = None
		self.__image1 = None
		self.__image2 = None
		self._MOTION_LEVEL = 500000
		self._THRESHOLD = 35
		self.HEIGHT = 20
		self.WIDTH = 600

	def _updateImage(self, image):
		self.__image2 = self.__image1
		self.__image1 = self.__image0
		self.__image0 = image

	def _ready(self):
		return self.__image0 != None and self.__image1 != None and self.__image2 != None

	def _getMotion(self, image):
		self._updateImage(image)
		if not self._ready():
			return "something wrong here"
		d1 = cv2.absdiff(self.__image1, self.__image0)
		d2 = cv2.absdiff(self.__image2, self.__image0)
		result = cv2.bitwise_and(d1, d2)
		(value, result) = cv2.threshold(result, self._THRESHOLD, 255, cv2.THRESH_BINARY)
		minx, maxx= self.getRectangle(result)
		return (maxx - minx)

	def getRectangle(self, result):
		minx, maxx, numChanges = self.WIDTH, 0, 0
		changedCols = []
		for num in range(self.WIDTH):
			test = sum(result[:,num])
			if(test >= 4 * 255):
				numChanges +=1
				changedCols.append(num)
		if(numChanges >= 1):
			minx = min(changedCols)
			maxx = max(changedCols)
			print str(minx) + "min x"
			print str(maxx) + "max x"
			return (minx, maxx)
		else:
			return (0, 0)

def process():
	with picamera.PiCamera() as camera:
		#camera.start_preview()
		camera.resolution = (600,20)
		time.sleep(2)
		detection = MotionDetection()
		count = 0
		serThread = SerialThread()
		while True:
		# Create the in-memory stream
			stream = io.BytesIO()
			camera.capture(stream, format='jpeg')
		# Construct a numpy array from the stream
			data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		# "Decode" the image from the array, preserving colour
			image = cv2.imdecode(data, 0)
			print "reached this point"
			center = detection._getMotion(image)
			serThread = SerialThread()
			serThread.addValue(str(center))
			print repr(center)


if __name__ == "__main__":
	process()
