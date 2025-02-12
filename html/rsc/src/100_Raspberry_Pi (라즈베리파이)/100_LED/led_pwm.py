from gpiozero import PWMLED
from time import sleep

# PWM 제어 LED 생성
led = PWMLED(17)

while 1 : # 무한 반복
   
   # 0 부터 100까지 반복
   for x in range( 101 ) :
      # LED의 전압 비율 설정
      led.value = x/100
      # 0.02초 정지
      sleep( 0.02 )
   pass

pass
