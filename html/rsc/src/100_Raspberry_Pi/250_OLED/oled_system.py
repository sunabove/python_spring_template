import os, datetime, psutil, shutil 
import board, busio
from adafruit_ssd1306 import SSD1306_I2C
from time import sleep 

from PIL import Image, ImageOps, ImageDraw, ImageFont

oled_alive = True 

# I2C 설정
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_path = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
font = ImageFont.truetype( font_path, 30)

def display_oled_info( draw, image, idx = 0 ) :
    idx = idx % 6

    text = ""

    if idx < 0 : # shutdown
        text = "SHUTDOWN"
    elif idx == 0 : # current time
        text = datetime.datetime.now().strftime("%p %H:%M:%S")
    elif idx == 1 : # hostname
        hostname = os.popen("hostname").read().strip().split()[0]

        text = f"{hostname}"
    elif idx == 2 : # ip address
        ipaddr = os.popen("hostname -I").read().strip().split()[-1]

        text = f"{ipaddr}"
    elif idx == 3 : # disk usage
        # Disk usage

        total, used, free = shutil.disk_usage("/")
        total //= (2**30)
        used //= (2**30)
        free //= (2**30)
        pct = used*100/total

        text = f"Disk:{pct:02.1f}%"
    elif idx == 4 : # CPU
        pct = psutil.cpu_percent()

        text = f"CPU:{pct:02.1f}%"
    elif idx == 5 : # RAM
        pct = psutil.virtual_memory()[2] 

        text = f"RAM:{pct:02.1f}%" 
    pass

    print( f"text = {text}")

    if text : 
        w, h = image.size 

        text_bbox = draw.textbbox((0, 0), text, font=font)  # 텍스트 경계 사각형 계산
        tw = text_width = text_bbox[2] - text_bbox[0]
        th = text_height = text_bbox[3] - text_bbox[1]

        # text center align
        x = (w - tw)//2
        y = (h - th)//2
        
        draw.rectangle( [0, 0, w -1, h -1], fill=0, outline = 0)
        draw.text( [x, y], text, font = font, fill = 255) 
        
        oled.image( image )
        oled.show() 
    pass

    sleep(2.5)

    if idx >= 0 : 
        print ("Turn off screen to prevent heating oled.")
        oled.fill(0)  # 화면을 검은색(0)으로 채움
        oled.show()   # 변경 사항 디스플레이에 반영
    pass

    sleep(1)
pass

pass # -- stop

def service() :
    try:
        global oled_alive

        oled_alive = 1

        # Create blank image for drawing.
        image = Image.new('1', [oled.width, oled.height], "WHITE")
        draw = ImageDraw.Draw(image) 

        idx = 0
        while oled_alive :
            display_oled_info(draw, image, idx) 
            idx += 1

            idx %= 1000
        pass

        stop()

    except IOError as e:
        print(e)    
    except KeyboardInterrupt:
        print("ctrl + c:") 
    pass
pass  # -- service

if __name__ == '__main__':
    service()
pass