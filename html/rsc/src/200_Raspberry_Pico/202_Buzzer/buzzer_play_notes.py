from time import sleep
from picozero import Speaker, LED
from machine import Timer

led = LED(25)

timer = Timer()

def led_blink( timer ):
    led.toggle()

timer.init( freq=1, mode=Timer.PERIODIC, callback=led_blink )

speaker = Speaker(4)

notes ="""b0,c1,c#1,d1,d#1,e1,f1,f#1,g1,g#1,a1,a#1,b1,c2,c#2,d2,d#2,e2,
f2,f#2,g2,g#2,a2,a#2,b2,c3,c#3,d3,d#3,e3,f3,f#3,g3,g#3,a3,a#3,b3,c4,c#4,
d4,d#4,e4,f4,f#4,g4,g#4,a4,a#4,b4,c5,c#5,d5,d#5,e5,f5,f#5,g5,g#5,a5,a#5,
b5,c6,c#6,d6,d#6,e6,f6,f#6,g6,g#6,a6,a#6,b6,c7,c#7,d7,d#7,e7,f7,f#7,
g7,g#7,a7,a#7,b7,c8,c#8,d8,d#8"""

notes = notes.strip().split(",")
notes_len = len( notes )

BEAT = 1

start = 37
end = start + 25

while 1 : 
    for idx, note in enumerate( notes[start:end] ) :
        note = note.strip()
        if "#" not in note :
            print( f"[{ start + idx:3d}/{end - start}] speaker play note: {note}" )
            speaker.play( note, BEAT*2 )
    pass
    
    sleep( 2 )
pass
