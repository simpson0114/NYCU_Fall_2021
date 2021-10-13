from sage.all import *
class LFSR:
    def __init__(self, key, taps):
        d = max(taps)
        assert len(key) == d, "Error: key of wrong size."
        self._s = key
        self._t = [d - t for t in taps]

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s
    
    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self.s[p] for p in self._t)]
        return b

    def getbit(self):
        return self._clock()

key = [1, 0 ,0]
taps = [3, 2]
rng = LFSR(key, taps)
for _ in range(20):
    print(rng.getbit())
                
F = PolynomialRing(GF(2), 'x')
x = F.gen()
P = x^3 + x + 1
C = companion_matrix(P, format = 'bottom')
C

import itertools
key_len = 64

for b in range(key_len):
    for c in itertools.combinations(range(key_len), b):
        key_candidate = [1 - stream[i] if i in c else stream[i] for i in range(key_len)]
        lfsr = LFSR(key_candidate, [64, 62, 60, 58, 52, 51, 49, 46, 45, 44, 42, 36, 35, 34, 33, 32, 30, 27, 23, 19, 28 ,16, 14])
        s = [lfsr.getbit() for _ in range(42)]
        matches = sum(a==b for a,b in zip(stream, s))
        if matches >= 180:
            print(key_candidate)
            break