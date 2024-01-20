import cv2
import numpy as np

masked_image = cv2.imread('threethreebands.jpeg')

original_image = cv2.imread('threethreebands_masked.jpeg')

# Check the dimensions
height, width, channels = masked_image.shape

height, width, channels = original_image.shape

# Print the dimensions
print(f"Height: {height}, Width: {width}, Channels: {channels}")

# Print the dimensions
print(f"Height: {height}, Width: {width}, Channels: {channels}")

cv2.imshow('Masked Image', masked_image)
cv2.imshow('Original Image', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()