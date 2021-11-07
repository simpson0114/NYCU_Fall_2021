from pwn import *
from Crypto.Util.number import *
from hashlib import sha256, md5
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature
from sage.all import *

ecE = SECP256k1
ecG = ecE.generator
ecn = ecE.order
A = int('5ebe2294ecd0e0f08eab7690d2a6ee69' + '00000000000000000000000000000000', 16)
K = int('1' + '00000000000000000000000000000000', 16)

print(ecn)

serv = remote('edu-ctf.csie.org', '42074')
a = serv.recvline().decode(encoding='UTF-8').lstrip('P = (').rstrip(')\n').split(',')
pubkeyX = int(a[0])
pubkeyY = int(a[1])

tempt = serv.recvline()
tempt = serv.recvline()
tempt = serv.recvline()
tempt = serv.recvline()

serv.send(b'1\n')
tempt = serv.recvline()
serv.send(b'1\n')
h1 = int.from_bytes(sha256('1'.encode()).digest(), 'big')
sig1 = serv.recvline().decode(encoding = 'UTF-8').lstrip('(').rstrip(')\n').split(',')
r1 = int(sig1[0])
s1 = int(sig1[1])


tempt = serv.recvline()
tempt = serv.recvline()
tempt = serv.recvline()
tempt = serv.recvline()

serv.send(b'1\n')
tempt = serv.recvline()
serv.send(b'2\n')
h2 = int.from_bytes(sha256('2'.encode()).digest(), 'big')
sig2 = serv.recvline().decode(encoding = 'UTF-8').lstrip('(').rstrip(')\n').split(',')
r2 = int(sig2[0])
s2 = int(sig2[1])
print(s1)
print(r2)

t = -s2*r1 * inverse_mod(s1 * r2, ecn)
u = r1 * h2 * inverse_mod(s1 * r2, ecn) - h1 * inverse_mod(s1, ecn)

L = matrix(ZZ, [[ecn, 0, 0], [t, 1, 0], [A + A*t + u, 0, K]])
B = L.LLL()
print(B)
print(K)

for row in B.rows():
    if row[2] == K and row[0] < 0:
        k1 = -row[0] + A
        k2 = row[1] + A
        break

d = (s1*k1*h2 - s2*h1*k2) * inverse_mod(s2*r1*k2 - s1*r2*k1, ecn) % ecn
pubkey = Public_key(ecG, d*ecG)
prikey = Private_key(pubkey, d)

msg = 'Kuruwa'
h = sha256(msg.encode()).digest()
h_num = int.from_bytes(sha256(msg.encode()).digest(), 'big')
k = int(md5(b'secret').hexdigest() + md5(long_to_bytes(prikey.secret_multiplier) + h).hexdigest(), 16)
r = (k * ecG).x() % ecn
s = (h_num + d * r) * inverse_mod(k, ecn) % ecn

serv.recvline()
serv.recvline()
serv.recvline()
serv.recvline()

serv.send(b'2\n')
print(serv.recvuntil(': '))
serv.send(b'Kuruwa\n')
print(serv.recvuntil(': '))
serv.send(str(r) + '\n')
print(serv.recvuntil(': '))
serv.send(str(s) + '\n')
print(serv.recvline())