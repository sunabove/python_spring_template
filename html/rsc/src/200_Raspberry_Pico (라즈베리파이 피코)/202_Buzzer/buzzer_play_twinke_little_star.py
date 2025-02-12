from time import sleep
from picozero import Speaker, LED

led = LED(25)
speaker = Speaker(4)

BEAT = 0.4

melodies = [
    ['c4', BEAT ], ['c4', BEAT ], ['g4', BEAT ], ['g4', BEAT ], ['a5', BEAT ], ['a5', BEAT ], ['g4', BEAT*2 ],
    ['f4', BEAT ], ['f4', BEAT ], ['e4', BEAT ], ['e4', BEAT ], ['d4', BEAT ], ['d4', BEAT ], ['c4', BEAT*2 ],
    
    ['g4', BEAT ], ['g4', BEAT ], ['f4', BEAT ], ['f4', BEAT ], ['e4', BEAT ], ['e4', BEAT ], ['d4', BEAT*2 ],
    ['g4', BEAT ], ['g4', BEAT ], ['f4', BEAT ], ['f4', BEAT ], ['e4', BEAT ], ['e4', BEAT ], ['d4', BEAT*2 ],
    
    ['c4', BEAT ], ['c4', BEAT ], ['g4', BEAT ], ['g4', BEAT ], ['a5', BEAT ], ['a5', BEAT ], ['g4', BEAT*2 ],
    ['f4', BEAT ], ['f4', BEAT ], ['e4', BEAT ], ['e4', BEAT ], ['d4', BEAT ], ['d4', BEAT ], ['c4', BEAT*2 ],
]

sleep( 1 )

try :
    for _ in range( 2 ) :
        led.toggle()
        speaker.play( melodies )
        sleep( 3 )
    pass
except :
    pass
finally:
    led.off()
pass
