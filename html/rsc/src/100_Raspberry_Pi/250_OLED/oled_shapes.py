from PIL import Image, ImageDraw
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
import math

# I2C 초기화
i2c = busio.I2C(board.SCL, board.SDA)

# OLED 디스플레이 설정 (128x32 해상도, I2C 주소 0x3C)
width = 128
height = 32

oled = SSD1306_I2C(width, height, i2c)

# 디스플레이 초기화
oled.fill(0)
oled.show()

# 이미지 생성
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)

# 도형 크기 및 간격 설정
usable_height = height - 10  # 위/아래 마진 합: 10 (5픽셀씩)
shape_size = 20  # 각 도형의 크기
gap = 12  # 도형 간의 간격
start_x = 8  # 첫 번째 도형의 시작 X 좌표

# 1. 정사각형
square_x1 = start_x
square_x2 = square_x1 + shape_size - 1
draw.rectangle((square_x1, 6, square_x2, 6 + shape_size - 1), outline=255, fill=0)

# 2. 정삼각형
triangle_x1 = square_x2 + gap
triangle_x2 = triangle_x1 + shape_size - 1
triangle_points = [
    (triangle_x1, 6 + shape_size - 1),  # 아래 왼쪽
    (triangle_x2, 6 + shape_size - 1),  # 아래 오른쪽
    ((triangle_x1 + triangle_x2) // 2, 6),  # 위쪽
]
draw.polygon(triangle_points, outline=255, fill=0)

# 3. 원
circle_x1 = triangle_x2 + gap
circle_x2 = circle_x1 + shape_size - 1
draw.ellipse((circle_x1, 6, circle_x2, 6 + shape_size - 1), outline=255, fill=0)

# 4. 별
star_x1 = circle_x2 + gap
star_x2 = star_x1 + shape_size - 1
center_x = (star_x1 + star_x2) // 2
center_y = 6 + shape_size // 2
outer_radius = shape_size // 2
inner_radius = outer_radius // 2

# 별의 5개 꼭짓점과 안쪽 점 계산
star_points = []
for i in range(10):
    angle = math.radians(72 * i)  # 각도 계산 (360 / 5 = 72도)
    radius = outer_radius if i % 2 == 0 else inner_radius
    x = center_x + radius * math.cos(angle - math.pi / 2)
    y = center_y + radius * math.sin(angle - math.pi / 2)
    star_points.append((x, y))

# 별 그리기
draw.polygon(star_points, outline=255, fill=0)

# OLED에 이미지 표시
oled.image(image)
oled.show()
