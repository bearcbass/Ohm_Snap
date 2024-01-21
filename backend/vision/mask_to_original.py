import cv2
import numpy as np


# original_image = cv2.imread("threethreebands.jpeg")
# masked_image = cv2.imread("threethreebands_masked.jpeg")
def mask_to_original(og_image, masked_image):
    # Check the dimensions
    height, width, channels = masked_image.shape

    height, width, channels = og_image.shape
    mask = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    result = og_image.copy()
    result[:, :, 0] = cv2.bitwise_and(og_image[:, :, 0], mask)
    result[:, :, 1] = cv2.bitwise_and(og_image[:, :, 1], mask)
    result[:, :, 2] = cv2.bitwise_and(og_image[:, :, 2], mask)
    print(result.shape)
    return result


if __name__ == "__main__":
    og = cv2.imread("images/threethreebands.jpeg")
    masked = cv2.imread("images/threethreebands_masked.jpeg")
    result = mask_to_original(og, masked)
    cv2.imshow("Result", result)
    cv2.imwrite("result_image.jpg", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
