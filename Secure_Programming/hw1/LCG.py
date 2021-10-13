from Crypto.Util.number import *
import random
from randcrack import RandCrack

class LCG():
    def __init__(self, seed):
        self.state = seed
        self.m = 2**32
        self.A = random.getrandbits(32) | 1
        self.B = random.getrandbits(32) | 1

    
    def getbits(self):
        self.clock()
        return self.state

    def clock(self):
        self.state = (self.A * self.state + self.B) % self.m

rng = LCG()
print(rng.A, rng.B)
S = []
for i in range(3):
    S.append(rng.getbits())

# S[1] = AS[0] + B
# S[2] = AS[1] + B

A = (S[1] - S[2]) * inverse(S[0] - S[1], rng.m)
print(A)



# 預測 python random 的工具
rc = RandCrack()
for i in range(624):
    rc.submit(random.getrandbits(32))

print(rc.predict_randrange(2**64))
print(random.randrange(2**64))    