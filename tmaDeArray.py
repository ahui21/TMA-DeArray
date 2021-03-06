import math
import cv2
import cv2.cv as cv
import numpy as np

class TMADeArray:

	imgLoc = raw_input("Enter the location of the picture file to be analyzed: ")
	estimate = int(input("Enter a rough estimate for the number of cores in this TMA: "))
	
	preProcessedImg = cv2.imread(imgLoc)
	cv2.imshow('pre-processing', preProcessedImg)
	
	img = cv2.imread(imgLoc, 0)
	img = cv2.medianBlur(img, 5)
	cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	height, width = img.shape[:2]

	meanRadiusEstimate = int(math.sqrt((height * width) / (4 * estimate)))

	print 'meanRadius: ', meanRadiusEstimate

	circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, int(meanRadiusEstimate * 0.5), param1 = 50, param2 = 50, minRadius = 0, maxRadius = int(1.5 * meanRadiusEstimate))

	circles = np.uint16(np.around(circles))

	tempRadii = list();

	for i in circles[0,:]:
		tempRadii.append(i[2])

	print tempRadii

	tempRadiiCount = list();

	for i in range(0, int(1.5*meanRadiusEstimate)):
		tempRadiiCount.append(tempRadii.count(i))

	print tempRadiiCount, 'lies', max(tempRadiiCount)

	newRadii = tempRadiiCount.index(max(tempRadiiCount))

	circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, int(meanRadiusEstimate * 0.5), param1 = 50, param2 = 13, minRadius = int(0.75 * newRadii), maxRadius = int(1.25 * newRadii))

	circles = np.uint16(np.around(circles))

	for i in circles[0,:]:
		# draw the outer circle
		cv2.circle(preProcessedImg, (i[0], i[1]), i[2], (0, 255, 0), 2)
	
	print 'Circles with radius', estimate, 'found.\n'

	cv2.imshow('detected circles', preProcessedImg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
