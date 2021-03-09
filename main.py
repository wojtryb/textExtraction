import cv2
import numpy as np
import math

from methods.geometricReduction import geometricReduction
from methods.mergeToString import mergeToString
from methods.letterGradient import letterGradient
from methods.eliminateDuplicates import eliminateDuplicates

from displayFunctions.engraveContours import engraveContours
from displayFunctions.printAndQuit import printAndQuit
from displayFunctions.printOnBlack import printOnBlack

#specify an image to load
name = '2'
NAME = 'inputImages/' + name + '.jpg'
SCALE = 1.0

#------------------------------------#

#pick methods to be used
GEOMETRICREDUCTION = True	#use method 0 (should always be used due to performance)
MERGETOSTRING = True		#use method 1
LETTERGRADIENT = True		#use method 2
MULTITHRESHOLD = True		#use method 3

PRINTONBLACK = False		#display only extracted contours

#------------------------------------#

#read the image and its blackAndWhite version
img = cv2.imread(NAME,0)
small = cv2.resize(img, (0,0), fx=SCALE, fy=SCALE)

ref = cv2.imread(NAME)
ref = cv2.resize(ref, (0,0), fx=SCALE, fy=SCALE)

#-------------acquisition--------------#

contours = []

#multithreshold method allows to perform the aquisition process multiple times
#with different thresholds (HDR-like) and then merge the results into one. 
if MULTITHRESHOLD:
	thresholdValues = [80, 127, 170]
else:
	thresholdValues = [127]

for ThresIter in thresholdValues:
	_,thresh = cv2.threshold(small,ThresIter,255,0)
	con,_ = cv2.findContours(thresh, 1, method=cv2.CHAIN_APPROX_NONE)

	#-------------reduction----------------#

	#geometric reduction is the most basic method of discarding contours
	#using their geometric properties to differentiate text from other elements
	if GEOMETRICREDUCTION:	#method 0
		con = geometricReduction(
			contours = con, #current list of contours
			low = 480,		#smallest area inside the contour
			high =  36000,	#biggest area inside the contour
			points = None,	#maximal amount of points forming the contour (not used)
			width = 0.6,	#minimal height to width ratio
			heigth = 6,		#maximal height to width ratio
			fill = 0.3		#minimal part of the bounding box that the contour fills
			)

	#-----------letter gradient------------#

	#method of discarding the contours by thir width. Line perpendicular to the
	#contour is counted in its multiple points. If a contour is a letter, the lenght of those
	#sections should be similar in all the points 
	if LETTERGRADIENT: #method 2
		con = letterGradient(
			contours = con, #list of contours
			origin = small, #the original image
			mask = 5,		#size of the square used to count parameters of line perp. to contour
			desiredPoints = 20,	#amount of points specified on a contour
			threshold = 2.5	#threshold for deciding if the contour should he kept
			)


	#-----------string merging-------------#

	#method of discarding the contours without any neighbours. Letters tend to form strings
	#so those without horizontal neighbours of similar size can be deleted.
	if MERGETOSTRING:		#method 1
		strings = mergeToString(
			contours = con.copy(),	#list of contours
			verSim = 0.65,			#vertical similarity (0-no shared pixels vertically, 1-one includes the neighbor)
			spacing = 1.65,			#how much horizontal spacing is allowed (in bounding box widths)
			verDiff = 0.5,			#maximal difference in heights (bigger to smaller)
			horDiff = 0.4,			#maximal difference in widths (bigger to smaller)
			)
	else:
		strings = [con]

	con = []
	for string in strings:
		con.extend(string)

	contours.extend(con)

#if alghoritm was used multiple times with different thresholds, duplicates of the same
#letters from multiple iterations need to be removed
if MULTITHRESHOLD:
	contours = eliminateDuplicates(
		contours = contours.copy(),
		similarityThreshold = 0.88
		)

#separate string merging is required when using multithreshold method
if MERGETOSTRING and MULTITHRESHOLD:
	strings = mergeToString(contours.copy(), 0.65, 1.65, 0.5, 0.4)

#draw extracted contours
for string in strings:
	ref = engraveContours(ref, string, False)

#choose between showing the original image with drawn contours or just contours on black image
if PRINTONBLACK:
	printOnBlack(ref, contours, name)
else:
	printAndQuit(ref, name)