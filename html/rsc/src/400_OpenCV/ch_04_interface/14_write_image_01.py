# 14_write_image_01.py

import cv2
from matplotlib import pyplot as plt

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

# 영상을 행렬로 읽어 들임
image = cv2.imread( dir.joinpath( "img/read_color.jpg" ), cv2.IMREAD_COLOR) 

params_jpg = (cv2.IMWRITE_JPEG_QUALITY, 10)       # JPEG 화질 설정
params_png = [cv2.IMWRITE_PNG_COMPRESSION, 9]     # PNG 압축 레벨 설정

# 행렬을 영상 파일로 저장
cv2.imwrite( dir.joinpath( "img/write_test1.jpg" ), image) # 기본 화질로 저장
cv2.imwrite( dir.joinpath( "img/write_test2.jpg" ), image, params_jpg) # 지정 화질로 저장 (저화질)
cv2.imwrite( dir.joinpath( "img/write_test3.png" ), image, params_png)
cv2.imwrite( dir.joinpath( "img/write_test4.bmp" ), image)         # BMP 파일로 저장

print("저장 완료")

# 저장된 이미지 출력하여 확인하기
cv2.imshow( "img/write_test1.jpg", cv2.imread( dir.joinpath( "img/write_test1.jpg" ) ) ) 
cv2.imshow( "img/write_test2.jpg", cv2.imread( dir.joinpath( "img/write_test2.jpg" ) ) ) 
cv2.imshow( "img/write_test3.png", cv2.imread( dir.joinpath( "img/write_test3.png" ) ) ) 
cv2.imshow( "img/write_test4.bmp", cv2.imread( dir.joinpath( "img/write_test4.bmp" ) ) ) 

cv2.waitKey(0) # 키 입력 대기