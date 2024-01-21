import cv2 as cv

import numpy as np 

# Read the images 
img = cv.imread("single_resistor.jpg") 

# Check if the image is loaded successfully
if img is not None:
    # Display the image
    cv.imshow("image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("Failed to load the image.")

image = cv.resize(img, (400, 300)) 

# # Convert Image to Image HSV 
hsv = cv.cvtColor(image, cv.COLOR_BGR2LAB)

lower = (50, 0, 0) 
upper = (100, 220, 220) 

mask = cv.inRange(hsv, lower, upper) 

cv.imshow("Mask", mask) 
cv.waitKey(0) 