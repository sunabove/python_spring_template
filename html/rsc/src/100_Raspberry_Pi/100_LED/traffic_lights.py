from gpiozero import TrafficLights, Button
from time import sleep, time

# 버튼과 신호등 초기화
button = Button(21)              # GPIO 핀 21에 연결된 버튼을 설정
tr = TrafficLights(23, 24, 25)   # GPIO 핀 23, 24, 25에 각각 초록, 노랑, 빨강 신호등을 설정

# 신호등 및 관련 타이밍 설정
lights = [tr.green, tr.amber, tr.red]  # 초록, 노랑, 빨강 순서의 신호등 리스트
durations = [5, 3, 10]   # 각 신호등이 켜져 있을 시간 (초)
periods = [0, 1/3, 1/4]  # 각 신호등의 깜빡임 주기 (초)

light_no = 0   # 현재 신호등 인덱스
signal_no = 0  # 신호 변경 카운터

# 신호를 변경하는 함수
def change_signal():
    global light_no, signal_no
    signal_no += 1  # 신호 변경 카운터 증가
    light_no += 1   # 다음 신호등으로 이동
pass

# 버튼이 눌렸을 때 change_signal 함수가 실행되도록 설정
button.when_pressed = change_signal

# 무한 루프 시작
while True:
   # 모든 신호등을 꺼둠
   for light in lights:
      light.off()

   # 신호등 인덱스가 리스트 범위를 넘지 않도록 조정
   light_no = light_no % len(lights)  
   curr_signal_no = signal_no         # 현재 신호 번호 저장

   light = lights[light_no]           # 현재 켜야 할 신호등 선택
   duration = durations[light_no]     # 현재 신호등이 켜질 시간 설정
   period = periods[light_no]         # 현재 신호등의 깜빡임 주기 설정

   start_time = time()  # 신호등 시작 시간을 기록
   elapsed = 0          # 경과 시간 초기화

   # 현재 신호가 유효하고, 경과 시간이 지정된 시간을 넘지 않을 때까지 신호등 깜빡임
   while curr_signal_no == signal_no and elapsed < duration:
      if period > 0:
         # 깜빡임 주기에 따라 신호등 켜기/끄기 결정
         if int(elapsed / period) % 2:
               light.off()  # 주기적으로 꺼짐
         else:
               light.on()   # 주기적으로 켜짐
         pass
      else:
         light.on()  # 깜빡임 주기가 없을 경우, 계속 켜짐
      pass

      sleep(0.2)  # 짧은 지연 시간 설정
      elapsed = time() - start_time  # 경과 시간 업데이트
   pass

   # 신호 번호가 변경되지 않았으면 다음 신호등으로 이동
   if curr_signal_no == signal_no:
      light_no += 1
   pass
pass
