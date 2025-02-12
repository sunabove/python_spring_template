# 마우스 이벤트 예제

import numpy as np
import cv2

def onMouse(event, x, y, flags, param) : # 마우스 콜백 함수 정의
    if event == cv2.EVENT_LBUTTONDOWN :
        print("Left down")
    elif event == cv2.EVENT_LBUTTONUP :
        print("Left up")    
    elif event == cv2.EVENT_RBUTTONDOWN :
        print("Right Down")
    elif event == cv2.EVENT_RBUTTONUP :
        print("Right up")
    elif event == cv2.EVENT_LBUTTONDBLCLK :
        print("Left Double Click")
    elif event == cv2.EVENT_RBUTTONDBLCLK :
        print("Right Double Click")
    pass
pass

image = np.full((200, 300), 255, np.uint8)

title1, title2 = 'Mouse Event1','Mouse Event2'
cv2.imshow(title1, image)
cv2.imshow(title2, image)

cv2.setMouseCallback(title1, onMouse) # 마우스 콜백 함수 등록
cv2.waitKey(0)
cv2.destroyAllWindows()