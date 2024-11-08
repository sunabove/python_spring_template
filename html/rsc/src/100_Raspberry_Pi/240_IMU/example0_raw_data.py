from MPU6050 import MPU6050
from time import sleep

i2c_bus = 1
device_address = 0x68
freq_divider = 0x01

### DMP output frequency is calculated easily using this equation: (200Hz / (1 + value))
### For example, 0x04 gives (200Hz / (1 + 4)) = 40HZ
### I propose 0x04 for a less noisy quaternion and 0x01 for accelerometer & gyrometer.

# Make an MPU6050
mpu = MPU6050(i2c_bus, device_address, freq_divider)

# Initiate your DMP
mpu.dmp_initialize()
mpu.set_DMP_enabled(True)

packet_size = mpu.DMP_get_FIFO_packet_size()
FIFO_buffer = [0]*64

g = 9.8 # gravity acceleration (m/s^2)
a_coeff = g/(2**14)
b_coeff = a_coeff*2
c_coeff = 250 / 2**15

duration = 0.1

count = 0 
while 1 : 
    sleep( duration )

    if not mpu.isreadyFIFO(packet_size): 
        # Check if FIFO data are ready to use...
        continue
    pass

    count += 1
        
    FIFO_buffer = mpu.get_FIFO_bytes(packet_size) # get all the DMP data here

    ### The full range of accelerometer is set to [-2g, +2g]. ###
    ### The transformations in this code are based on this range ###

    # raw acceleration
    accel = mpu.get_acceleration()
    Ax = accel.x * a_coeff
    Ay = accel.y * a_coeff
    Az = accel.z * a_coeff

    # DMP acceleration (less noisy acceleration - based on fusion)
    accel_dmp = mpu.DMP_get_acceleration_int16(FIFO_buffer)
    Ax_dmp = accel_dmp.x * b_coeff
    Ay_dmp = accel_dmp.y * b_coeff
    Az_dmp = accel_dmp.z * b_coeff

    # raw gyro (full range: [-250, +250]) (unit: degree / second)
    gyro = mpu.get_rotation()
    Gx = gyro.x * c_coeff
    Gy = gyro.y * c_coeff
    Gz = gyro.z * c_coeff

    print( f'[{count:4d}] Ax: {Ax:8.5f}, {Ax_dmp:8.5f} m/s2' )
    print( f'[{count:4d}] Ay: {Ay:8.5f}, {Ay_dmp:8.5f} m/s2' )
    print( f'[{count:4d}] Az: {Az:8.5f}, {Az_dmp:8.5f} m/s2' ) 

    print( f'[{count:4d}] Gx: {Gx:8.5f} °/s' )
    print( f'[{count:4d}] Gy: {Gy:8.5f} °/s' )
    print( f'[{count:4d}] Gz: {Gz:8.5f} °/s' )

    print( "-"*40 )

pass