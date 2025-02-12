import smbus, time
from math import degrees
import matplotlib.pyplot as plt
import matplotlib.animation as animation

bus = smbus.SMBus(1)  # MPU-6050 초기 설정
address = 0x68        # MPU-6050 I2C 주소

# 레지스터 정의
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# 센서 활성화
bus.write_byte_data(address, PWR_MGMT_1, 0)

# 데이터 읽기 함수
def read_word(reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg+1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    pass

    return value
pass

def read_accel():
    x = read_word(ACCEL_XOUT_H) / 16384.0
    y = read_word(ACCEL_YOUT_H) / 16384.0
    z = read_word(ACCEL_ZOUT_H) / 16384.0

    return (x, y, z)
pass

def read_gyro():
    x = read_word(GYRO_XOUT_H) / 131.0
    y = read_word(GYRO_YOUT_H) / 131.0
    z = read_word(GYRO_ZOUT_H) / 131.0

    return (x, y, z)
pass

# 각도 계산 함수
def calculate_angles(gyro, dt, last_angles):
    
    roll_x  = last_angles[0] + gyro[0] * dt
    pitch_y = last_angles[1] + gyro[1] * dt
    yaw_z   = last_angles[2] + gyro[2] * dt

    return (pitch_y, roll_x, yaw_z)
pass

# 위치 계산 함수 (이중 적분)
def calculate_position(accel, velocity, position, dt):
    ax, ay, az = accel
    vx, vy, vz = velocity
    px, py, pz = position

    # 속도 계산 (가속도의 1차 적분)
    vx += ax * dt
    vy += ay * dt
    vz += az * dt

    # 위치 계산 (속도의 1차 적분)
    px += vx * dt
    py += vy * dt
    pz += vz * dt

    return (vx, vy, vz), (px, py, pz)
pass

# 그래프 초기화
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
pitch_data, roll_data, yaw_data = [], [], []
x_data, y_data, z_data = [], [], []

time_data = []

last_angles = (0.0, 0.0, 0.0)
angle_data = []

last_velocity = (0.0, 0.0, 0.0)
last_position = (0.0, 0.0, 0.0)
xyz_data = []

last_time = time.time()

# 위치 데이터
plot_x, = ax1.plot(time_data, x_data, "gp-", label="X (9.8 m)" )
plot_y, = ax1.plot(time_data, y_data, "r*--", label="Y (9.8 m)" )
plot_z, = ax1.plot(time_data, z_data, "bs:", label="Z (9.8 m)" )

ax1.set_ylabel("Position (9.8 m)")
ax1.set_xlabel("Time (s)")
ax1.legend(loc="upper left")
ax1.set_title("Estimated Position - X, Y, Z (Without Calibration)")

# Roll, Pitch, Yaw 데이터
plot_pitch, = ax2.plot(time_data, pitch_data, "gp-", label="Pitch: Y (°)" )
plot_roll, = ax2.plot(time_data, roll_data, "r*--", label="Roll : X (°)" )
plot_yaw, = ax2.plot(time_data, yaw_data, "bs:", label="Yaw  : Z (°)" )

ax2.set_ylabel("Angle (°)")
ax2.set_xlabel("Time (s)")
ax2.legend(loc="upper left")
ax2.set_title("IMU Orientation - Pitch, Roll, Yaw (Without Calibration)") 

plots = [ plot_pitch, plot_roll, plot_yaw, plot_x, plot_y, plot_z ]

plt.tight_layout()

start_time = None

# 실시간 업데이트 함수
def update( frame ):
    global last_angles, last_velocity, last_position, last_time, start_time

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    if start_time is None : start_time = current_time

    elapsed = current_time - start_time

    accel = read_accel()
    gyro = read_gyro()
    
    # 자세 계산
    (pitch_y, roll_x, yaw_z) = calculate_angles(gyro, dt, last_angles)
    last_angles = (pitch_y, roll_x, yaw_z)

    # 위치 계산
    last_velocity, last_position = calculate_position(accel, last_velocity, last_position, dt)
    x, y, z = last_position
    velocity = last_velocity

    print()
    print( "-"*40 )
    print( f"[{frame:4d}] elapsed  = {elapsed:.1f} (secs)" )
    print( f"[{frame:4d}] gyro     = {degrees(gyro[0]):.3f}, {degrees(gyro[1]):.3f}, {degrees(gyro[2]):.3f} (°/s)" )
    print( f"[{frame:4d}] angle    = {degrees(roll_x):.3f}, {degrees(pitch_y):.3f}, {degrees(yaw_z):.3f} (°)" )
    
    print( f"[{frame:4d}] accel    = {accel[0]:.3f}, {accel[1]:.3f}, {accel[2]:.3f} (g)" )
    print( f"[{frame:4d}] velocity = {velocity[0]:.3f}, {velocity[1]:.3f}, {velocity[2]:.3f} (9.8 m/s)" )
    print( f"[{frame:4d}] position = {x:.3f}, {y:.3f}, {z:.3f} (9.8 m)" )
    print( "-"*40 )

    if len( time_data ) > 60 :
        time_data.pop( 0 )

        pitch_data.pop( 0 )
        roll_data.pop( 0 )
        yaw_data.pop( 0 )

        x_data.pop( 0 )
        y_data.pop( 0 )
        z_data.pop( 0 )

        del angle_data[:3]
        del xyz_data[:3]
    pass

    # 데이터 추가
    time_data.append( elapsed )

    pitch_data.append( degrees(pitch_y) )
    roll_data.append( degrees(roll_x) )
    yaw_data.append( degrees(yaw_z) )

    x_data.append( x )
    y_data.append( y )
    z_data.append( z )

    plot_pitch.set_data( time_data, pitch_data )
    plot_roll.set_data( time_data, roll_data )
    plot_yaw.set_data( time_data, yaw_data )

    plot_x.set_data( time_data, x_data )
    plot_y.set_data( time_data, y_data )
    plot_z.set_data( time_data, z_data )

    angle_data.append( degrees(pitch_y) )
    angle_data.append( degrees(roll_x) )
    angle_data.append( degrees(yaw_z) )

    xyz_data.append( x )
    xyz_data.append( y )
    xyz_data.append( z ) 

    ax1.set_xlim( min( time_data ), max( 1, max( time_data) ) ) 
    ax2.set_xlim( min( time_data ), max( 1, max( time_data) ) )

    ax1.set_ylim( min( 0, min( xyz_data )*1.1), max( 0, max( xyz_data )*1.1 ) )
    ax2.set_ylim( min( 0, min( angle_data )*1.1), max( 0, max( angle_data )*1.1 ) )
    
    return plots
pass

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=0 )

plt.show()
