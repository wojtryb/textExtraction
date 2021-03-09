# Text extraction
Python implementation of the classic methods for finding the text on images using OpenCV. False positives can be removed from detected contours with four methods: geometric reduction, letter gradient, string merging and multiple threshold.

## Example images:
Example of the detected text:
- ![example image 1](https://github.com/wojtryb/textExtraction/tree/master/outputExamples/img1.png?raw=true)

## Requirements:
The application was tested with **Python 3.8.5** and **OpenCV 4.2.0**. Newer versions may require changes in the code, 

## Installation:
- make sure Python and OpenCV are installed.
- Edit the **main.py** file to pick a desired image and parametrize the functions.  
- Run the **main.py** file.

## Methods:
- **geometric reduction** is the most basic method of removing false positives from a list of detected contours. It uses the size of bounding boxes, their areas, width to height ratio to remove the most obvious non-letter instances. Using this method is necessary for performance reasons.
- **letter gradient** uses the fact, that width of the letters is usually uniform across the whole sign. This method divides the contour into multiple parts, calculates perpendicular line to each point, and finds the intersection of the line with other side of the letter. Contours with too big differences in width calculated this way are discarded.
- **string merging** assumes that letters form horizontal strings with the signs having the similar size and height. Contours without any neighbours that can satisfy those conditions can be removed from the list.
- **multiple threshold** method can be used when low contrast letters are not aquired at the beginning of the alghoritm. The image is being thresholded multiple times and the letters from various iterations can form one output. Duplicates of the same letters are being removed.   

## Licence:
The project is part of a engineering thesis. Please don't sell or redistribute. Use for educational purposes only.
