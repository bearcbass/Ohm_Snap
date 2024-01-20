import cv2
import numpy as np

# Read the image
#image = cv2.imread('single_resistor.jpg')
image = cv2.imread('challengingresist.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detector
edges = cv2.Canny(blurred, 50, 150)

# Display the original and edges images
cv2.imshow('Original Image', image)
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Assuming 'edges' is the result of edge detection
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on minimum area (you may adjust this threshold)
min_contour_area = 100  # Adjust as needed
valid_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

# Check if there are valid contours
if valid_contours:
    # Select the contour with the maximum area
    selected_contour = max(valid_contours, key=cv2.contourArea)

    # Fit a bounding rectangle around the contour
    rect = cv2.minAreaRect(selected_contour)

    # Get the angle of the major axis of the bounding rectangle
    angle = rect[2]

    # Assuming 'image' is the original image
    x, y, w, h = cv2.boundingRect(selected_contour)

    # Crop the original image based on the bounding box of the selected contour
    resistor_region = image[y:y+h, x:x+w]

    # Rotate the resistor region
    rotation_matrix = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    rotated_resistor = cv2.warpAffine(resistor_region, rotation_matrix, (w, h))

    # Now 'selected_contour' corresponds to the resistor,
    # 'resistor_region' is the cropped image, and 'rotated_resistor' is the rotated image
else:
    print("No valid contours found.")