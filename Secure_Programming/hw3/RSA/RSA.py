from sage.all import *

p = random_prime(2^512)
q = random_prime(2^512)
n = p * q
x0 = randrange(1, 2^128)
pad = randrange(1, 2^888)
m = (pad << 128) + x0
print(n - m)
assert m < n
c = pow(m, 3, n)


R = 2^128
a = (pad << 128)
L = matrix(ZZ, [[R^3, 3*a*R^2, 3*a^2*R, a^3-c], [0, n*R^2, 0, 0], [0, 0, n*R, 0], [0, 0, 0, n]])
v = L.LLL()[0]

F.<x> = PolynomialRing(ZZ)
Q = v[0]//R^3 * x^3 + v[1]//R^2 * x^2 + v[2]//R * x + v[3]
print(Q.roots())

G.<x> = PolynomialRing(Zmod(n))
g = (a+y)^3 - c
g.small_rooots(X=2^128)