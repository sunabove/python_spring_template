from machine import Pin, I2C
from time import sleep
from oled_writer import Writer

import ssd1306
import oled_freesans20 as font 

# OLED 디스플레이 설정 (128x32 해상도)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
w = width = 128
h = height = 32
oled = ssd1306.SSD1306_I2C(w, h, i2c)
writer = Writer(oled, font, verbose=0)

# 화면 중간에 출력하기 위해 위치 계산
fw = font_width = writer.font.max_width()  # 폰트의 최대 글자 너비
fh = font_height = writer.font.height()   # 폰트 높이

text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijiklmnopqrstuvwxyz0123456789"
text_width = len(text) * font_width

x = 10
y = (h - fh) // 2 + 2  # 화면 가운데 행 계산
duration = 0.03

idx = 0 
while 1 :
    oled.fill(0)
    
    writer.print(text, x=x, y=y)
    
    oled.rect(0, 0, w, h, 1)
    oled.show()
    
    sleep( duration )
    
    idx += 1
    
    x = x - 5 if x > -text_width*0.6 else 10
pass
