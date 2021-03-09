import cv2
import numpy as np 

#prints just the contours on black image
def printOnBlack(reference, contours, name = 'temp'):
	imWidth = reference.shape[0]
	imHeigth = reference.shape[1]
	img = np.zeros((imWidth,imHeigth,3), np.uint8)
	for cnt in contours:
		cv2.drawContours(img, [cnt], 0, (255,255,255), 3)
	print(len(contours))
	img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
	cv2.imshow('Output', img)
	# cv2.imwrite(name + '_.png', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	quit()
