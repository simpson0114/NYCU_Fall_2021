#!/usr/bin/env python3
from random import randint
from Crypto.Util.number import *
from hashlib import sha256, md5
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature
from sage.all import *
# FLAG = open("flag", 'r').read()

E = SECP256k1
G, n = E.generator, E.order

d = randint(1, n)

pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)
print(f'P = ({pubkey.point.x()}, {pubkey.point.y()})')
print(prikey.secret_multiplier)
print(d)
print(E)
print(G)
print(n)

msg = '1'
h = sha256(msg.encode()).digest()
h1 = int.from_bytes(sha256(msg.encode()).digest(), 'big')
k = int(md5(b'secret').hexdigest() + md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16)
K = int('5ebe2294ecd0e0f08eab7690d2a6ee69' + '00000000000000000000000000000000', 16)
k1 = k
print('k1 ' + str(k % n))
sig = prikey.sign(bytes_to_long(h), k)
print(f'({sig.r}, {sig.s})')
r1 = sig.r
s1 = sig.s

msg = '2'
h = sha256(msg.encode()).digest()
h2 = int.from_bytes(sha256(msg.encode()).digest(), 'big')
k = int(md5(b'secret').hexdigest() + md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16)
k2 = k
print('k2 ' + str(k2 % n))
sig = prikey.sign(bytes_to_long(h), k)
print(f'({sig.r}, {sig.s})')
r2 = sig.r
s2 = sig.s

t = -s2*r1 * inverse_mod(s1*r2, n)
u = r1 * h2 * inverse_mod(s1 * r2, n) - h1 * inverse_mod(s1, n)

G.<x, y> = PolynomialRing(Zmod(n))
f  = x + t * y + u
print(f.small_roots(X = K))