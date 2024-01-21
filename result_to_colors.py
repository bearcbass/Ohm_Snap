
import cv2
import numpy as np

"""
Sadly this approach doesnt work, 
it does not take into account any edges, so it will look 
at the background and count that as a color. 

I think using SAM again would be the better alternative.

Then we can use these ranges to determine the correct values
"""

def create_hsv_ranges():
    # Define HSV color ranges for various colors
    color_ranges = {
        'red': ([0, 100, 100], [10, 255, 255]),
        'blue': ([110, 100, 100], [130, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'brown': ([0, 60, 60], [20, 255, 255]),
        'violet': ([130, 100, 100], [160, 255, 255]),
        'orange': ([10, 100, 100], [20, 255, 255]),
        'green': ([40, 100, 100], [80, 255, 255]),
    }

    return color_ranges

"""
First import all of the images needed
"""
result_image = cv2.imread('result_image.jpg')

# Convert image to HSV
result_hsv = cv2.cvtColor(result_image, cv2.COLOR_BGR2HSV)

# Convert image to grayscale
result_gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)

"""
Next make sure all dimensions work
"""
height1, width1, channels1 = result_image.shape

print(f"Height: {height1}, Width: {width1}, Channels: {channels1}")

height2, width2, channels2 = result_hsv.shape

print(f"Height: {height2}, Width: {width2}, Channels: {channels2}")

height3, width3 = result_gray.shape

print(f"Height: {height3}, Width: {width3}")

if (height3 != height2 or height2 != height1 or height1 != height3):
    print("Dimensions don't Match")

if (width3 != width2 or width2 != width1 or width1 != width3):
    print("Dimensions don't Match")


cv2.imshow('Original Image', result_image)
#cv2.imshow('Colored Image', result_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Create binary vector to indicate presence of colors
color_vector = []

# Check presence of each color in the resistor
for color, (lower, upper) in create_hsv_ranges().items():
    color_mask = cv2.inRange(result_hsv, np.array(lower), np.array(upper))
    color_present = cv2.countNonZero(color_mask) > 0
    color_vector.append((color, color_present))

# Print the color vector
print("Resistor Color Vector:", color_vector)

# Display the images (commented out for now)
cv2.imshow('Original Image', result_image)
cv2.imshow('Colored Image', result_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(color_vector)
