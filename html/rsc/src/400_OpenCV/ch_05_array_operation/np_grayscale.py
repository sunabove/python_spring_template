import cv2, numpy as np

gray = np.empty( (400, 800) )

# horizontal line
gray[ 50 ] = 255
#gray[ 200 , : ] = 255
gray[ 200 ] = 255
# vertical line
gray[ : , 100 ] = 255
gray[ : , 700 ] = 255

gray[ 180:220 , 360:440 ] = 255

gray[ 240:280 , 360:440 ] = 255

cv2.imshow( 'Grayscale image', gray )
cv2.waitKey( 0 )