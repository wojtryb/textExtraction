import cv2

#count if two contours can contain the same sign
def countSimilarity(contour1, contour2):
	#position and size of two contours
	x1,y1,w1,h1 = cv2.boundingRect(contour1)
	x2,y2,w2,h2 = cv2.boundingRect(contour2)

	#areas
	area1 = w1 * h1
	area2 = w2 * h2

	#coordinates of bounding boxes vertices to comparison
	x = (x1, x2)
	y = (y1, h2)
	xw = (x1+w1, x2+w2)
	yh = (y1+h1, y2+h2)

	#compare similarity of width and height
	widthSim = min(xw) - max(x)
	heigthSim = min(yh) - max(y)

	#counting the common area of the boxes
	if widthSim <= 0 or heigthSim <= 0:
		commonArea = 0
	else:
		commonArea = widthSim * heigthSim

	similarity = commonArea / (area1 + area2 - commonArea)
	return similarity

#method of eliminating duplicate contours on base of bounding box similarities
def eliminateDuplicates(contours, similarityThreshold):
	out = []
	for i, contour in enumerate(contours):
		similarity = 0

		#check all the remaining contours for similarity
		for candidate in contours[i+1:]:
			similarityTemp = countSimilarity(contour, candidate)
			similarity = max(similarity, similarityTemp) #overwrite with higher value
			
		#discard if the the contour is too similar to any other in a list
		if similarity <= similarityThreshold:
			out.append(contour)
	return out
