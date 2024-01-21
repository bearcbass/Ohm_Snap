import cv2
import numpy as np

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

def create_masked_object(original_image, mask_image):
    # Convert the mask image to a binary mask
    _, binary_mask = cv2.threshold(mask_image, 1, 255, cv2.THRESH_BINARY)

    # Convert the binary mask to a 3-channel mask
    colored_mask = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR)

    # Extract the masked object from the original image using the mask
    masked_object = cv2.bitwise_and(original_image, colored_mask)

    return masked_object


result_image = cv2.imread('result_image.jpg')

mask_image = cv2.imread('greenband.jpeg', cv2.IMREAD_GRAYSCALE)

cv2.imshow('Original Image', result_image)
cv2.imshow('mask Image', mask_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

new_image = create_masked_object(result_image, mask_image)

cv2.imshow('new ', new_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Get unique RGB values in the masked area
unique_colors_masked_area = np.unique(new_image.reshape(-1, new_image.shape[2]), axis=0)
num_pixels = len(unique_colors_masked_area)

# Specify the number of sample points
num_samples = int(num_pixels * 0.25) # <- modify this to get more data points
num_samples = num_samples if num_samples % 2 == 0 else num_samples + 1  # Ensure num_samples is even

# Randomly select sample points
sample_points = unique_colors_masked_area[np.random.choice(unique_colors_masked_area.shape[0], num_samples, replace=False)]

# Calculate the average RGB value for each column
average_per_column = np.mean(sample_points, axis=0)

# Display the result image, mask image, masked object, average RGB values, and the sample points
cv2.imshow('Result Image', result_image)
cv2.imshow('Mask Image', mask_image)
cv2.imshow('New Image', new_image)
print("Average RGB Value per Column:\n", average_per_column)

# Create vectors with average RGB values and sampled RGB values
average_rgb_vector = np.round(average_per_column).astype(int)

cv2.waitKey(0)
cv2.destroyAllWindows()