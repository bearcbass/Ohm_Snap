import cv2
import numpy as np

original_image = cv2.imread('threethreebands.jpeg')

masked_image = cv2.imread('threethreebands_masked.jpeg')

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

# Create a mask by extracting the alpha channel from the masked image (assuming it's a PNG with an alpha channel)
mask = masked_image

#inverse_mask = cv2.bitwise_not(mask)

cv2.imshow('Mask Image', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#inverse_mask = cv2.cvtColor(inverse_mask, cv2.COLOR_BGR2GRAY)

result = original_image.copy()

# Print dimensions for debugging
print("Original Image Dimensions:", original_image.shape)
print("Mask Dimensions:", mask.shape)
#print("Inverse Mask Dimensions:", inverse_mask.shape)

result[:, :, 0] = cv2.bitwise_and(original_image[:, :, 0], mask)
result[:, :, 1] = cv2.bitwise_and(original_image[:, :, 1], mask)
result[:, :, 2] = cv2.bitwise_and(original_image[:, :, 2], mask)

cv2.imwrite('result_image.jpg', result)

cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

