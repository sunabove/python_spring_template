# oled_hello.py

import board, busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# I2C 설정
i2c = busio.I2C(board.SCL, board.SDA)

# 디스플레이 초기화
w = width = 128
h = height = 32

oled = SSD1306_I2C(width, height, i2c)

# 이미지 생성
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# 화면 지우기
oled.fill(0)
oled.show()
