# servo_cali.py
# 서보 암을 중앙 방향으로 부착합니다.

from picozero import Servo  # picozero 라이브러리에서 Servo 클래스 임포트
from time import sleep  # time 라이브러리에서 sleep 함수 임포트

# 핀 1에 연결된 서보 객체 생성
servo = Servo(1)

# 각 위치에서 대기할 시간 (초)
duration = 1

print("Start calibrating ...\n")  # 캘리브레이션 시작 메시지 출력

count = 0  # 카운트 초기화
for _ in range(3):  # 3회 반복하여 서보 이동
    count += 1 # 카운트 증가
    print(f"[{count:2d}] Locating servo min angle ...")  # 최소 각도로 이동 메시지
    servo.min()  # 서보를 최소 각도로 이동
    sleep(duration)  # duration 동안 대기
    print(f"[{count:2d}] Servo value = {servo.value:4.1f}")  # 현재 각도 출력

    count += 1 # 카운트 증가
    print(f"[{count:2d}] Locating servo middle angle ...")  # 중간 각도로 이동 메시지
    servo.mid()  # 서보를 중간(90도) 각도로 이동
    sleep(duration)  # duration 동안 대기
    print(f"[{count:2d}] Servo value = {servo.value:4.1f}")  # 현재 각도 출력

    count += 1 # 카운트 증가
    print(f"[{count:2d}] Locating servo max angle ...")  # 최대 각도로 이동 메시지
    servo.max()  # 서보를 최대 각도로 이동
    sleep(duration)  # duration 동안 대기
    print(f"[{count:2d}] Servo value = {servo.value:4.1f}")  # 현재 각도 출력

    count += 1 # 카운트 증가
    print(f"[{count:2d}] Locating servo middle angle ...")  # 중간 각도로 복귀 메시지
    servo.mid()  # 서보를 중간(90도) 각도로 이동
    sleep(duration)  # duration 동안 대기
    print(f"[{count:2d}] Servo value = {servo.value:4.1f}")  # 현재 각도 출력
pass

# 서보 암을 중앙에 부착할 수 있도록 사용자에게 안내
print("\nAttach the servo arm at 90 degree for 20 seconds!")
sleep(20)  # 20초 대기

# 서보 모터 종료
servo.off()  # 서보 모터의 PWM 신호를 종료
servo.close()  # PWM을 해제하고 핀 초기화

print("\nGood bye!")  # 프로그램 종료 메시지 출력
