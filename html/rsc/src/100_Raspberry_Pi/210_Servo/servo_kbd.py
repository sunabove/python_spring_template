# servo_pwm.py

# GPIO 핀 17을 사용하여 PWM 신호를 생성합니다. 

import curses
import RPi.GPIO as GPIO  # 표준 Raspberry Pi GPIO 라이브러리 임포트
from time import sleep   # 프로그램에 대기(일시 정지) 기능 추가



def main(stdscr): 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)   # 핀 번호 체계를 BCM 모드로 설정

    GPIO.setup(17, GPIO.OUT)  # 핀 17을 출력으로 설정

    duration = 0.5
    frequency = 50 # 주파수
    dc = 0 
    dc_increment = 2.5/4

    p = GPIO.PWM(17, frequency)      # 핀 17을 PWM 핀으로 설정하고 주파수를 50Hz로 설정
    p.start(0)                # PWM 시작, 듀티 사이클을 0으로 설정
    sleep( duration )
    p.ChangeDutyCycle( dc )
    sleep( duration )

    stdscr.addstr( 0, 0, "Enter q to quit!")
    stdscr.addstr( 1, 0, "Use ← ↑ → ↓ key to control servo!" ) 
    stdscr.addstr( 2, 0, "" ) 
    stdscr.addstr( 3, 0, f"Duty cycle = {dc:5.2f}")

    next_key = None

    while 1 :
        curses.halfdelay(1)

        if next_key is None:
            key = stdscr.getch()
        else:
            key = next_key
            next_key = None
        pass

        if key != -1:
            # KEY DOWN
            curses.halfdelay(3)

            if key in [ curses.KEY_UP, curses.KEY_LEFT ] :
                dc += dc_increment
            elif key in [ curses.KEY_DOWN, curses.KEY_RIGHT ] : 
                dc -= dc_increment
            elif key in [ ord('q'), ord('Q'), curses.KEY_ENTER ] : 
                break
            pass

            dc = max( 0, min( 12.5, dc ) )

            stdscr.addstr( 3, 0, f"Duty cycle = {dc:5.2f}")

            p.ChangeDutyCycle( dc )
            sleep( duration )

            next_key = key

            while next_key == key:
                next_key = stdscr.getch()
            pass
        pass
    pass

    p.stop()        # PWM을 중지
    GPIO.cleanup()  # GPIO 핀을 기본값으로 재설정
pass



if __name__ == "__main__" :
    curses.wrapper(main)
pass

