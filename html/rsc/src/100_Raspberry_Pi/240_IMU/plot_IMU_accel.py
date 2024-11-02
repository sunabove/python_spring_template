# plot_IMU.py
import smbus
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# MPU-6050 초기 설정
bus = smbus.SMBus(1)  # I2C 버스 번호 (Raspberry Pi의 경우 보통 1번)
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
    return value

def read_accel():
    x = read_word(ACCEL_XOUT_H) / 16384.0
    y = read_word(ACCEL_YOUT_H) / 16384.0
    z = read_word(ACCEL_ZOUT_H) / 16384.0
    return (x, y, z)

def read_gyro():
    x = read_word(GYRO_XOUT_H) / 131.0
    y = read_word(GYRO_YOUT_H) / 131.0
    z = read_word(GYRO_ZOUT_H) / 131.0
    return (x, y, z)

# 그래프 초기화
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
accel_x_data, accel_y_data, accel_z_data = [], [], []
gyro_x_data, gyro_y_data, gyro_z_data = [], [], []
time_data = []

# 가속도 그래프
plot_ax, = ax1.plot(time_data, accel_x_data, "gp-", label="Accel X (g)")
plot_ay, = ax1.plot(time_data, accel_y_data, "r*--", label="Accel Y (g)")
plot_az, = ax1.plot(time_data, accel_z_data, "bs:", label="Accel Z (g)")

ax1.set_title("Accelerometer Data")
ax1.set_ylabel("Acceleration (g)")
ax1.set_xlabel("Time (s)")
ax1.legend(loc="upper right")

# 자이로 그래프
plot_gx, = ax2.plot(time_data, gyro_x_data, "gp-", label="Gyro X (°/s)")
plot_gy, = ax2.plot(time_data, gyro_y_data, "r*--", label="Gyro Y (°/s)")
plot_gz, = ax2.plot(time_data, gyro_z_data, "bs:", label="Gyro Z (°/s)")

ax2.set_title("Gyroscope Data")
ax2.set_ylabel("Angular Velocity (°/s)")
ax2.set_xlabel("Time (s)")
ax2.legend(loc="upper right")

ax1.grid(1, linestyle='--')
ax2.grid(1, linestyle='--')

plots = [ plot_ax, plot_ay, plot_az, plot_gx, plot_gy, plot_gz ]

plt.tight_layout()

start_time = time.time()

# 실시간 업데이트 함수
def update(frame):
    
    accel_x, accel_y, accel_z = read_accel()
    gyro_x, gyro_y, gyro_z = read_gyro()
    current_time = time.time()
    elapsed = current_time - start_time

    print()
    print( "-"*40 )
    print( f"[{frame:4d}] elapsed = {elapsed:.1f} (secs)" )
    print( f"[{frame:4d}] accl = {accel_x:.3f}, {accel_y:.3f}, {accel_z:.3f} (g)" )
    print( f"[{frame:4d}] gyro = {gyro_x:.3f}, {gyro_z:.3f}, {gyro_z:.3f} (°/s)" )
    print( "-"*40 )

    # 데이터 추가
    time_data.append( elapsed )
    
    accel_x_data.append(accel_x)
    accel_y_data.append(accel_y)
    accel_z_data.append(accel_z)

    gyro_x_data.append(gyro_x)
    gyro_y_data.append(gyro_y)
    gyro_z_data.append(gyro_z)

    plot_ax.set_data(time_data, accel_x_data )
    plot_ay.set_data(time_data, accel_y_data )
    plot_az.set_data(time_data, accel_z_data )

    plot_gx.set_data(time_data, gyro_x_data )
    plot_gy.set_data(time_data, gyro_y_data )
    plot_gz.set_data(time_data, gyro_z_data )

    accel_datas = accel_x_data + accel_y_data + accel_z_data
    gyro_datas = gyro_x_data + gyro_y_data + gyro_z_data

    ax1.set_xlim( 0, max( 1, max( time_data) ) ) 
    ax2.set_xlim( 0, max( 1, max( time_data) ) )
    
    ax1.set_ylim( min( 0, min( accel_datas )*1.1),
                  max( 0, max( accel_datas )*1.1 ) ) 
    
    ax2.set_ylim( min( 0, min( gyro_datas )*1.1),
                  max( 0, max( gyro_datas )*1.1 ) )

    return plots
pass

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)

plt.show()
