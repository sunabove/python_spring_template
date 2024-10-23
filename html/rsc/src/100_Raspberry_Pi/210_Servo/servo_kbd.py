# servo_kbd.py
# 키보드 입력을 통해 서보 모터의 각도를 제어하는 프로그램
# GPIO 핀 17을 사용하여 PWM 신호를 생성하고 서보 모터를 제어합니다.

import curses  # 키보드 입력을 처리하는 curses 라이브러리 임포트
import RPi.GPIO as GPIO  # Raspberry Pi GPIO 제어를 위한 표준 라이브러리 임포트
from time import sleep   # 프로그램에 대기(일시 정지) 기능을 추가하기 위한 sleep 함수 임포트

def main(stdscr): 
    GPIO.setwarnings(False)  # GPIO 관련 경고를 비활성화
    GPIO.setmode(GPIO.BCM)   # BCM 핀 번호 체계를 사용하도록 설정

    GPIO.setup(17, GPIO.OUT)  # GPIO 핀 17을 출력 모드로 설정

    duration = 0.5  # 모터 움직임 간의 대기 시간 (초)
    frequency = 50  # 서보 모터의 PWM 주파수 (50Hz)
    dc = 0  # 초기 듀티 사이클을 0으로 설정
    dc_increment = 2.5/4 # 듀티 사이클을 변경할 때 사용할 증분 값
    count = 0 # 실행 횟수

    p = GPIO.PWM(17, frequency)  # GPIO 핀 17에서 50Hz로 PWM 시작
    p.start(0)  # PWM을 시작하고 듀티 사이클을 0으로 설정
    sleep(duration)  # 초기화 후 잠시 대기
    p.ChangeDutyCycle(dc)  # 초기 듀티 사이클 설정
    sleep(duration)  # 잠시 대기

    # 화면에 안내 메시지 출력
    stdscr.addstr(0, 0, "Enter q to quit!")  # 프로그램 종료 안내
    stdscr.addstr(1, 0, "Use ← ↑ → ↓ key to control servo!")  # 방향키로 서보 모터 제어 안내
    stdscr.addstr(2, 0, "")  # 빈 줄 추가
    stdscr.addstr(5, 0, f"[{count:3d}] Duty cycle = {dc:5.2f}")  # 현재 듀티 사이클 출력

    next_key = None  # 다음 입력을 저장할 변수

    # 무한 루프: 키 입력을 통해 서보 모터 제어
    while 1:
        curses.halfdelay(1)  # 0.1초 대기 후 입력 대기

        # 현재 입력을 확인
        if next_key is None:
            key = stdscr.getch()  # 키 입력 대기
        else:
            key = next_key  # 이전에 저장된 키 입력 사용
            next_key = None  # 다음 키 입력을 None으로 초기화
        pass

        if key != -1:  # 유효한 키가 입력된 경우
            count += 1 # 실행 횟수 증가
        
            curses.halfdelay(3)  # 키가 입력되면 0.3초 대기

            # 방향키 ↑ 또는 ←가 입력된 경우 듀티 사이클 증가
            if key in [curses.KEY_UP, curses.KEY_LEFT]:
                dc += dc_increment
                stdscr.addstr(3, 0, f"[{count:3d}] ↑ : angle increased.")
            # 방향키 ↓ 또는 →가 입력된 경우 듀티 사이클 감소
            elif key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
                dc -= dc_increment
                stdscr.addstr(3, 0, f"[{count:3d}] ↓ : angle decreased.")
            # 'q' 또는 'Q'가 입력되면 루프를 종료 (프로그램 종료)
            elif key in [ord('q'), ord('Q'), curses.KEY_ENTER]:
                stdscr.addstr(3, 0, f"[{count:3d}] q pressed.")
                break
            pass

            # 듀티 사이클이 0에서 12.5 사이에 있도록 제한
            dc = max(0, min(12.5, dc))

            # 화면에 현재 듀티 사이클을 출력
            stdscr.addstr(5, 0, f"[{count:3d}] Duty cycle = {dc:5.2f}")

            # 새로운 듀티 사이클을 PWM에 적용하여 서보 모터 제어
            p.ChangeDutyCycle(dc)
            sleep(duration)  # 듀티 사이클 변경 후 잠시 대기

            next_key = key  # 현재 키 입력을 저장하여 연속적으로 같은 키가 입력되었는지 확인

            # 같은 키가 계속 눌렸는지 확인
            while next_key == key:
                next_key = stdscr.getch()  # 다음 키 입력 대기
            pass
        pass
    pass

    p.stop()  # PWM 신호 중지
    GPIO.cleanup()  # 사용한 GPIO 핀을 기본 상태로 되돌림
pass

if __name__ == "__main__":
    curses.wrapper(main)  # curses 환경에서 프로그램 실행
pass
