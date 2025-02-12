# coding: utf-8
import cv2
# Load a color image 
img = cv2.imread('messi5.jpg')
# print image size
shape = img.shape 
print( "image size = ", shape ) 
# image height, width and channel count
h = shape[0] 
w = shape[1]
channel = shape[1]
print( f"h = {h}, w = {w}, channel = {channel}" )