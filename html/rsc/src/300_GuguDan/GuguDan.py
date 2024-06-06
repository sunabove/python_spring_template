line = "="*50
for i in range( 2 ) :
    print( line )
    for k in range( 1, 10 ) :
        for m in range( 4 ) :
            dan = 4*i + m + 2
            print( dan, "x" , k , "=", f"{dan*k:2d}", " ", end="" )
        pass
        print()
    pass
pass
print( line )