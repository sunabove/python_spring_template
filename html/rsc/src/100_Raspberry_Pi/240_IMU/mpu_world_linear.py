print( "Hello ...", flush=1 )
print( "Initiating MPU6050 ...", flush=1 )

from MPU6050 import init_mpu6050
from time import sleep 
import math, time
import numpy as np
from scipy.signal import butter, filtfilt

mpu, packet_size, fifo_buffer = init_mpu6050()

print( "Done.\n" )

g = 9.80665 # gravity acceleration (m/s^2)

accel_coeff = g/(2**14)
admp_coeff = accel_coeff*2
gyro_coeff = 250 / 2**15
g_cali_coeff = 1 # 중력 가속도 보정 계수

cali_start = -1
cali_end = -1
cali_duration = 20 # 캘리브레이션 시간
g_cali = 0

then = time.time()

velocity = np.array( [0, 0, 0], float )
position = np.array( [0, 0, 0], float )

duration = 0.01
count = 0

# 캘리브레이션 가속도 데이터 (X, Y, Z 축 가속도)
accel_cali_data = []

# 저주파 필터를 사용하여 중력 성분 추출
def low_pass_filter(data, cutoff=0.1, fs=50, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data, axis=0)
pass

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

    if cali_start < 0 :
        print( f"Calibrating gravity coefficients for {cali_duration} seconds ...." )
        print( "Please place the IMU on a flat, horizontal surface.", flush=1)
        input( "Enter to continue, please ... ")
        cali_start = time.time()
        count = 0 
    elif ( now - cali_start < cali_duration ) or abs(g_cali - g) > 0.001 : # 캘리브레이션
        g_measure = math.sqrt( ax*ax + ay*ay + az*az )

        if len( accel_cali_data ) > 1_000 :
            accel_cali_data.pop( 0 )
        pass
    
        accel_cali_data.append( [ax, ay, az] )

        if len( accel_cali_data ) < 20 :
            count = 0 
            continue 
        pass

        # X, Y, Z 축에 대해 필터 적용
        # 중력 벡터의 크기를 통해 중력 가속도 계산
        
        gravity = low_pass_filter( np.array( accel_cali_data) )
        gravity_magnitude = np.linalg.norm(gravity, axis=1)
        gravity_average = np.mean(gravity_magnitude)

        g_cali_coeff = g/gravity_average
        g_cali = g_measure*(g_cali_coeff)

        print( f"[{count:4d}] {(now - cali_start):4.1f} sec: Gravity:", end="")
        print( f" avg = {gravity_average:6.3f}", end="")
        print( f", measure = {g_measure:6.3f}", end="")
        print( f", cali = {g_cali:6.3f} m/s2", end="" )
        print()
    elif cali_start > 0 and cali_end < 0 :
        count = 0 
        cali_end = time.time()
        print( "Success calibrating IMU.")
        print()
        input( "Enter to continue, please ... ")
    pass

    if cali_end < 0 :
        continue
    pass

    dt = elapsed

    accel = np.array( [ax, ay, az], float )
    
    # accelation calibrqation
    accel_cali = accel*g_cali_coeff
    accel_cali[2] -= g # 중력 가속도 감쇠

    velocity += accel_cali*dt 
    position += velocity*dt
    
    print( f'[{count:4d}] World Gravity     ', end="" )
    print( f'  x: {ax:13.5f}', end="" )
    print( f', y: {ay:13.5f}', end="" )
    print( f', z: {az:13.5f} m/s2' )

    print( f'[{count:4d}] World G calibrated', end="" )
    print( f'  x: {accel[0]*g_cali_coeff:13.5f}', end="" )
    print( f', y: {accel[1]*g_cali_coeff:13.5f}', end="" )
    print( f', z: {accel[2]*g_cali_coeff:13.5f} m/s2' )

    print( f'[{count:4d}] World Accelration ', end="" )
    print( f'  x: {accel_cali[0]:13.5f}', end="" )
    print( f', y: {accel_cali[1]:13.5f}', end="" )
    print( f', z: {accel_cali[2]:13.5f} m/s2' )

    print( f'[{count:4d}] World Velocity    ', end="" )
    print( f'  x: {velocity[0]:13.5f}', end="" )
    print( f', y: {velocity[1]:13.5f}', end="" )
    print( f', z: {velocity[2]:13.5f} m/s' )

    print( f'[{count:4d}] World Position    ', end="" )
    print( f'  x: {position[0]:13.5f}', end="" )
    print( f', y: {position[1]:13.5f}', end="" )
    print( f', z: {position[2]:13.5f} m' )

    print( "-"*86 )

pass