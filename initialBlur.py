import math
import cv2
import cv2.cv as cv
import numpy as np
from array import array

class initialBlur:

	maxIntensity = 255.0

	phi = 1
	theta = 1

	areaList = [0]

	imgLoc = raw_input("Enter the location of the picture file to be analyzed: ")
	
	preProcessedImg = cv2.imread(imgLoc)
	cv2.imshow('pre-processing', preProcessedImg)
	
	img = cv2.imread(imgLoc)

	tempimg = cv2.imread(imgLoc, 0)
	tempimg = cv2.medianBlur(tempimg, 5)
	
	height, width = img.shape[:2]

	height = int(height / 50)
	width = int(width / 50)
	
	if height % 2 == 0:
		height = height + 1
	if width % 2 == 0:
		width = width + 1

	# img = cv2.GaussianBlur(img,(height,width),0)
	cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cimg = cv2.bilateralFilter(cimg, 11, 17, 17)	
	cv2.imshow('fifty',cimg)

	# ret,newimg = cv2.threshold(cimg,1,255,cv2.THRESH_BINARY)	

	# cv2.imshow('newfifty',newimg)

	edged = cv2.Canny(cimg, 30, 200)
	contours = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
	for i in range(0, len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if area >= math.pi * 100:
			areaList.append(int(area / math.pi))
	
	maxOfList = max(areaList)
	numOfAreas = len(areaList)

	freqList = [0]
	n = 1
	cont = True
	start = False
	listOfRadii = [0]

	while cont:
		count = 0
		for i in range(0, len(areaList)):
			curArea = areaList[i]
			if curArea > ((n ** 2) * 0.75) and curArea < ((n ** 2) * 1.25):
				count = count + 1
		if count >= 2 * freqList[len(freqList) - 1] and count >= numOfAreas * 0.1:
			start = True
		if count <= 0.5 * freqList[len(freqList) - 1] or count <= numOfAreas * 0.1:
			start = False
		if start:
			listOfRadii.append(n)
		freqList.append(count)

		n = n + 1
		if (n**2) > maxOfList:
			cont = False

	meanRadiusEstimate = listOfRadii[int(len(listOfRadii)/2)]

	circles = cv2.HoughCircles(tempimg, cv.CV_HOUGH_GRADIENT, 1, int(meanRadiusEstimate * 1.5), param1 = 50, param2 = 13, minRadius = listOfRadii[1], maxRadius = listOfRadii[len(listOfRadii) - 1])

	circles = np.uint16(np.around(circles))

	for i in circles[0,:]:
		# draw the outer circle
		cv2.circle(preProcessedImg, (i[0], i[1]), i[2], (0, 255, 0), 2)
	
	cv2.imshow('detected circles', preProcessedImg)

	for cnt in contours:
		cv2.drawContours(cimg, [cnt], 0, 0, -1)
	# cv2.drawContours(cimg, contours, -1, (0,255,0), 3)
	cimg = cv2.GaussianBlur(cimg,(height,width),0)
	
	cv2.imshow('contours of truth',cimg)
	cv2.imshow('0', edged)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
