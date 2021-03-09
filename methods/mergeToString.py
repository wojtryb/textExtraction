import cv2

#concanates two lists and returns the outcome as array
def extend(input1, input2):
	cnt = list(input1)
	cnt.extend(list(input2))
	cnt = np.asarray(cnt)
	return cnt

#groups separate letters into strings
def mergeToString(contours, verSim, spacing, verDiff, horDiff):
	strings = []

	#works until all the contours are placed in groups
	while len(contours) > 0:
		current = []
		current.append(contours[0])
		contours.pop(0)	#place one contour in a string and remove it from the input list
		i = 0

		#search the list for neighbours
		while i < len(contours):
			neighbour = contours[i]
			xN,yN,wN,hN = cv2.boundingRect(neighbour)

			#compare the neighbor candidate with every letter in a current string
			for cur in current:
				x,y,w,h = cv2.boundingRect(cur)
				if (min(yN+hN, y+h) - max(yN, y))/min(h, hN) > verSim\
				and min(h, hN)/max(h, hN) > verDiff:					
					dist = min(abs((x + w) - xN), abs((x - wN) - xN))
					if dist/max(w, wN) < spacing\
					and min(w, wN)/max(w, wN) > horDiff:
						#if the conditions are fulfilled, add the neighbor to string						
						current.append(neighbour)
						contours.pop(i)
						i = -1
						break
			i += 1

		#discard strings with only one letter in it
		if len(current) > 1:
			strings.append(current)

	return strings