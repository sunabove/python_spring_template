# gpiozero 패키지에서 TonalBuzzer 클래스를 임포트하여 톤을 생성할 수 있는 부저 제어
from gpiozero import TonalBuzzer
# time 모듈에서 sleep 함수를 임포트하여 시간 지연 사용
from time import sleep

# TonalBuzzer 객체 생성, GPIO 4번 핀에 연결된 부저를 제어
buzzer = TonalBuzzer(4)

# 옥타브 범위를 설정하여 반복 (3옥타브에서 5옥타브까지)
for octave in range(3, 6):
    # 도레미파솔라시 (ABCDEFG) 음계 순서대로 실행
    for scale in "ABCDEFG":
        try:
            # 현재 음계를 나타내는 문자열을 생성 (예: C4, D4, 등)
            tone = f"{scale}{octave}"
            # 부저에서 해당 음계의 톤을 재생
            buzzer.play(tone)
            # 재생 중인 음계를 콘솔에 출력
            print("Tone =", tone)
            # 1초 동안 톤을 유지
            sleep(1)
        except:
            # 예외 발생 시 패스 (예: 잘못된 음계가 있을 경우)
            pass
        pass
    pass
pass