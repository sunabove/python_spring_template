# 15_write_image_02.py

import numpy as np
import cv2

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

image8 = cv2.imread( dir.joinpath( "img/read_color.jpg" ), cv2.IMREAD_COLOR)

image16 = np.uint16(image8*(65535/255))       # 형변환 및 화소 스케일 조정
image32 = np.float32(image8*(1/255))

# 화소값을 확인하기 위한 관심 영역(10,10 위치에서 2x3 크기) 출력
print("image8 행렬의 일부\n %s\n"  % image8[10:12, 10:13])
print("image16 행렬의 일부\n %s\n" % image16[10:12, 10:13])
print("image32 행렬의 일부\n %s\n" % image32[10:12, 10:13])

# 16비트, 32비트 영상 저장
cv2.imwrite( dir.joinpath("img/write_test_16.tif"), image16 )
cv2.imwrite( dir.joinpath("img/write_test_32.tif"), image32 )

# 영상 출력
cv2.imshow( "image16", image16 )
cv2.imshow( "image32", (image32*255).astype("uint8") )

cv2.waitKey(0) # 키 입력 대기