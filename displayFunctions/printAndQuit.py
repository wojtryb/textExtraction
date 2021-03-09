import cv2

#shows the original image with drawn contours 
def printAndQuit(reference, name = 'temp'):

	reference = cv2.resize(reference, (0,0), fx=0.3, fy=0.3)
	cv2.imshow('Output', reference)
	cv2.imwrite(name + '_.png', reference)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	quit()