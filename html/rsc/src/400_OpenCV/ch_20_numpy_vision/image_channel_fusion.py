# coding: utf-8
import cv2, numpy as np
# Load a color image 
img = cv2.imread('messi5.jpg')

# split the image into 3 channel data
blue  = img[:, :, 0]  # blue channel data
green = img[:, :, 1]  # green channel data
red   = img[:, :, 2]  # red channel data

fusion =  (blue + green + red )/3

cv2.imshow('Fusion channels', fusion) 

cv2.waitKey(0)
cv2.destroyAllWindows() 