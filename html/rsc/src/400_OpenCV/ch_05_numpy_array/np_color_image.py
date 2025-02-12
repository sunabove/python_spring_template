import cv2, numpy as np

h = 100; w = 200; shape = (h, w)

blue = np.empty( shape )
# cross line
blue[ 50 ] = 255
blue[ 50:61 ] = 255
blue[ 50:51 , ] = 255
blue[ 50:51 ,  :  ] = 255
blue[ 50:51 ,  0 :  ] = 255
blue[ 50:51 ,  0 : -1  ] = 255
blue[ 50:51 ,    : -1  ] = 255

# blue[ , 100 ] = 255 # 컴파일 에러 발생
blue[  : , 100 ] = 255
#blue[ 0: , 100 ] = 255
#blue[ 0: -1 , 100 ] = 255
#blue[  : -1 , 100 ] = 255

green = np.empty( shape )
red = np.empty( shape )

green[ 10:20, 20:50 ] = 255
red[ 15:25, 25:55 ] = 255

image = np.stack( (blue, green, red), axis=2 )

cv2.imshow('Color image', image )
cv2.waitKey(0)