print( "Hello ...", flush=1 )
print( "Initialting MPU6050 ...", flush=1 )

from MPU6050 import init_mpu6050
from time import sleep 
import time

mpu, packet_size, fifo_buffer = init_mpu6050()

print( "Done.\n" )

g = 9.80665 # gravity acceleration (m/s^2)

accel_coeff = g/(2**14)
admp_coeff = accel_coeff*2
gyro_coeff = 250 / 2**15

then = time.time()

velocity = [0, 0, 0]
position = [0, 0, 0]

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

    now = time.time()
    elapsed = now - then
    then = now

    # raw acceleration
    accel = mpu.get_acceleration()
    accel.x = accel.x * accel_coeff
    accel.y = accel.y * accel_coeff
    accel.z = accel.z * accel_coeff
    
    # quaternion
    q = mpu.DMP_get_quaternion_int16(FIFO_buffer)
    q.normalize()

    # world-frame acceleration vectors (practical for INS)
    accel_linear = mpu.get_linear_accel(accel, q)
    ax = accel_linear.x 
    ay = accel_linear.y 
    az = accel_linear.z

    dt = elapsed

    velocity[0] += ax*dt
    velocity[1] += ay*dt
    velocity[2] += az*dt

    position[0] += velocity[0]*dt
    position[1] += velocity[1]*dt
    position[2] += velocity[2]*dt
    
    print( f'[{count:4d}] World Accel ', end="" )
    print( f'  x: {ax:13.5f}', end="" )
    print( f', y: {ay:13.5f}', end="" )
    print( f', z: {az:13.5f} m/s2' )

    print( f'[{count:4d}] World Veloc ', end="" )
    print( f'  x: {velocity[0]:13.5f}', end="" )
    print( f', y: {velocity[1]:13.5f}', end="" )
    print( f', z: {velocity[2]:13.5f} m/s' )

    print( f'[{count:4d}] World Pos   ', end="" )
    print( f'  x: {position[0]:13.5f}', end="" )
    print( f', y: {position[1]:13.5f}', end="" )
    print( f', z: {position[2]:13.5f} m' )

    print( "-"*74 )

pass