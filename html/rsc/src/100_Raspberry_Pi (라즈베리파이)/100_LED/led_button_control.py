# gpiozero 패키지의 LED와 Button 클래스를 임포트합니다.
from gpiozero import LED, Button

# GPIO 17번 핀에 연결된 LED 객체를 생성합니다.
led = LED(17)
# GPIO 2번 핀에 연결된 버튼 객체를 생성합니다.
button = Button(2)

# 버튼이 눌렸을 때, 
# LED를 켜는 led.on 함수를 실행합니다.
button.when_pressed = led.on
# 버튼이 떼어졌을 때, 
# LED를 끄는 led.off 함수를 실행합니다.
button.when_released = led.off

# 사용자가 Enter 키를 누를 때까지 
# 프로그램을 종료하지 않고 대기합니다.
input("ENTER to quit! ")
