import cv2
import imutils
from sklearn import preprocessing

class huDescriptor:

	def huMoments(self, img):
		huMoments = []
		image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		threshold = cv2.threshold(image,180,255, cv2.THRESH_BINARY)[1]
		contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)
		contour = max(contours, key=cv2.contourArea)

		x, y, width, height = cv2.boundingRect(contour)
		roi = cv2.resize(threshold[y:y +height, x:x + width],(50,50))

		moments = cv2.moments(roi)
		huMoments = preprocessing.normalize(cv2.HuMoments(moments))
			
		return huMoments

		