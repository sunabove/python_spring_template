from machine import Pin, I2C
from time import sleep
import ssd1306

# I2C 핀 설정 (Pico 기본 핀: GPIO 4, 5)
i2c = I2C(0, scl=Pin(5), sda=Pin(4))

# OLED 디스플레이 초기화 (128x32 해상도)
w = width = 128
h = height = 32
oled = ssd1306.SSD1306_I2C(width, height, i2c)

duration = 0.7

# 정사각형 크기와 위치 설정
m = margin = 4
ss = square_size = h - 2*m  # 한 변의 길이
x = m
y = m
 
# 화면 지우기
oled.fill(0)

oled.rect(0, 0, w, h, 1)

# 정사각형 그리기
oled.rect(x, y, ss, ss, 1)

# 삼각형의 세 꼭짓점 좌표
x1, y1 = 2*m + ss + ss // 2, m  # 상단 중앙
x2, y2 = x1 - ss//2 , h - m - 1   # 좌하단
x3, y3 = x2 + ss, y2  # 우하단

# 삼각형 선 그리기
oled.line(x1, y1, x2, y2, 1)  # 왼쪽 변
oled.line(x2, y2, x3, y3, 1)  # 밑변
oled.line(x3, y3, x1, y1, 1)  # 오른쪽 변

# 원 그리기 함수
def draw_circle(cx, cy, radius):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if x*x + y*y <= radius*radius:
                oled.pixel(cx + x, cy + y, 1)

# 원 중심과 반지름 설정
radius = ss//2
cx = x3 + radius + 2*m
cy = h // 2 

draw_circle( cx, cy, radius )

# 디스플레이에 출력
oled.show() 
