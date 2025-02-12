from machine import Pin, I2C
from time import sleep
import os, ssd1306

# I2C 핀 설정 (Pico의 GP4 = SDA, GP5 = SCL)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
# OLED 디스플레이 설정 (128x32 해상도)
oled = ssd1306.SSD1306_I2C( 128, 32, i2c)

# 화면 초기화 및 텍스트 출력
oled.fill(0)
oled.text("Hello, World!", 0, 0)  # "Hello, World!" 출력
oled.text(f"{os.uname().machine}", 0, 12)  # 머신 정보 출력 
oled.text(f"V {os.uname().release}", 0, 24)  # 펌웨어 버전 출력
oled.show()

sleep(3)

# 텍스트 이동 효과
for x in range(oled.width):
    oled.fill(0)
    # 텍스트를 오른쪽에서 왼쪽으로 이동하며 출력
    oled.text( "Hello, World!", oled.width - x - 1, oled.height//2)  
    oled.show()
    sleep(0.05)
pass

# 마지막 텍스트 출력
oled.fill(0)
oled.text("Hello, World!", 15, 16)
oled.show()