poly = [61, 59, 57, 51, 50, 48, 45, 44, 43, 41, 38, 37, 34, 33, 32, 30, 29, 28, 27, 26, 25, 20, 19, 17, 16, 15, 14, 13, 7, 5, 4, 3, 2, 1, 0]

def clock(count):
    b = count[0]
    for i in range(63):
        count[i] = count[i+1]
    count[63] = b
    for i in range(len(poly)):
        count[poly[i]] ^= b
    return count

count = [0] * 64

for i in range(64):
    count[i] = 2**i
for i in range(64):
    print('poly' + str(i+1) + ' = [', end = '')
    for i in range(42):
        count = clock(count)
        # print(count[0])
    a = count[0]
    for i in range(64):
        if a == 1:
            print(i, end = ']')
        elif a & 1 == 1:
            print(i, end = ', ')
        a >>= 1     
    print() 
    count = clock(count)