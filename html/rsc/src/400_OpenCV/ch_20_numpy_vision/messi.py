# coding: utf-8
import cv2
# Load a color image 
img = cv2.imread('messi5.jpg')

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()