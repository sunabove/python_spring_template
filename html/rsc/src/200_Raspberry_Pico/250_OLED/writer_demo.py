from machine import Pin, I2C
from writer import Writer
import ssd1306

# Font
import freesans20

# OLED 디스플레이 설정 (128x32 해상도)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
w = width = 128
h = height = 32
ssd = ssd1306.SSD1306_I2C( w, h, i2c)

wri = Writer(ssd, freesans20)
#Writer.set_textpos(ssd)
wri.printstring('Sunday\n')
#wri.printstring('12 Aug 2018\n')
wri.printstring('10.30am')
ssd.show()
