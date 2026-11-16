#!/usr/bin/env python3
"""Independent one-leg accelerated-worldline verification. Standard library only."""
import math
C=299792458.0
A=9.80665
Y=31557600.0
def model(y):
    z=A*y*Y/C
    return (C/A/Y*math.sinh(z),C/A/Y*2*math.sinh(z/2)**2,math.tanh(z))
for y in [0,1,2,5]:
    t,x,v=model(y)
    L=C/A/Y
    assert abs((x+L)**2-t*t-L*L)<1e-8
    assert abs(v)<1
    print(f'{y}: {t:.9f} yr, {x:.9f} ly, {v:.9f} c')
print('PASS: 8 checks, independent local formula implementation')
