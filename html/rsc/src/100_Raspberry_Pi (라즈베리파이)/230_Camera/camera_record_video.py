# camera_record_video.py

print( "Getting a camera ..." )

from picamzero import Camera
from datetime import datetime

cam = Camera()

print( "A camera was prepared." )

# 영상 해상도 설정
#cam.still_size = (640, 480)
cam.still_size = (1296, 972)
#cam.still_size = (1920, 1080)
#cam.still_size = (2592, 1944)

# 영상에 텍스트 추가
cam.annotate( f"Hello, world! : {datetime.now()}")

# 정지 영상 촬영
file_name = "test.mp4"
duration = 10  # 촬영 시간
print( f"Recording a video for {duration} seconds ..." )
cam.record_video( file_name, duration=duration)

print( f"A video ({file_name}) recored." )