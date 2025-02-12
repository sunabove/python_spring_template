# 윈도우 크기 변경

# 패키지 임포트
import numpy as np, cv2 as cv, cv2

image = np.zeros( (200, 400), np.uint8) # ndarray 행렬 생성
image.fill( 250 ) # 모든 원소에 255(흰색) 지정

image2 = np.zeros((200, 400), np.uint8) # ndarray 행렬 생성
image2.fill( 10 ) # 모든 원소에 255(흰색) 지정

title1, title2 = 'AUTOSIZE', 'NORMAL'
cv2.namedWindow( title1, cv2.WINDOW_AUTOSIZE) # 윈도우 생성 - 크기 변경 불가
cv2.namedWindow( title2, cv2.WINDOW_NORMAL)   # 크기 변경 가능

# 윈도우 생성은 두가지 옵션 가능
# cv2.WINDOW_AUTOSIZE -> 크기 변경 불가
# cv2.WINDOW_NORMAL -> 크기 변경 가능
cv2.imshow(title1, image )
cv2.imshow(title2, image2 )

# ------------------------------
#cv2.resizeWindow(title1, 400, 300) # 크기 변경 불가
cv2.resizeWindow(title2, 400, 300) # 크기 변경 가능
# -------------------------------
cv2.waitKey(0)            # 윈도우 키 입력 이벤트 대기
cv2.destroyAllWindows()   # 열린 모든 윈도우 제거
