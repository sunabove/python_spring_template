# 22_read_camera_write_video.py

import cv2
from pathlib import Path

# 비디오 캡처 객체 생성 (기본 카메라 사용)
camera = cv2.VideoCapture(0)

# 비디오 저장을 위한 설정
fourcc = cv2.VideoWriter_fourcc(*'H264')
dir = Path( __file__ ).resolve().parent # 현재 소스 폴더
out = cv2.VideoWriter( dir.joinpath( "img/output.mp4" ), fourcc, 20.0, (640, 480) )

name = "Your Name"  # 여기에 자신의 이름을 입력하세요

fps = int( camera.get( cv2.CAP_PROP_FPS ) )        # 초당 프레임 수
delay = int(1000/fps)                              # 지연 시간 (ms)
width = int( camera.get(cv2.CAP_PROP_FRAME_WIDTH) )   # 동영상 넓이
height = int( camera.get(cv2.CAP_PROP_FRAME_HEIGHT) ) # 동영상 높이

font = cv2.FONT_HERSHEY_SIMPLEX # 폰트
fs = fontScale = 0.7 # 폰트 크기 비율
fc = fontColor = (0, 255, 0 ) # 폰트 칼라

count = 0  # 프레임 카운트 초기화

while camera.isOpened() and count < 400 :
    ret, frame = camera.read()
    if not ret: break

    count += 1
    
    blue, green, red = cv2.split(frame)             # 영상의 채널 분리 

    if   count > 300 : cv2.add( red  , 100, red )    # red 채널 밝기 100 증가
    elif count > 200 : cv2.add( green, 100, green )  # green 채널 밝기 100 증가
    elif count > 100 : cv2.add( blue , 100, blue )   # blue 채널 밝기 100 증가

    frame = cv2.merge( [blue, green, red] )         # 영상의 채널 합성

    # 프레임에 텍스트 정보 출력
    x, y, dy = 20, 0, 30

    frameInfos = [ f"Name: {name}", f"Frame count: {count}", f"FPS: {fps}", f"Width: {width} px", f"Height: {height} px" ]

    for text in frameInfos : 
        cv2.putText( frame, text, (x, y := y+dy), font, fs, fc, 2, cv2.LINE_AA )

    # 프레임에 사각형 그리기
    th = thickness = 6                      # 사각형 선의 두께
    start_point = ( th, th )                  # 사각형의 시작점
    end_point = ( width//2, height - th)   # 사각형의 끝점
    color = (0, 255, 255)      # 사각형의 색 (BGR: 파랑, 초록, 빨강)
    cv2.rectangle(frame, start_point, end_point, color, thickness)

    # 결과 프레임을 비디오 파일에 저장
    out.write(frame)

    # 프레임을 화면에 표시
    cv2.imshow('Frame', frame) 

    # ESC, Q 키를 누르면 루프를 종료
    if ( cv2.waitKey( delay ) & 0xff ) in ( 27, 81, 113 ) : break
pass

# 모든 리소스 해제
camera.release()
out.release()
cv2.destroyAllWindows()

print( "동영상 변환이 완료되었습니다.")