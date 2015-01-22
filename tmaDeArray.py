import cv2
import cv2.cv as cv
import numpy as np

imgLoc = raw_input("Enter the location of the picture file to be analyzed: ")
estimate = int(input("Enter a rough estimate for the number of cores in this TMA: "))

img = cv2.imread(imgLoc, 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

print 'Circles with radius ', estimate, ' found.\n'

circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 30, minRadius = 0, maxRadius = 0)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
	# draw the outer circle
	cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
	#draw the center of the circle
	cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
