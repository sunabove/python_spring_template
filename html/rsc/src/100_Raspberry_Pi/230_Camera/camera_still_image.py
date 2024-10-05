# camera_still_image.py

print( "Getting a camera ..." )

from picamzero import Camera
from datetime import datetime

cam = Camera()

print( "A camera was prepared." )

# 영상 해상도 설정
#cam.still_size = (640, 480)
#cam.still_size = (1296, 972)
#cam.still_size = (1920, 1080)
cam.still_size = (2592, 1944)

# 영상에 텍스트 추가
cam.annotate( f"Hello, world! : {datetime.now()}")

# 정지 영상 촬영
file_name = "test.jpg"
cam.take_photo( file_name )

print( f"An image ({file_name}) saved." )
