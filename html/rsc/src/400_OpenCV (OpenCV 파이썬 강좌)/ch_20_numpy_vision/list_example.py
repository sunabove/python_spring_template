# coding: utf-8
import numpy as np

# Python List Manipulation
a = [ 1, 2, 3 ]
b = [ q*2 for q in a ]
print( b )

a = [ 1, 2, 3 ]
b = [ 4, 5, 6 ]
c = [ q*r for q, r in zip(a, b) ]
print( c )
