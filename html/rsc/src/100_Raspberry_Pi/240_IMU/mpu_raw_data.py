print( "Hello ...", flush=1 )
print( "Initialting MPU6050 ...", flush=1 )

from MPU6050 import init_mpu6050
from time import sleep 

mpu, packet_size, fifo_buffer = init_mpu6050()

print( "Done.\n" )

g = 9.80665 # gravity acceleration (m/s^2)

accel_coeff = g/(2**14)
admp_coeff = accel_coeff*2
gyro_coeff = 250 / 2**15

duration = 0.1
count = 0

while 1 :
    if not mpu.isreadyFIFO(packet_size):
        # Check if FIFO data are ready to use...
        continue
    pass

    sleep( duration )

    count += 1
        
    ### The full range of accelerometer is set to [-2g, +2g]. ###
    ### The transformations in this code are based on this range ###

    # raw acceleration
    accel = mpu.get_acceleration()
    ax = accel.x * accel_coeff
    ay = accel.y * accel_coeff
    az = accel.z * accel_coeff

    # DMP acceleration (less noisy acceleration - based on fusion)
    fifo_buffer = mpu.get_FIFO_bytes(packet_size) # get all the DMP data here
    accel_dmp = mpu.DMP_get_acceleration_int16(fifo_buffer)
    ax_dmp = accel_dmp.x * admp_coeff
    ay_dmp = accel_dmp.y * admp_coeff
    az_dmp = accel_dmp.z * admp_coeff

    # raw gyro (full range: [-250, +250]) (unit: degree / second)
    gyro = mpu.get_rotation()
    gx = gyro.x * gyro_coeff
    gy = gyro.y * gyro_coeff
    gz = gyro.z * gyro_coeff

    print( f'[{count:4d}] IMU Accl ', end="" )
    print( f'  x: {ax/g:9.5f}', end="" )
    print( f', y: {ay/g:9.5f}', end="" )
    print( f', z: {az/g:9.5f} g(m/s2)' ) 

    print( f'[{count:4d}] IMU Admp ', end="" )
    print( f'  x: {ax_dmp/g:9.5f}', end="" )
    print( f', y: {ay_dmp/g:9.5f}', end="" )
    print( f', z: {az_dmp/g:9.5f} g(m/s2)' ) 

    print( f'[{count:4d}] IMU Gyro ', end="" )
    print( f'  x: {gx:9.5f}', end="" )
    print( f', y: {gy:9.5f}', end= "" )
    print( f', z: {gz:9.5f} °/s' )

    print( "-"*66 )

pass

print( "Good bye!" )