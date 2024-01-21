
import cv2
from matplotlib import pyplot as plt
import math
image = cv2.imread("resistor.jpg") 
# Dividing height and width by 2 to get the center of the image
    
def rotate_and_crop(img,x1,y1,x2,y2):
    height, width = img.shape[:2]
    print(height,width)
    
    ang = math.degrees(math.atan((y2-y1)/(x2-x1)))
    if ang < 0:
        ang+=180
    print("ang is",ang)
    center = (x1,y1)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=ang, scale=1)
    # Rotate the image using cv2.warpAffine
    rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))
    cv2.imshow("rotated",rotated_image)
    cv2.waitKey(0)
    cropped_image = rotated_image[y1-10:y1+10, x1:(width)]
    return cropped_image
# visualize the original and the rotated image
cropped_image = rotate_and_crop(image, 55, 16, 45, 407) #CHANGE these to be variables from top_corner
cv2.imshow('Original image', image)

cv2.imshow('Cropped image', cropped_image)
cv2.imwrite("cropped.jpg",cropped_image)

# imgplot = plt.imshow(image)
# plt.show()
# wait indefinitely, press any key on keyboard to exit
cv2.waitKey(0)