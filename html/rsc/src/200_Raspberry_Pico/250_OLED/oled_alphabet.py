from machine import Pin, I2C
import ssd1306
import time
import consolas_font as font

# I2C 설정 (SDA=GP4, SCL=GP5)
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Initialize font
font.load_font("consolas_font.py")

# Clear screen
oled.fill(0)

# Display text
oled.text('Hello, Pico!', 0, 0)

# Show on display
oled.show()
