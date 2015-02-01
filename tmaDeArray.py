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

	meanRadius = int(math.sqrt((height * width) / (4 * estimate)))

	print 'meanRadius: ', meanRadius

	circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, meanRadius, param1 = 50, param2 = 13, minRadius = int(meanRadius * 0.75), maxRadius = int(meanRadius * 1.25))

	circles = np.uint16(np.around(circles))

	rows = np.zeros(height).astype('int')
	print rows
	cols = np.zeros(width).astype('int')
	print cols
	# rows = []
	# for i in range(height):
#		rows.append(0)
#	cols = []
#	for i in range(width):
#		cols.append(0)

	for i in circles[0,:]:
		rows[i[1]] += 1
		cols[i[0]] += 1

	print rows
	print cols

	for i in rows[0,50]:
		if i > 1:
			cv2.line(preProcessedImg, (0, i[1]), (height, i[1]), (0,0,255), 3)
	for i in rows[100,150]:
		if i > 1:
			cv2.line(preProcessedImg, (0, i[1]), (height, i[1]), (0,0,255), 3)
	for i in rows[200,250]:
		if i > 1:
			cv2.line(preProcessedImg, (0, i[1]), (height, i[1]), (0,0,255), 3)
	for i in rows[300,350]:
		if i > 1:
			cv2.line(preProcessedImg, (0, i[1]), (height, i[1]), (0,0,255), 3)

	for i in cols[0,50]:
		if i > 1:
			cv2.line(preProcessedImg, (i[0], 0), (i[0], width), (0,0,255), 3)
	for i in cols[100,150]:
		if i > 1:
			cv2.line(preProcessedImg, (i[0], 0), (i[0], width), (0,0,255), 3)
	for i in cols[200,250]:
		if i > 1:
			cv2.line(preProcessedImg, (i[0], 0), (i[0], width), (0,0,255), 3)
	for i in cols[300,350]:
		if i > 1:
			cv2.line(preProcessedImg, (i[0], 0), (i[0], width), (0,0,255), 3)

	for i in circles[0,:]:
		# draw the outer circle
		cv2.circle(preProcessedImg, (i[0], i[1]), i[2], (0, 255, 0), 2)
		#draw the center of the circle
		cv2.circle(preProcessedImg, (i[0], i[1]), 2, (0, 0, 255), 3)
	
	print 'Circles with radius', estimate, 'found.\n'

	cv2.imshow('detected circles', preProcessedImg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
