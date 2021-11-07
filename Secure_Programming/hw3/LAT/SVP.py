from sage.all import *
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
import random
import math

FLAG = b'FLAG{????????????????????}'


def gen_key():
    q = getPrime(512)
    upper_bound = int(math.sqrt(q // 2))
    lower_bound = int(math.sqrt(q // 4))
    f = random.randint(2, upper_bound)
    while True:
        g = random.randint(lower_bound, upper_bound)
        if math.gcd(f, g) == 1:
            break
    h = (inverse(f, q)*g) % q
    return (q, h), (f, g)


def encrypt(q, h, m):
    assert m < int(math.sqrt(q // 2))
    r = random.randint(2, int(math.sqrt(q // 2)))
    e = (r*h + m) % q
    return e


def decrypt(q, h, f, g, e):
    a = (f*e) % q
    m = (a*inverse(f, g)) % g
    return m


q = 13198797472876287864902532913662133207745076880722933181850739256048248640200371699901863528719230289037546070463557840514069399741170318469168055220829673
h = 10087945478419986810683355485899283062694316065852893531674190136106148631015543635096193003039720583579764280499310840409413968369520060566979727182282589
e = 8989708726503367404715754689730782388959095528339234074784589050444870239608140046626770182336762701788963731736424741343914003600890982230995409715448250

v1 = vector((1, h))
v2 = vector((0, q))

# Gaussian Lattice Reduction
while True:
    if v2.norm() < v1.norm():
        v1, v2 = v2, v1
    m = round(v1*v2/(v1*v1))
    if m == 0:
        break
    v2 = v2 - m * v1

# SVP (Shortest Vector Problem)
f = v1[0]
g = v1[1]


h = (inverse(f, q)*g) % q

print(long_to_bytes(decrypt(q, h, f, g, e)))