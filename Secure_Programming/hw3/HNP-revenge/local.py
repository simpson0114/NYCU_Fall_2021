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
a = int('5ebe2294ecd0e0f08eab7690d2a6ee69' + '00000000000000000000000000000000', 16)
K = int('100000000000000000000000000000000', 16)
print(k - a == int(md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16))
k1 = k
print('k1 ' + str(k % n))
print('a ' + str(a))
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
r = (k * G).x() % n
s = (h2 + d * r) * inverse_mod(k, n) % n
print(r2 == r)
print(s2 == s)

t = -s2*r1 * inverse_mod(s1*r2, n)
u = r1 * h2 * inverse_mod(s1 * r2, n) - h1 * inverse_mod(s1, n)

L = matrix(ZZ, [[n, 0, 0], [t, 1, 0], [a + a*t + u, 0, K]])
B = L.LLL()

for row in B.rows():
    if row[2] == K:
        print(-row[0])
        print(row[1])
        k1_g = -row[0] + a
        k2_g = row[1] + a
        break

print(k1 == k1_g)
print(k2 == k2_g)

dguess = (s1*h2*k1 - s2*h1*k2) * inverse_mod(s2*r1*k2 - s1*r2*k1, n) % n

print('d = ' + str(d))
print('dguess = ' + str(dguess))
print(k1)
print('md5 ' + str(md5(b'secret').hexdigest()))
print(md5(b'secret').hexdigest() + md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest())
print(sha256(msg.encode()).digest())
print(long_to_bytes(prikey.secret_multiplier))
print(h)
# for _ in range(3):
#     print('''
# 1) talk to Kuruwa
# 2) login
# 3) exit''')
#     option = input()
#     if option == '1':
#         msg = input('Who are you?\n')
#         if msg == 'Kuruwa':
#                 print('No you are not...')
#         else:
#             h = sha256(msg.encode()).digest()
#             k = int(md5(b'secret').hexdigest() + md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16)
#             sig = prikey.sign(bytes_to_long(h), k)
#             print(f'({sig.r}, {sig.s})')

#     elif option == '2':
#         msg = input('username: ')
#         r = input('r: ')
#         s = input('s: ')
#         h = bytes_to_long(sha256(msg.encode()).digest())
#         verified = pubkey.verifies(h, Signature(int(r), int(s)))
#         if verified:
#             if msg == 'Kuruwa':
#                 print(FLAG)
#             else:
#                 print('Bad username')
#         else:
#             print('Bad signature')
#     else:
#         break
