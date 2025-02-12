# 13_read_image_05_32bit_image.py
import cv2
from matplotlib import pyplot as plt

# 영상의 행렬 정보 출력
def print_mat_info( image ):
    # 영상 채널 갯수
    nchannel = 3 if image.ndim == 3 else 1

    print( f"type: {type(image)}, data_type: {image.dtype}, ndim: {image.ndim},  channel: {nchannel}" )
pass

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

title1, title2 = "16bit unchanged", "32bit unchanged"  # 윈도우 이름
color2unchanged1 = cv2.imread( dir.joinpath( "img/read_16.tif" ), cv2.IMREAD_UNCHANGED)
color2unchanged2 = cv2.imread( dir.joinpath( "img/read_32.tif" ), cv2.IMREAD_UNCHANGED)

print("16/32비트 영상 행렬 좌표 (10, 10) 화소값")
print(title1, "원소 자료형 ",  type(color2unchanged1[10][10][0]))   # 원소 자료형
print(title1, "화소값(3원소) 샘플", color2unchanged1[10, 10] )      # 행렬 내 한 화소 값 표시
print(title2, "원소 자료형 ",  type(color2unchanged2[10][10][0]))
print(title2, "화소값(3원소) 샘플", color2unchanged2[10, 10] )
print()

print_mat_info( color2unchanged1 ) # 행렬 정보 출력
print_mat_info( color2unchanged2 )

cv2.imshow(title1, color2unchanged1 )
cv2.imshow(title2, (color2unchanged2*255).astype("uint8"))
cv2.waitKey(0) # 키 입력 대기