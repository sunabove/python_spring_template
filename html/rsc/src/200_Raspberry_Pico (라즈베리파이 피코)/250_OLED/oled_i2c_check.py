# oled_i2c_check.py

from machine import Pin, I2C

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
print("I2C Address:", [hex(addr) for addr in i2c.scan()])
