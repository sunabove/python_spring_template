# 11_read_image_01_cv.py
import cv2

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

#  영상 파일 읽기
image = cv2.imread( dir.joinpath( "./img/read_color.jpg" ) )

# opencv 영상 출력
cv2.imshow( "OpenCV" ,image )
cv2.waitKey( 0 )
cv2.destroyAllWindows()