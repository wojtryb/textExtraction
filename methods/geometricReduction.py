import cv2
from numpy import inf

#discard the contours by their geometric properties
def geometricReduction(contours, low, high, points, width, heigth, fill):
	#if points not specified, allow any amount of contour points 
	if points is None:
		points = inf
	
	contoursOut = []

	for contour in contours:
		area = cv2.contourArea(contour)
		x,y,w,h = cv2.boundingRect(contour)
		boxarea = w*h
		if area > low\
		and area < high\
		and len(contour) < points\
		and h/w>width\
		and h/w<heigth\
		and area/boxarea > fill:
			contoursOut.append(contour)
	return contoursOut
