from machine import Pin
from time import sleep

# 행(row) 핀들을 초기화하고 출력 모드로 설정합니다.
row_pins = [ Pin(10, mode=Pin.OUT),
             Pin(9, mode=Pin.OUT),
             Pin(8, mode=Pin.OUT),
             Pin(7, mode=Pin.OUT) ]

# 열(column) 핀들을 초기화하고 출력 모드로 설정합니다.
col_pins = [ Pin(12, mode=Pin.OUT),
             Pin(13, mode=Pin.OUT),
             Pin(14, mode=Pin.OUT),
             Pin(15, mode=Pin.OUT) ]

# 행과 열의 개수를 저장합니다.
row_len = len(row_pins)
col_len = len(col_pins)

# 특정 행 핀들의 상태를 설정하는 함수입니다.
def set_row_pins(state, *rows):
    # 인자가 없을 경우 모든 행을 대상으로 합니다.
    if rows is None or rows[0] is None:
        rows = range(row_len)
    
    # 지정된 행들의 핀 상태를 설정합니다.
    for row in rows:
        if state: 
            row_pins[row].off()  # LED 켜기 (가정: Active-Low)
        else:
            row_pins[row].on()   # LED 끄기
    pass
pass

# 특정 열 핀들의 상태를 설정하는 함수입니다.
def set_col_pins(state, *cols):
    # 인자가 없을 경우 모든 열을 대상으로 합니다.
    if cols is None or cols[0] is None:
        cols = range(col_len)
    
    # 지정된 열들의 핀 상태를 설정합니다.
    for col in cols:
        if state: 
            col_pins[col].on()   # LED 켜기
        else:
            col_pins[col].off()  # LED 끄기
    pass
pass

# 특정 행과 열의 LED를 켜는 함수입니다.
def turn_on(row=None, col=None, duration=0.1):
    set_row_pins(True, row)  # 지정된 행의 핀을 켭니다.
    set_col_pins(True, col)  # 지정된 열의 핀을 켭니다.
    sleep(duration)  # 지정된 시간 동안 대기합니다.
pass

# 특정 행과 열의 LED를 끄는 함수입니다.
def turn_off(row=None, col=None, duration=0.1):
    set_row_pins(False, row)  # 지정된 행의 핀을 끕니다.
    set_col_pins(False, col)  # 지정된 열의 핀을 끕니다.
    sleep(duration)  # 지정된 시간 동안 대기합니다.
pass

# 특정 행과 열의 LED를 켜고 난 후 끄는 함수입니다.
def toggle(row=None, col=None, duration=0.1):
    turn_on(row, col, duration)  # LED를 켭니다.
    turn_off(row, col, duration)  # LED를 끕니다.
pass

# LED 토글 시 대기 시간 설정
duration = 0.5
scene_duration = 1.5

# 모든 핀을 세 번 토글합니다.
print("toggle all pins")
for _ in range(3):
    toggle(duration=duration)
pass

# 대기 시간
sleep( scene_duration )

# 모든 핀을 순차적으로 오름차순으로 토글합니다.
print("toggle each pin in ascending order of pin number")
for row in range(row_len):
    for col in range(col_len):
        toggle(row=row, col=col, duration=duration)
    pass
pass

# 대기 시간
sleep( scene_duration )

# 모든 핀을 내림차순으로 토글합니다.
print("toggle each pin in descending order of pin number")
for row in range(row_len - 1, -1, -1):
    for col in range(col_len - 1, -1, -1):
        toggle(row=row, col=col, duration=duration)
    pass
pass

# 대기 시간
sleep( scene_duration )

# 지그재그 패턴으로 핀을 토글합니다.
print("toggle each pin in zigzag direction")
for row in range(row_len):
    # 짝수 행은 왼쪽에서 오른쪽으로, 홀수 행은 오른쪽에서 왼쪽으로
    rng = range(col_len - 1, -1, -1) if row % 2 else range(col_len)
    
    for col in rng:
        toggle(row=row, col=col, duration=duration)
    pass
pass

# 대기 시간
sleep( scene_duration )

# 나선형 방향으로 핀을 토글합니다.
print("toggle each pin in spiral direction")
n = [[0] * col_len for _ in range(row_len)]  # LED 행렬을 초기화

row = 0  # 시작 행 위치
col = 0  # 시작 열 위치
direction = 0  # 이동 방향 (0: 오른쪽, 1: 아래, 2: 왼쪽, 3: 위)

# 행렬을 나선형으로 탐색하며 핀을 토글합니다.
for i in range(1, row_len * col_len + 1):
    n[row][col] = i
    toggle(row=row, col=col, duration=duration)

    # 다음 위치 계산
    if direction == 0:  # 오른쪽으로 이동
        if col < col_len - 1 and n[row][col + 1] == 0:
            col += 1
        else:
            direction = 1  # 아래로 방향 전환
            row += 1
    elif direction == 1:  # 아래로 이동
        if row < row_len - 1 and n[row + 1][col] == 0:
            row += 1
        else:
            direction = 2  # 왼쪽으로 방향 전환
            col -= 1
    elif direction == 2:  # 왼쪽으로 이동
        if col > 0 and n[row][col - 1] == 0:
            col -= 1
        else:
            direction = 3  # 위로 방향 전환
            row -= 1
    elif direction == 3:  # 위로 이동
        if row > 0 and n[row - 1][col] == 0:
            row -= 1
        else:
            direction = 0  # 다시 오른쪽으로 방향 전환
            col += 1
    pass 
pass # toggle_spiral_direction

# 대기 시간
sleep( scene_duration )

# 각 행을 순차적으로 토글합니다.
print("toggle each row in ascending order of row number")
for row in range(row_len):
    toggle(row=row, duration=duration)
pass

# 대기 시간
sleep( scene_duration )

# 각 열을 순차적으로 토글합니다.
print("toggle each column in ascending order of pin number")
for col in range(col_len):
    toggle(col=col, duration=duration)
pass 

# 모든 LED를 끕니다.
turn_off()

# 대기 시간
sleep( scene_duration )

# 각 행을 순차적으로 켭니다.
print("turn on each row in ascending order of row number")
for row in range(row_len):
    turn_on(row=row, duration=duration)
pass

# 대기 시간
sleep( scene_duration )

# 각 행을 역순으로 끕니다.
print("turn off each row in descending order of row number")
for row in range(row_len - 1, -1, -1):
    set_row_pins(False, row)
    sleep(1)  # 각 행을 끄는 시간 간격 설정
pass

# 모든 LED를 끕니다.
turn_off()

# 대기 시간
sleep( scene_duration )

# 각 열을 순차적으로 켭니다.
print("turn on each column in ascending order of row number")
for col in range(col_len):
    turn_on(col=col, duration=duration)
pass

# 대기 시간
sleep( scene_duration )

# 각 열을 역순으로 끕니다.
print("turn off each column in descending order of row number")
for col in range(col_len - 1, -1, -1):
    set_col_pins(False, col)
    sleep(1)  # 각 열을 끄는 시간 간격 설정
pass
 
