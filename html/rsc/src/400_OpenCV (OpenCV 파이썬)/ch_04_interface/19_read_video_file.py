# 19_read_video_file.py

import cv2

# 그림자 문자 출력
def put_string(frame, text, pt, value=None, color=(120, 200, 90)) :
    text = str(text) + str(value)
    shade = (pt[0] + 2, pt[1] + 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, shade, font, 0.7, (0, 0, 0), 2) # 그림자 효과
    cv2.putText(frame, text, pt   , font, 0.7, color, 2) # 작성 문자
pass

# 현재 소스 파일의 폴더 경로
from pathlib import Path
dir = Path( __file__ ).resolve().parent

capture = cv2.VideoCapture( dir.joinpath( "img/write_video.avi" ) )    # 동영상 파일 읽기
if not capture.isOpened(): raise Exception("동영상 파일 읽기 불가")	

frame_rate = capture.get(cv2.CAP_PROP_FPS)           # 초당 프레임 수
delay = int(1000/frame_rate)                         # 지연 시간
frame_cnt = 0                                        # 현재 프레임 번호
height = int( capture.get(cv2.CAP_PROP_FRAME_HEIGHT) )  # 동영상 높이

while True:
    ret, frame = capture.read()
    if not ret or cv2.waitKey(delay) >= 0: break    # 프레임 간 지연 시간 지정
    blue, green, red = cv2.split(frame)             # 컬러 영상 채널 분리
    frame_cnt += 1    # 프레임 카운트 1씩 증가

    if 100 <= frame_cnt < 200: cv2.add(blue, 100, blue)     # blue 채널 밝기 증가
    elif 200 <= frame_cnt < 300: cv2.add(green, 100, green) # green 채널 밝기 증가
    elif 300 <= frame_cnt < 400: cv2.add(red  , 100, red)   # red 채널 밝기 증가

    '''
    if 100 <= frame_cnt < 200: blue += 100     # blue 채널 밝기 증가
    elif 200 <= frame_cnt < 300: green += 100  # green 채널 밝기 증가
    elif 300 <= frame_cnt < 400: red += 100    # red 채널 밝기 증가
    '''

    frame = cv2.merge( [blue, green, red] )                 # 단일채널 영상 합성
    put_string(frame, "frame_cnt : ", (20, height//2), frame_cnt)
    cv2.imshow("Read Video File", frame)
pass

capture.release()