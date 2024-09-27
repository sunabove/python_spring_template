# camera_video.py
# 카메라를 설정 및 초기화 
print("Getting a camera ...")

from picamzero import Camera # picamzero 라이브러리에서 Camera 가져오기

cam = Camera() # Camera 객체 생성

# 비디오 녹화 시작 메시지 출력
duration = 30    # 비디오 녹화 시간
print( f"Recording a video for {duration} seconds ... ", end="" )

# 비디오를 녹화하고, 파일명은 "video_cam.mp4"로 저장
file_name = cam.record_video( f"video_cam_{duration}.mp4", duration)

# 녹화 완료 후 파일명 출력
print("Done.")
print(f"Video File = ({file_name})")

# 마지막으로 카메라 리소스를 정리하는 부분
del cam  # Camera 자원 해제
print("Camera cleaned up.")