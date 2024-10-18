import smbus
import math
import time

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a*a) + (b*b))

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians) 

bus = smbus.SMBus(1)
address = 0x68

bus.write_byte_data(address, power_mgmt_1, 0)

count = 0 
while 1 :
    count += 1 
    print( f"Count: {count:d}" )
    print( f"Gyroscope data" )
    print(  "-"*14 )

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    gyro_xout_scaled = gyro_xout/131
    gyro_yout_scaled = gyro_yout/131
    gyro_zout_scaled = gyro_zout/131

    print( f"X out: \t {gyro_xout} \t scaled: \t {gyro_xout_scaled}" )
    print( f"Y out: \t {gyro_yout} \t scaled: \t {gyro_yout_scaled}" )
    print( f"Z out: \t {gyro_zout} \t scaled: \t {gyro_zout_scaled}" )

    print()
    print( "Accelerometer data" )
    print(  "-"*14 )

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print( f"X accel out: \t {accel_xout} \t scaled: \t {accel_xout_scaled}" )
    print( f"Y accel out: \t {accel_yout} \t scaled: \t {accel_yout_scaled}" )
    print( f"Z accel out: \t {accel_zout} \t scaled: \t {accel_zout_scaled}" ) 
	
    print()

    print(  "-"*14 )
    
    x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) 

    print( f"X rotation: \t {x_rotation}" )
    print( f"Y rotation: \t {y_rotation}" ) 
    
    print()

    time.sleep(1)
pass