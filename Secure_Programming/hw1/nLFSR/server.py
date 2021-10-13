#!/bin/env python3 -u
import os

def bitlist(state):
    num = state
    list = []
    for i in range(64):
        if num & 1 == 1:
            list.append(1)
        else:
            list.append(0)
        num >>= 1
    return list

state = int.from_bytes(os.urandom(8), 'little')
state_list = bitlist(state)
poly = 0xaa0d3a677e1be0bf   # 1010101000001101001110100110011101111110000110111110000010111111
stream = []
def step():
    global state
    out = state & 1
    state >>= 1
    if out:
        state ^= poly
    return out
    

def random():
    for _ in range(42):
        step()
    return step()

for _ in range(64):
    y = random()
    x = int(1)
    if x == y:
        stream.append(1)
    else:
        stream.append(0)

key_len = 64

poly = [0] * 64

polylist = [61, 59, 57, 51, 50, 48, 45, 44, 43, 41, 38, 37, 34, 33, 32, 30, 29, 28, 27, 26, 25, 20, 19, 17, 16, 15, 14, 13, 7, 5, 4, 3, 2, 1, 0]

def clock(count):
    b = count[0]
    for i in range(63):
        count[i] = count[i+1]
    count[63] = b
    for i in range(len(polylist)):
        count[polylist[i]] ^= b
    return b

count = [0] * 64

for i in range(64):
    count[i] = 2**i
for i in range(64):
    for _ in range(42):
        clock(count)
    poly[i] = clock(count)


key = [0] * key_len
s = []
# compare_key(key, poly, diff, diff_len, stream, 0)

tempt = [0] * 64
tempt_stream = [0] * 64
sign = 0
sign_stream = 0
for i in range(64):
    tempt[i] = poly[i]
    tempt_stream[i] = stream[i]
for i in range(63):
    k = 0
    for j in range(64-i):
        if tempt[j] % 2**(i+1) != 0:
            if k == 0:
                sign = tempt[j]
                sign_stream = tempt_stream[j]
                k = 1
            else:
                tempt[j-1] = sign ^ tempt[j]
                tempt_stream[j-1] = sign_stream ^ tempt_stream[j]
        elif k == 1:
            tempt[j-1] = tempt[j]
            tempt_stream[j-1] = tempt_stream[j]
        else:
            tempt[j] = tempt[j]
            tempt_stream[j] = tempt_stream[j]
print(bin(tempt[0]))
key[63] = tempt_stream[0]

for a in range(63):
    sign = 0
    sign_stream = 0
    for i in range(64):
        tempt[i] = poly[i]
        tempt_stream[i] = stream[i]
    for i in range(63-a):
        k = 0
        for j in range(64-i):
            if tempt[j] % 2**(i+1) != 0:
                if k == 0:
                    sign = tempt[j]
                    sign_stream = tempt_stream[j]
                    k = 1
                else:
                    tempt[j-1] = sign ^ tempt[j]
                    tempt_stream[j-1] = sign_stream ^ tempt_stream[j]
            elif k == 1:
                tempt[j-1] = tempt[j]
                tempt_stream[j-1] = tempt_stream[j]
            else:
                tempt[j] = tempt[j]
                tempt_stream[j] = tempt_stream[j]
    for i in range(a+1):
        if sign & 2**(63-i) != 0:
            if i == 0:
                print(bin(sign))
                print(sign_stream)
            sign ^= 2**(63-i)
            sign_stream ^= key[63-i]
            if i == 0:
                print(sign_stream)
    print(bin(sign) + str(62 - a))
    key[62 - a] = sign_stream

print(state_list)
print(key)


# money = 1.2
# while money > 0:
#     y = random()
#     x = int(input('> '))
#     if x == y:
#         money += 0.02
#     else:
#         money -= 0.04
#     print(money)
#     if money > 2.4:
#         print("Here's your flag:")
#         with open('./flag.txt') as f:
#             print(f.read())
#         exit(0)
# print('E( G_G)')
