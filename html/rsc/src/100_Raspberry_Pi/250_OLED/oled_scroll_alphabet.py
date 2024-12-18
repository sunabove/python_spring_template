import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont
import time

# I2C 설정
i2c = busio.I2C(board.SCL, board.SDA)

# 디스플레이 초기화
oled = SSD1306_I2C(128, 64, i2c)

# 폰트 설정 (Pillow에서 제공하는 TrueType 폰트 사용)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 48)

# 텍스트 설정 (A-Z, 0-9)
text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# 이미지 생성하여 텍스트 크기 계산
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# 텍스트의 경계박스를 얻어 텍스트 크기 계산
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# 스크롤 시작 위치 설정
scroll_x = oled.width/10  # 화면 오른쪽에서 시작

# 스크롤 루프
duration = 0.1
scroll_x_amount = oled.width//20
while True:
    # 새 화면 생성
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # 텍스트 그리기 (스크롤 X 좌표에 따라 위치 지정)
    draw.text((scroll_x, (oled.height - text_height) // 2), text, font=font, fill=255)

    # 화면에 이미지 출력
    oled.image(image)
    oled.show()

    # 스크롤 이동 (왼쪽으로 이동)
    scroll_x -= scroll_x_amount  # 스크롤 속도 조정

    # 텍스트가 화면을 벗어나면 다시 오른쪽으로 되돌리기
    if scroll_x < -text_width:
        scroll_x = oled.width

    # 잠시 기다리기 (스크롤 속도 조정)
    time.sleep( duration )
pass
