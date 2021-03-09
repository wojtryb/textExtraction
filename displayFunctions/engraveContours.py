import cv2
from random import randint
	
#draws the contours on the original image using random colors
def engraveContours(reference, contours, color):
	if color == False: #fill all with one color
		R = randint(0, 255)
		G = randint(0, 255)
		B = randint(0, 255)
		cv2.fillPoly(reference, pts =contours, color=(R,G,B))
	else:	#different color for each contour
		for con in contours:
			R = randint(0, 255)
			G = randint(0, 255)
			B = randint(0, 255)
			cv2.fillPoly(reference, pts =[con], color=(R,G,B))
		
	#draw bounding boxes around the contours
	for con in contours:
		x,y,w,h = cv2.boundingRect(con)
		cv2.rectangle(reference,(x,y),(x+w,y+h),(255,0,0),2)
	
	return reference