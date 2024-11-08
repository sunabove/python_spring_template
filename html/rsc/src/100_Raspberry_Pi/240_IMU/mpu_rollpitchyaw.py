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

    FIFO_buffer = mpu.get_FIFO_bytes(packet_size)
    
    q = mpu.DMP_get_quaternion_int16(FIFO_buffer)
    grav = mpu.DMP_get_gravity(q)
    roll_pitch_yaw = mpu.DMP_get_euler_roll_pitch_yaw(q)
    
    print( f'[{count:4d}] ', end="" )
    print( f'roll: {roll_pitch_yaw.x:9.5f} °', end="" )
    print( f', pitch: {roll_pitch_yaw.y:9.5f} °', end="" )
    print( f', yaw: {roll_pitch_yaw.z:9.5f} ° (degree)' )
    print( "-"*72 )

pass