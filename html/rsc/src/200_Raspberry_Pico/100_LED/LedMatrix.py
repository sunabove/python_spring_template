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

for _ in range( 3 ):
    toggle(duration=duration)
pass

for row in range( row_len ):
    for col in range( col_len ) :
        toggle(row=row, col=col, duration=duration)
    pass
pass

for row in range( row_len ):
    rng = range( col_len -1, -1, -1 ) if row%2 else range( col_len ) 
    
    for col in rng :
        toggle(row=row, col=col, duration=duration)
    pass
pass

turn_on()