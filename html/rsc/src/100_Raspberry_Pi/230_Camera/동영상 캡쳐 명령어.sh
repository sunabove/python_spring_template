# 카메라 연결 확인
libcamera-hello --list-camera 

# 640x480 동영상 캡쳐
rpicam-vid -o video_1_640_480.h264 -n --width 640 --height 480 -t 120s

# 1286x972 동영상 캡쳐
rpicam-vid -o video_2_1296_972.h264 -n --width 1296 --height 972 -t 120s

# 1920x1080 동영상 캡쳐
rpicam-vid -o video_3_1920_1080.h264 -n --width 1920 --height 1080 -t 120s
