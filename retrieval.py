import numpy as np
import cv2
import imutils
import glob
import math
import csv
from hudescriptor import huDescriptor
from colordescriptor import ColorDescriptor

class retrieval:

	def compare(self, image, limit):

		huResults = {}
		cdResults = {}
		hu = huDescriptor()
		cd = ColorDescriptor((8, 12, 3))

		huMoments = abs(hu.huMoments(image))
		colorDesc = cd.describe(image)

		cdResults = self.distance('conf/colorFeatures.csv', colorDesc)
		huResults = self.distance('conf/huFeatures.csv', huMoments)
		
		#auxResults = [(key, value ) for (key, value) in huResults.items()]
		auxResults = [(key, ((value*0.85)+(cdResults[key]*0.15)) ) for (key, value) in huResults.items()]
		
		results = sorted([(v, k) for (k, v) in auxResults])
		return results[:limit]

	def distance(self, path, inputFeatures):
		results = {}
		with open(path) as f:
			reader = csv.reader(f)

			for row in reader:
				features = [float(x) for x in row[1:]]
				d = math.dist(features, inputFeatures)

				results[row[0]] = d

			f.close()
		return results