# oled_hello.py
import board, busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# I2C 설정
i2c = busio.I2C(board.SCL, board.SDA)

# 디스플레이 초기화
oled = SSD1306_I2C(128, 64, i2c)

# 화면 지우기
oled.fill(0)
oled.show()

# 이미지 생성
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
w, h = image.size

# 폰트 설정 (Pillow에서 제공하는 TrueType 폰트 사용)
# 시스템 폰트 경로 확인 후 적절한 폰트 파일 경로로 변경
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_path = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
font = ImageFont.truetype(font_path, 48)

# 텍스트와 크기 설정
text = "Hello"
text_bbox = draw.textbbox((0, 0), text, font=font)  # 텍스트 경계 사각형 계산
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# 텍스트 중앙 정렬
text_x = (w - text_width) // 2
text_y = (h - text_height) // 2

# 사각형 그리기
draw.rectangle( [0, 0, w -1, h -1], fill=0, outline = 0)
draw.rectangle( [0, 1, w -1, h -1], fill=0, outline = 1)
# 텍스트 그리기
draw.text((text_x, text_y), text, font=font, fill=255)

# 디스플레이에 이미지 출력
oled.image(image)
oled.show()
