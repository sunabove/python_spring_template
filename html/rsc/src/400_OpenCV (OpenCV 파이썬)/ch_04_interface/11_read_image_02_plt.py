# 11_read_image_02_plt.py
import cv2
from matplotlib import pyplot as plt

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

# 영상 파일 읽기
image = cv2.imread( dir.joinpath( "./img/read_color.jpg" ) )
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# BGR 영상을 RGB 영상으로 변경
plt.imshow( cv2.cvtColor(image, cv2.COLOR_BGR2RGB) )
# BGR 영상을 RGB 영상으로 변경
#plt.imshow( image[ :, :, ::-1 ] )
#plt.imshow( image )

plt.show()