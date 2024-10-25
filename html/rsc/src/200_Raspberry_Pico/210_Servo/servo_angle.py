from picozero import Servo  # picozero 라이브러리에서 Servo 클래스 임포트
from time import sleep  # time 라이브러리에서 sleep 함수 임포트

# 프로그램 시작 메시지
print("Hello ...\n")

# 핀 1에 연결된 서보 객체 생성 및 초기값 설정
servo = Servo(1)
servo.value = 0  # 서보 위치를 0으로 설정 (최소 각도)
sleep(0.5)  # 0.5초 대기

# 서보 위치를 점진적으로 0에서 1까지 증가시키는 루프
for i in range(0, 101, 5):  # 0부터 100까지 5씩 증가
    servo.value = i / 100  # 서보 위치를 0.0에서 1.0까지 설정
    print(f"[{i//5:2d}] servo.value = {servo.value:4.2f}")  # 현재 서보 위치 출력
    sleep(0.25)  # 0.25초 대기
pass

# 서보 모터 종료
servo.off()  # 서보 모터의 PWM 신호를 종료
servo.close()  # PWM을 해제하여 핀 초기화

# 프로그램 종료 메시지
print("\nGood bye!")