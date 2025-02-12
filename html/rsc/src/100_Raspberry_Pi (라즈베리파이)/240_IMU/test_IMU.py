import smbus
import time
import math

# MPU6050 레지스터 주소
MPU6050_ADDR = 0x68  # MPU6050 I2C 주소

# MPU6050 레지스터
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# I2C 버스 설정
bus = smbus.SMBus(1)  # Raspberry Pi에서 I2C bus 1 사용

# MPU6050 초기화
def mpu_init():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # MPU6050 시작

# 레지스터에서 2바이트 읽기 (MPU6050은 데이터가 MSB, LSB로 나뉘어 저장됨)
def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    
    # 음수 값을 처리하기 위해 16비트 데이터를 부호 있는 값으로 변환
    if value > 32768:
        value = value - 65536
    return value

# 가속도 및 자이로 값 읽기
def read_accel_gyro():
    # 가속도 값 읽기
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_XOUT_H + 2)
    acc_z = read_raw_data(ACCEL_XOUT_H + 4)
    
    # 자이로 값 읽기
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_XOUT_H + 2)
    gyro_z = read_raw_data(GYRO_XOUT_H + 4)
    
    # 가속도 값 (단위: g, 1g = 9.8m/s^2)
    Ax = acc_x / 16384.0
    Ay = acc_y / 16384.0
    Az = acc_z / 16384.0
    
    # 자이로 값 (단위: 도/초)
    Gx = gyro_x / 131.0
    Gy = gyro_y / 131.0
    Gz = gyro_z / 131.0
    
    return (Ax, Ay, Az, Gx, Gy, Gz)

# 회전 각도 계산 (자이로 데이터를 이용)
def calculate_rotation(Ax, Ay, Az):
    # 각 축에 대한 회전 각도 계산 (라디안 -> 도)
    roll = math.atan2(Ay, Az) * 180 / math.pi
    pitch = math.atan2(-Ax, math.sqrt(Ay**2 + Az**2)) * 180 / math.pi
    return roll, pitch

# 초기화
mpu_init()

# 데이터 읽기 루프
count = 0 
while 1:
    count += 1
    # 가속도와 자이로 값 읽기
    Ax, Ay, Az, Gx, Gy, Gz = read_accel_gyro()
    
    # 회전 각도 계산
    roll, pitch = calculate_rotation(Ax, Ay, Az)
    
    print(  "-"*40 )
    print( f"Count: {count:d}" )
    print(f"가속도: X={Ax:.2f}g, Y={Ay:.2f}g, Z={Az:.2f}g")
    print(f"각속도: X={Gx:.2f}°/s, Y={Gy:.2f}°/s, Z={Gz:.2f}°/s")
    print(f"회전각: Roll={roll:.2f}°, Pitch={pitch:.2f}°")
    
    # 1초 대기
    time.sleep(1)
pass
