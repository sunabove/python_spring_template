# 18_write_camera_frame.py

import cv2

capture = cv2.VideoCapture(0)    # 0번 카메라 연결
if capture.isOpened() == False: raise Exception("카메라 연결 안됨")

fps = capture.get( cv2.CAP_PROP_FPS )            # 초당 프레임 수
delay = round( 1_000/fps )                       # 프레임 간 지연 시간
width = int( capture.get(cv2.CAP_PROP_FRAME_WIDTH) )   # 동영상 넓이
height = int( capture.get(cv2.CAP_PROP_FRAME_HEIGHT) ) # 동영상 높이
size  = ( width, height )                        # 동영상 파일 해상도
fourcc = cv2.VideoWriter_fourcc(*'H264')         # 압축 코덱 설정

# 카메라 속성 콘솔창에 출력
print("프레임 해상도:", size )
print("압축 코덱 숫자:", fourcc)
print("delay: %2d ms" % delay)
print("fps: %.2f" % fps)

capture.set(cv2.CAP_PROP_ZOOM, 1)                 # 카메라 속성 지정
capture.set(cv2.CAP_PROP_FOCUS, 0)                # 카메라 포커서 설정
capture.set(cv2.CAP_PROP_FRAME_WIDTH , size[0])   # 해상도 넓이 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])   # 해상도 높이 설정

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

# 동영상 파일 개방 및 코덱, 해상도 설정
filename = dir.joinpath( "img/write_video.mp4" )
writer = cv2.VideoWriter( filename=filename, fourcc=fourcc, fps=fps, frameSize=size )

if writer.isOpened() == False: raise Exception("동영상 파일 쓰기 불가")

while True: # 무한 반복
    ret, frame = capture.read()             # 카메라 영상 받기
    if not ret: break  # 최근접 루프 탈출
    if cv2.waitKey( delay ) >= 0: break # 최근접 루프 탈출

    writer.write( frame )               # 프레임을 동영상으로 저장
    cv2.imshow( "View Frame from Camera" , frame)
pass

writer.release()   # 쓰기 동영상 파일 자원 해제
capture.release()  # 캡쳐 카메라 자원 해제

print( f"동영상 저장이 완료되었습니다. {filename.name}" )