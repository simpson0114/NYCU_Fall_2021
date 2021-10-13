import random
import json
import functools as fn
import numpy as np
import string
import hashlib

charset = string.ascii_lowercase+string.digits+',. '
charset_idmap = {e: i for i, e in enumerate(charset)}

ksz = 80

def decrypt(ctx, key):
    N, ksz = len(charset), len(key)
    return ''.join(charset[(c-key[i % ksz]) % N] for i, c in enumerate(ctx))

def toPrintable(data):
    ul = ord('_')
    data = bytes(c if 32 <= c < 127 else ul for c in data)
    return data.decode('ascii')

with open('./output.txt') as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])
ctx = [charset_idmap[c] for c in ctx]

with open('./ngrams.json') as f:
    ngrams = json.load(f)

@fn.lru_cache(10000)
def get_trigram(x):
    x = ''.join(x)
    y = ngrams.get(x)
    if y is not None:
        return y
    ys = []
    a, b = ngrams.get(x[:2]), ngrams.get(x[2:])
    if a is not None and b is not None:
        ys.append(a+b)
    a, b = ngrams.get(x[:1]), ngrams.get(x[1:])
    if a is not None and b is not None:
        ys.append(a+b)
    if len(ys):
        return max(ys)
    if any(c not in ngrams for c in x):
        return -25
    return sum(map(ngrams.get, x))

@fn.lru_cache(10000)
def fitness(a): # 對於 key 的機率去評分
    plain = decrypt(ctx, a)
    tgs = zip(plain, plain[1:], plain[2:])
    score = sum(get_trigram(tg) for tg in tgs)
    return score

def initialize(size): # 生成一堆隨機的 key
    population = []
    for i in range(size):
        key = tuple(random.randrange(len(charset)) for _ in range(ksz))
        population.append(key)
    return population

def crossover(a, b, prob):  # 對於高分數的 key 去生成另外的 key
    r = list(a)
    for i in range(len(r)):
        if random.random() < prob:
            r[i] = b[i]
    return tuple(r)

def mutate(a):  # 突變 挑 key 中的其中一個字變為其他 key
    r = list(a)
    i = random.randrange(len(a))
    r[i] = random.randrange(len(charset))
    return tuple(r)

keys = np.array(initialize(7000))
scores = np.array([])
for i in keys:
    scores = np.append(scores, fitness(tuple(i)))

# 分數較高的前600個 key
keys = keys[scores.argsort()[::-1]][:600]

# 讓 600 個 key 一直生出下一代的 key 
for m in range(2000):
    np.random.shuffle(keys)
    for i in range(len(keys)//2):
        child = np.array(crossover(keys[i*2], keys[i*2+1], 0.7))
        keys = np.concatenate((keys, [child]))
    np.random.shuffle(keys)
    for i in range(len(keys)//2):
        keys[i] = mutate(keys[i])
    scores = np.array([])
    for i in keys:
        scores = np.append(scores, fitness(tuple(i)))
    keys = keys[scores.argsort()[::-1]][:600]
    scores = scores[scores.argsort()[::-1]][:600]
    print(m, int(scores[0]), decrypt(ctx, keys[0]))

k = hashlib.sha512(''.join(charset[k] for k in keys[0]).encode('ascii')).digest()
enc = bytes(ci ^ ki for ci, ki in zip(enc.ljust(len(k), b'\0'), k))
print('enc =', enc)
