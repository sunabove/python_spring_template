import cv2, numpy as np

gray = np.empty( (100, 200) )
gray = np.zeros( (100, 200) )

# horizontal line
gray[ 50 ] = 255
gray[ 50, ] = 255
gray[ 50, : ] = 255
gray[ 50, 0: ] = 255
gray[ 50, :-1 ] = 255
# vertical line
gray[ :, 100 ] = 255

cv2.imshow('Grayscale image', gray)
cv2.waitKey(0)