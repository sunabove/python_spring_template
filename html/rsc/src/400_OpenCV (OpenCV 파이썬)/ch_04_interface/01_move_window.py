# 윈도우 이동
import numpy as np
import cv2

image = np.zeros((200, 400), np.uint8) # 행렬 생성
image[:] = 125 # 밝은 회색(100) 바탕 영상 생성

image2 = np.zeros((200, 400), np.uint8) # 행렬 생성
image2[:] = 125 # 밝은 회색(250) 바탕 영상 생성

title1, title2 = 'Position1','Position2'
cv2.namedWindow(title1, cv2.WINDOW_AUTOSIZE) # 원도우 생성 및 크기 조정 옵션
cv2.namedWindow(title2)

cv2.moveWindow(title1, 150, 150) # 윈도우 이동 - 위치 지정
cv2.moveWindow(title2, 400, 50)

cv2.imshow(title1, image) # 행렬 원소를 영상으로 표시
cv2.imshow(title2, image2)

cv2.waitKey(0) # 윈도우 키 이벤트 대기
#input( "Enter to quit" )
cv2.destroyAllWindows() # 열린 모든 윈도우 제거 