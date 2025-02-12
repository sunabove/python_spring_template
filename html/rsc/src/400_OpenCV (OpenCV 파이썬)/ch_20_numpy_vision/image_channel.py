# coding: utf-8
import cv2
# Load a color image 
img = cv2.imread('messi5.jpg')
# split the image into 3 channel data
blue  = img[:, :, 0]  # blue channel data
green = img[:, :, 1]  # green channel data
red   = img[:, :, 2]  # red channel data

cv2.imshow('Blue channel', blue)
cv2.imshow('Green channel', green)
cv2.imshow('Red channel', red)

cv2.waitKey(0)
cv2.destroyAllWindows() 