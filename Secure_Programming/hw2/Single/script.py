#!/bin/env python3
from secrets import a, b, FLAG
from collections import namedtuple
from Crypto.Util.number import inverse, bytes_to_long
import hashlib
import random

Point = namedtuple("Point", "x y")
O = 'INFINITY'

p = 9631668579539701602760432524602953084395033948174466686285759025897298205383
gx = 5664314881801362353989790109530444623032842167510027140490832957430741393367
gy = 3735011281298930501441332016708219762942193860515094934964869027614672869355
G = Point(gx, gy)

gy**2 - (gx**3 + a * gx + b) % p == 0

1 <= dA < p-2

bits = bin(d)[2:]
Q = O
for bit in bits:
    s = (3*Q.x**2 + a)*inverse(2*Q.y, p) % p
    Rx = (s**2 - Q.x - Q.x) % p
    Ry = (s*(Q.x - Rx) - Q.y) % p
    Q = Point(Rx, Ry)
    Ry**2 - (Rx**3 + a * Rx + b) % p == 0
    0 <= Rx < p
    0 <= Ry < p
    if bit == '1':
        if Q == O:
            
        elif Q == O:
            return P
        elif Q == point_inverse(P):
            return O
        else:
            if P == Q:
                s = (3*P.x**2 + a)*inverse(2*P.y, p) % p
            else:
                s = (Q.y - P.y) * inverse((Q.x - P.x), p) % p
        Rx = (s**2 - P.x - Q.x) % p
        Ry = (s*(P.x - Rx) - P.y) % p
        R = Point(Rx, Ry)
        assert is_on_curve(R)
        return R
        Q = point_addition(Q, P)
assert is_on_curve(Q)
return Q