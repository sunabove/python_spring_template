# 카메라를 설정 및 초기화하는 과정 시작
print("Getting a camera...")

# picamzero 라이브러리에서 Camera 모듈을 가져오기
from picamzero import Camera

# Camera 객체 생성
cam = Camera()

# 비디오 녹화 시작 메시지 출력
print("Recording a video... ", end="")

# 10초 동안 비디오를 녹화하고, 파일명은 "video_cam.mp4"로 저장
file_name = cam.record_video("video_cam.mp4", duration=10)

# 녹화 완료 후 파일명 출력
print("Done.")
print(f"Video File = ({file_name})")

# 마지막으로 카메라 리소스를 정리하는 부분
del cam  # Camera 객체 삭제(자원 해제)
print("Camera cleaned up.")