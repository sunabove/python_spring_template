from machine import Pin
from time import sleep

row_pins = [ Pin(15, mode=Pin.OUT),
             Pin(14, mode=Pin.OUT),
             Pin(13, mode=Pin.OUT),
             Pin(12, mode=Pin.OUT) ]

col_pins = [ Pin(16, mode=Pin.OUT),
             Pin(17, mode=Pin.OUT),
             Pin(18, mode=Pin.OUT),
             Pin(19, mode=Pin.OUT) ]

row_len = len( row_pins )
col_len = len( col_pins )

def set_row_pins(state, *rows):
    if rows is None or rows[0] is None:
        rows = range( row_len ) 
    
    for row in rows:
        if state: 
            row_pins[row].off()  # LED 켜기 (가정: Active-Low)
        else:
            row_pins[row].on()   # LED 끄기
        pass
    pass
pass

def set_col_pins(state, *cols):
    if cols is None or cols[0] is None :
        cols = range( col_len )
    pass
    
    for col in cols:
        if state: 
            col_pins[col].on()   # LED 켜기
        else:
            col_pins[col].off()  # LED 끄기
        pass
    pass
pass

def turn_on(row=None, col=None, duration=0.1):
    set_row_pins(True, row)
    set_col_pins(True, col)
    
    sleep(duration)
pass

def turn_off(row=None, col=None, duration=0.1):
    set_row_pins(False, row)
    set_col_pins(False, col)
    
    sleep(duration)
pass

def toggle(row=None, col=None, duration=0.1):
    turn_on(row, col, duration)
    
    turn_off(row, col, duration)
pass

duration = 0.5

print( "toggle all pins" )
for _ in range( 3 ):
    toggle(duration=duration)
pass

print( "toggle each pin ascending pin number" )
for row in range( row_len ):
    for col in range( col_len ) :
        toggle(row=row, col=col, duration=duration)
    pass
pass

print( "toggle each pin descending pin numbers" )
for row in range( row_len -1, -1, -1 ):
    rng = range( col_len -1, -1, -1 ) if row%2 else range( col_len ) 
    
    for col in rng :
        toggle(row=row, col=col, duration=duration)
    pass
pass

print( "toggle each pin in zigzag direction" )
for row in range( row_len ):
    rng = range( col_len -1, -1, -1 ) if row%2 else range( col_len ) 
    
    for col in rng :
        toggle(row=row, col=col, duration=duration)
    pass
pass

print( "toggle each pin in sprial direction" )
# toggle_spiral_direction
n = [[0] * col_len for _ in range(row_len)]

row = 0
col = 0
direction = 0
    
for i in range( 1, row_len*col_len + 1 ) :
    n[row][col] = i
    
    toggle(row=row, col=col, duration=duration)

    # 다음 위치 계산
    if direction == 0:  # 오른쪽으로 이동
        if col < col_len - 1 and n[row][col + 1] == 0:
            col += 1
        else:
            direction = 1
            row += 1
        pass
    elif direction == 1:  # 아래로 이동
        if row < row_len - 1 and n[row + 1][col] == 0:
            row += 1
        else:
            direction = 2
            col -= 1
    elif direction == 2:  # 왼쪽으로 이동
        if col > 0 and n[row][col - 1] == 0:
            col -= 1
        else:
            direction = 3
            row -= 1
    elif direction == 3:  # 위로 이동
        if row > 0 and n[row - 1][col] == 0:
            row -= 1
        else:
            direction = 0
            col += 1
    pass 
pass # toggle_spiral_direction

print( "toggle each row asceding row number" )
for row in range( row_len ):
    toggle(row=row, duration=duration)
pass

print( "toggle each colums ascending pin numbers" )
for col in range( col_len ):
    toggle(col=col, duration=duration)
pass 

turn_off()

print( "turn on each rows asceding row numbers" )
for row in range( row_len ):
    turn_on(row=row, duration=duration)
pass

print( "turn off each rows desceding row numbers" )
for row in range( row_len -1, -1, -1 ):
    set_row_pins(False, row)
    
    sleep(1)
pass

turn_off()

print( "turn on each columns asceding row numbers" )
for col in range( col_len ):
    turn_on(col=col, duration=duration)
pass

print( "turn off each columns desceding row numbers" )
for col in range( col_len -1, -1, -1 ):
    set_col_pins(False, col)
    
    sleep(1)
pass

turn_on()