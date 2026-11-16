#!/usr/bin/env python3
"""One-dimensional idealized constant proper acceleration in flat spacetime.
Not a round-trip or propulsion model. SI constants, Julian year.
"""
import math
C=299792458.0
G0=9.80665
YEAR=365.25*86400.0

def trajectory(tau_years, acceleration=G0):
    tau=tau_years*YEAR
    z=acceleration*tau/C
    earth_years=(C/acceleration)*math.sinh(z)/YEAR
    light_years=(C/acceleration)*2*math.sinh(z/2)**2/YEAR
    beta=math.tanh(z)
    return earth_years,light_years,beta

def test():
    assert trajectory(0)==(0.0,0.0,0.0)
    t,x,b=trajectory(1)
    assert abs(t-1.187312402)<1e-9
    assert abs(x-0.563642465)<1e-9
    assert abs(b-0.774827263)<1e-9
    for y in (0,1,2,5):
        t,x,b=trajectory(y)
        L=C/G0/YEAR
        assert abs(((x+L)**2-t*t)-L*L)<1e-8, (y,t,x,b)
        assert 0<=b<1
    print("PASS: 12 analytic invariants and benchmark assertions")

if __name__=="__main__":
    test()
    for y in (0,1,2,5):
        t,x,b=trajectory(y)
        print(f"tau={y} yr; earth_t={t:.9f} yr; x={x:.9f} ly; beta={b:.9f}")
