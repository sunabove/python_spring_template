# 마우스 & 트랙바 이벤트

import numpy as np
import cv2

# 트랙바 콜백
def onChange(value):
    pass
pass

# 마우스 콜백
def onMouse(event, x, y, flags, param):
    global image, bar_name

    if event == cv2.EVENT_RBUTTONDOWN: # 오른쪽 마우스 클릭시
        image[ : ] = cv2.getTrackbarPos( bar_name, title ) + 10
        cv2.setTrackbarPos(bar_name, title, image[0][0] )
        cv2.imshow(title, image)
    elif event == cv2.EVENT_LBUTTONDOWN: # 왼쪽 마우스 클릭시
        image[ : ] = cv2.getTrackbarPos( bar_name, title ) - 10
        cv2.setTrackbarPos(bar_name, title, image[0][0])
        cv2.imshow(title, image)
    pass
pass

image = np.zeros((300, 500), np.uint8) # 영상 생성
title = "Mouse & Trackbar  event"
bar_name = "Brightness"
cv2.imshow(title, image)

cv2.createTrackbar(bar_name, title, 0, 255, onChange) # 트랙바 콜백
cv2.setMouseCallback(title, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()