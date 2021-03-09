import cv2
import numpy as np
from math import sqrt

#counts the distance between two points
def distance(point1, point2):
	dif1 = point1[0] - point2[0]
	dif2 = point1[1] - point2[1]
	out = dif1**2 + dif2**2
	return sqrt(out)

#discards the contours with non-uniform width
def letterGradient(contours, origin, mask, desiredPoints, threshold):
	imHeigth = origin.shape[1] #image height
	maskSpan = int((mask - 1)/2) #amount of pixels the mask expands in every direction
	contoursOut = []

	for contour in contours:
		#how many points to skip, so that the contour gets divided in desired amount of parts
		step = int(round(len(contour)/desiredPoints))
		step = max(step, 1) #when desired amount is bigger than the contour, take all the points

		DistList = []

		#pick a point skipping a desired step, and compare it with
		#neighbours specified in a maskSpan
		for PointID in range(0, len(contour)-maskSpan, step):

			X = []
			Y = []
			x = contour[PointID][0][0]
			y = contour[PointID][0][1]
			Point = (x, y)	#position of the picked point

			#get neighbouring pixels positions too
			for neighbour in range(PointID-maskSpan, PointID+maskSpan+1):
				X.append(contour[neighbour][0][0])
				Y.append(imHeigth - contour[neighbour][0][1])

			#interpolate the line
			if(max(Y)-min(Y)) < (max(X)-min(X)):
				Line = np.polyfit(X,Y,1)
				a = Line[0]
				if a == 0: a = 0.01 #can't have 0 for further divisions
				a = -1/a #perpendicular line
			else:
				Line = np.polyfit(Y,X,1)
				a = Line[0]
				if a == 0: a = 0.01

			#find the opposite side for mostly horizontal line
			if -1<a<1:
				right = cv2.pointPolygonTest(contour,(x+1,y),False)

				if right == True:	#letter interior is on the right of the contour point
					while cv2.pointPolygonTest(contour,(x,round(y)),False) > -1:
						x += 1
						y += a
				else:	#letter interior is on the left of the contour point
					while cv2.pointPolygonTest(contour,(x,round(y)),False) > -1:
						x -= 1
						y -= a

			#find the opposite side for mostly vertical line
			else:
				top = cv2.pointPolygonTest(contour,(x,y-1),False)

				if top == True:	#letter interior is on the top of the contour point
					while cv2.pointPolygonTest(contour,(round(x),y),False) > -1:
						x -= 1/a
						y -= 1
				else:	#letter interior is on the bottom of the contour point
					while cv2.pointPolygonTest(contour,(round(x),y),False) > -1:
						x -= 1/a
						y += 1
			
			newPoint = (x, y) #point on the other side of the letter
			dist = distance(Point, newPoint)	#width of the letter
			DistList.append(dist)

		#specify if the widths in multiple points of the letter are uniform enough
		Param = 0
		for i in range(len(DistList)):
			cur = DistList[i]
			pre = DistList[i-1]
			Param += abs(cur - pre)/min(cur, pre)
		Param /= len(DistList)
		if Param < threshold:
			contoursOut.append(contour)

	return contoursOut