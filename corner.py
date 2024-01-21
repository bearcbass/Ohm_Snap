import numpy as np 
import cv2 
from matplotlib import pyplot as plt 
  
  
# read the image 
img = cv2.imread('resistorBW.jpg') 

def top_corner(img):
    min = 0,0
    for i in range(len(img)):
        for k in range(len(img[0])):
            if((img[i,k]-[0,0,0]).all()):
                min = [i,k]
                return(min)
def bottom_corner(img):
    min = 0,0
    for i in range(len(img)-1,0,-1):
        for k in range(len(img[0])-1,0,-1):
            if((img[i,k]-[0,0,0]).all()):
                min = [i,k]
                return(min)
print(top_corner(img))
print(bottom_corner(img))