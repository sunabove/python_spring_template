import os
import gc
import time
from machine import Pin, I2C, ADC, RTC, freq
import ssd1306
import oled_freesans20 as font
from oled_writer import Writer

# OLED 디스플레이 설정
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
w = width = 128
h = height = 32
oled = ssd1306.SSD1306_I2C(w, h, i2c)

# Writer 객체 초기화
writer = Writer(oled, font, verbose=False)

# 온도 센서 설정
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

# RTC 설정
rtc = RTC()

# RTC 초기화 (필요 시 사용자 정의)
rtc.datetime((2025, 1, 1, 0, 12, 30, 0, 0))  # (년도, 월, 일, 요일, 시, 분, 초, 밀리초)

def display_info(writer, idx=0):
    """Pico 시스템 정보를 OLED에 출력."""
    idx = idx % 5  # 5가지 정보를 순환 출력
    text = ""

    if idx == 0:  # 현재 시각
        datetime = rtc.datetime()
        text = f"{datetime[4]:02}:{datetime[5]:02}:{datetime[6]:02}"
    elif idx == 1:  # CPU 클럭
        text = f"CPU {freq()//1_000_000:.0f}Mhz" 
    elif idx == 2:  # 메모리 상태 
        gc.collect()
        free_mem = gc.mem_free()/(gc.mem_free() + gc.mem_alloc())*100
        text = f"Mem : {free_mem:.1f}%"
    elif idx == 3:  # 플래시 스토리지 상태
        statvfs = os.statvfs('/')
        total = statvfs[2] * statvfs[1]  # 전체 크기
        free = statvfs[3] * statvfs[1]   # 사용 가능한 크기
        used_pct = (1 - free / total) * 100
        text = f"Disk : {used_pct:4.1f}%"
    elif idx == 4:  # 온도 
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        text = f"Temp : {temperature:.1f} C"
    pass

    print(f"[{idx}] Text = {text}")

    # OLED에 출력
    oled.fill(0)
    text_width = writer.stringlen(text)
    x = (w - text_width) // 2  # 가로 중앙
    y = (h - writer.font.height()) // 2 + 2 # 세로 중앙
    writer.print(text, x=x, y=y) 
    oled.rect(0, 0, w, h, 1)
    oled.show()
pass 

if __name__ == "__main__":
    """시스템 정보 순환 출력."""
    idx = 0
    while True:
        display_info(writer, idx)
        idx += 1
        time.sleep( 3 )  # 출력 유지 시간
    pass
pass
