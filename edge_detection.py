import cv2
import math
import numpy as np

# Read the image
#image = cv2.imread('single_resistor.jpg')
#image = cv2.imread('resistor.png')
#image = cv2.imread('challengingresist.png')
image = cv2.imread('mask_image.jpeg')

brightness_factor = 1.5 # Adjust as needed
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_factor, 0, 255)
brightened_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detector
edges = cv2.Canny(blurred, 10, 150)

# Display the original and edges images
cv2.imshow('Original Image', image)
cv2.imshow('Brightened Image', brightened_image)
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

    # Ensure the angle is in the range [0, 180)
    angle = angle % 180

    # Rotate the image without cropping
    # Pad the image before rotation
    (h, w) = brightened_image.shape[:2]
    max_dim = int(max(h, w) * np.sqrt(2))  # Ensure enough space for rotation
    padded_image = np.full((max_dim, max_dim, 3), 255, dtype=np.uint8)
    x_offset = (max_dim - w) // 2
    y_offset = (max_dim - h) // 2
    padded_image[y_offset:y_offset + h, x_offset:x_offset + w] = brightened_image

    # Rotate the padded image
    center = (max_dim // 2, max_dim // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(padded_image, rotation_matrix, (max_dim, max_dim), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))


    # This i for cropping
    # Crop the original image based on the bounding box of the selected contour
    #resistor_region = image[y:y+h, x:x+w]
    
    # Find contours in the rotated image
    rotated_contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rotated_min_contour_area = 100  # Adjust as needed
    rotated_valid_contours = [contour for contour in rotated_contours if cv2.contourArea(contour) > rotated_min_contour_area]

    # Check if there are valid contours in the rotated image
    if rotated_valid_contours:
        # Select the contour with the maximum area in the rotated image
        rotated_selected_contour = max(rotated_valid_contours, key=cv2.contourArea)

        # Get the bounding box of the rotated resistor region
        rotated_x, rotated_y, rotated_w, rotated_h = cv2.boundingRect(rotated_selected_contour)

        # Crop the rotated image to the resistor region
        cropped_rotated_image = rotated_image[rotated_y:rotated_y + rotated_h, rotated_x:rotated_x + rotated_w]

        # Display the original, padded, rotated, and cropped rotated images
        cv2.imshow('Original Image', brightened_image)
        cv2.imshow('Padded Image', padded_image)
        cv2.imshow('Rotated Image', rotated_image)
        cv2.imshow('Cropped Rotated Image', cropped_rotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Convert to grayscale
        gray = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred_rotated = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detector
        edges_rotated = cv2.Canny(blurred_rotated, 10, 150)

        cv2.imshow('Edges Rotated', edges_rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("No valid contours found in the rotated image.")

    # Rotate the resistor region
    #rotation_matrix = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    #rotated_resistor = cv2.warpAffine(resistor_region, rotation_matrix, (w, h))
    #rotated_resistor = cv2.warpAffine(resistor_region, rotation_matrix, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))


    # Now 'selected_contour' corresponds to the resistor,
    # 'resistor_region' is the cropped image, and 'rotated_resistor' is the rotated image
else:
    print("No valid contours found.")

cv2.imshow('Original Image', image)
cv2.imshow('Resistor Region', cropped_rotated_image)
cv2.imshow('Padded Image', padded_image)
cv2.imshow('Rotated Resistor', rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()