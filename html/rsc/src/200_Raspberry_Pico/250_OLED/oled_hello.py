from machine import Pin, I2C
from time import sleep
import os
import ssd1306

# I2C 핀 설정 (Pico의 GP4 = SDA, GP5 = SCL)

# OLED 디스플레이 설정 (128x32 해상도)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
oled = ssd1306.SSD1306_I2C( 128, 32, i2c)

# 화면 초기화 및 텍스트 출력
oled.fill(0)
oled.text("Hello, World!", 0, 0)  # 첫 번째 줄에 "Hello, World!" 출력
oled.text(f"{os.uname().machine}", 0, 12)  # 두 번째 줄에 머신 정보 출력 (e.g., 'Raspberry Pi Pico with RP2040')
oled.text(f"V {os.uname().release}", 0, 24)  # 세 번째 줄에 MicroPython 펌웨어 버전 출력 (e.g., '1.19.1')
oled.show()

sleep(5)

# 텍스트 이동 효과
for x in range(width):
    oled.fill(0)
    # 텍스트를 오른쪽에서 왼쪽으로 이동하며 출력
    oled.text( "Hello, World!", width - x - 1, 16)  
    oled.show()
    sleep(0.05)
pass

# 마지막 텍스트 출력
oled.fill(0)
# 마지막으로 "Goodbye!"를 가운데 높이(12)에 출력
oled.text("Hello, World!", 15, 16)
oled.show()
