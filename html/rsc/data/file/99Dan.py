# -*- coding: utf-8 -*-

fw = 119
w = fw//4*4
borders = [ 
            [ "╔", "╦", "╗" ],
            [ "║", "║", "║" ],
            [ "╠", "╦", "╣" ],
            [ "╠", "╬", "╣" ],
            [ "╚", "╩", "╝" ] 
        ]

def my_print( btype = 0, c = " ", *cells ) :
    if len( cells ) == 0 : 
        cells = [ "" ]
    elif len( cells ) == 1 and type(cells[0]) is list:
        cells = cells[0]
    pass

    len_cells = len( cells )
    tw = w // len_cells
    
    line = ""
    for i, cell in enumerate( cells ) : 
        b = borders[btype]
        t = ""

        t += b[0] if i == 0 else b[1]
        
        t += cell.center( tw - ( len(cell) - len(cell.encode("ascii", "ignore"))  + 1), c ) 

        t += b[-1] if i == len_cells -1 else "" 
        
        line += t
    pass

    print( " ", line )
pass

print()
my_print( 0, "═" ) 
my_print( 1, " ", "구구단" )

for i in range( 2, 7, 4 ) :
    my_print( [3, 2][ i == 2 ], "═", [""] * 4 )
    my_print( 1, " ", [ f"{i + c} 단" for c in range(4) ] )
    my_print( 3, "═", [""] * 4 )
    for r in range( 1, 10 ) :
        my_print( 1, " ", [ f"{i + c} x {r} = {(i+c)*r:2}" for c in range(4) ] )
    pass
pass

my_print( 4, "═", [""] * 4 )