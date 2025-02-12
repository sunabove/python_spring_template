# 트랙바 이벤트 예제
import numpy as np
import cv2

image = np.zeros((300, 500), np.uint8) # 영상 생성
title = "trackbar event"

def onChange(value): # 트랙바 콜백 함수
    image[:] = value # 트랙바의 값으로 이미지 값을 설정
    cv2.imshow(title, image)
pass

cv2.imshow(title, image)

cv2.createTrackbar("Brightness", title, 0, 255, onChange) # 트랙바 콜백 설정
cv2.waitKey(0)
cv2.destroyAllWindows()