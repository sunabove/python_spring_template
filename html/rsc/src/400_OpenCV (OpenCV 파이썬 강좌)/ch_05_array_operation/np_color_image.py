import cv2, numpy as np

h = 400; w = 800 ; shape = (h, w) 
blue = np.empty( shape )
green = np.empty( shape )
red = np.empty( shape )

# cross line
blue[ h//2 ] = 255
blue[ :, w//2 ] = 255

green[ h//3 ] = 255
green[ :, w//3 ] = 255

red[ h*2//3 ] = 255
red[ :, w*2//3 ] = 255

blue[ 180:220, 360:440 ] = 255
green[ 190:230, 370:450 ] = 255
red[ 200:240, 380:460 ] = 255

image = np.stack( (blue, green, red), axis=2 )

cv2.imshow('Color image', image )
cv2.waitKey(0)

