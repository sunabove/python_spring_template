# oled_system_info.py

import os, datetime, psutil, shutil 
import board, busio
from adafruit_ssd1306 import SSD1306_I2C
from time import sleep 

from PIL import Image, ImageOps, ImageDraw, ImageFont

# I2C 설정
i2c = busio.I2C(board.SCL, board.SDA)
w = width = 128
h = height = 32

oled = SSD1306_I2C(width, height, i2c)

# Create blank image for drawing.
image = Image.new('1', [oled.width, oled.height], "WHITE")
draw = ImageDraw.Draw(image)

font_path = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
font = ImageFont.truetype( font_path, 18 )

def disp_text_scroll( text ) :
    text_bbox = draw.textbbox((0, 0), text, font=font)  # 텍스트 경계 사각형 계산
    tw = text_width = text_bbox[2] - text_bbox[0]
    th = text_height = text_bbox[3] - text_bbox[1]
    spacing = 8 

    if tw < w*0.9 :
        # text center align
        x = (w - tw)/2
        y = (h - th)/2

        draw.rectangle( [0, 0, w -1, h -1], fill=0, outline = 0)
        draw.rectangle( [0, 1, w -1, h -1], fill=0, outline = 1)
        draw.text( [ int(x), int(y) ], text, font = font, fill = 255, spacing=spacing)
        
        oled.image( image )
        oled.show()
    else :
        x = w/4
        y = (h - th)/2
        scroll_x = w/30
        duration = 0.01
        while x >= - tw - 2 :
            draw.rectangle( [0, 0, w -1, h -1], fill=0, outline = 0)
            draw.rectangle( [0, 1, w -1, h -1], fill=0, outline = 1)
            draw.text( [ int(x), int(y) ], text, font = font, fill = 255, spacing=spacing) 
            
            oled.image( image )
            oled.show()

            x -= scroll_x

            sleep( duration )
        pass
    pass
pass

def display_system_info( idx = 0 ) :
    idx = idx % 7

    text = ""

    if idx == 0 : # shutdown
        text = "Hello"
    elif idx == 1 : # current time
        text = datetime.datetime.now().strftime("%H:%M:%S") 
    elif idx == 2 : # hostname
        hostname = os.popen("hostname").read().strip().split()[0]
        text = f"host : {hostname}"
    elif idx == 3 : # ip address
        ipaddr = os.popen("hostname -I").read().strip().split()[-1]
        text = f"IP : {ipaddr}"
    elif idx == 4 : # disk usage
        total, used, free = shutil.disk_usage("/")
        total //= (2**30)
        used //= (2**30)
        free //= (2**30)
        pct = used*100/total

        text = f"Disk : {pct:02.1f} %"
    elif idx == 5 : # CPU
        pct = psutil.cpu_percent()

        text = f"CPU : {pct:02.1f} %"
    elif idx == 6 : # RAM
        pct = psutil.virtual_memory()[2] 

        text = f"RAM : {pct:02.1f} %" 
    pass

    print( f"[{idx}] Text = {text}")

    disp_text_scroll( text )

    sleep(2.5)
pass

def main() :
    try:
        idx = 0
        while 1 :
            display_system_info( idx) 
            idx += 1

            idx %= 1000
        pass

    except KeyboardInterrupt :
        print("ctrl + c:") 
    pass
pass

if __name__ == '__main__':
    main()
pass