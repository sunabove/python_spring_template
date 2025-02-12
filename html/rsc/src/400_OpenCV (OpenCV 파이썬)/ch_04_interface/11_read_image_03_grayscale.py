# 11_read_image_00.py

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

# 원본 그레이 영상을 그레이 영상으로 읽음.
gray2gray  = cv2.imread( dir.joinpath( "./img/read_gray.jpg" ), cv2.IMREAD_GRAYSCALE) 
# 원본 그레이 영상을 컬러 영상으로 읽음.
gray2color = cv2.imread( dir.joinpath( "./img/read_gray.jpg" ), cv2.IMREAD_COLOR)

print_mat_info( gray2gray )
print_mat_info( gray2color )

cv2.imshow( "gray2gray" , gray2gray )
cv2.imshow( "gray2color" , gray2color )

cv2.waitKey( 0 )
cv2.destroyAllWindows()