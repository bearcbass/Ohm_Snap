import cv2 as cv

import numpy as np 
  
# Read the images 
img = cv.imread("resistor.jpg") 
image = cv.resize(img, (700, 600)) 
  
# # Convert Image to Image HSV 
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV) 

lower = (29, 0, 0) 
upper = (34, 255, 255) 
  
mask = cv.inRange(hsv, lower, upper) 
  
cv.imshow("Mask", mask) 
cv.waitKey(0) 