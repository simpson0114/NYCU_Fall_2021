#!/usr/bin/env python3
import cv2      #https://pypi.org/project/opencv-python/
import random
import string

charset = string.ascii_letters + string.digits + '+='
fire, water, earth, air = [random.choice(charset) for _ in range(4)]

def combine(a, b):
    return ''.join([a,b])

def dencrypt(arr1, arr2):
    
    h, w = arr1.shape
    for i in range(h):
        for j in range(w):
            arr1[i][j] ^= arr2[i][j]

msg1 = cv2.imread('flag_enc.png', cv2.IMREAD_GRAYSCALE)
msg2 = cv2.imread('golem_enc.png', cv2.IMREAD_GRAYSCALE)
dencrypt(msg1, msg2)
cv2.imwrite('flag.png', msg1)

