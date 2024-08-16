# picozero 패키지에서 Speaker 임포트하여 부저 제어
from picozero import Speaker
# time 모듈에서 sleep 함수를 임포트하여 시간 지연 사용
from time import sleep

# Buzzer 객체 생성, GPIO 4번 핀에 연결된 부저를 제어
buzzer = Speaker(4)

# 부저가 비프음을 울리도록 설정
# on_time: 부저가 켜져 있는 시간 (초 단위)
# off_time: 부저가 꺼져 있는 시간 (초 단위)
# n: 비프음의 반복 횟수
buzzer.beep(on_time=1, off_time=0.5, n=4, wait=1)

# 부저 자원을 정리
buzzer.close()
