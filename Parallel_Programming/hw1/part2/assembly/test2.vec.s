	.text
	.file	"test2.cpp"
	.globl	_Z5test2PfS_S_i         # -- Begin function _Z5test2PfS_S_i
	.p2align	4, 0x90
	.type	_Z5test2PfS_S_i,@function
_Z5test2PfS_S_i:                        # @_Z5test2PfS_S_i
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r14
	.cfi_def_cfa_offset 24
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	.cfi_offset %rbp, -16
	movq	%rdx, %r14
	movq	%rdi, %rbx
	movl	$20000000, %ebp         # imm = 0x1312D00
	.p2align	4, 0x90
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	movl	$4096, %edx             # imm = 0x1000
	movq	%r14, %rdi
	movq	%rbx, %rsi
	callq	memcpy
	movl	$4096, %edx             # imm = 0x1000
	movq	%r14, %rdi
	movq	%rbx, %rsi
	callq	memcpy
	movl	$4096, %edx             # imm = 0x1000
	movq	%r14, %rdi
	movq	%rbx, %rsi
	callq	memcpy
	movl	$4096, %edx             # imm = 0x1000
	movq	%r14, %rdi
	movq	%rbx, %rsi
	callq	memcpy
	movl	$4096, %edx             # imm = 0x1000
	movq	%r14, %rdi
	movq	%rbx, %rsi
	callq	memcpy
	addl	$-5, %ebp
	jne	.LBB0_1
# %bb.2:
	popq	%rbx
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	_Z5test2PfS_S_i, .Lfunc_end0-_Z5test2PfS_S_i
	.cfi_endproc
                                        # -- End function
	.section	.text.startup,"ax",@progbits
	.p2align	4, 0x90         # -- Begin function _GLOBAL__sub_I_test2.cpp
	.type	_GLOBAL__sub_I_test2.cpp,@function
_GLOBAL__sub_I_test2.cpp:               # @_GLOBAL__sub_I_test2.cpp
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$_ZStL8__ioinit, %edi
	callq	_ZNSt8ios_base4InitC1Ev
	movl	$_ZNSt8ios_base4InitD1Ev, %edi
	movl	$_ZStL8__ioinit, %esi
	movl	$__dso_handle, %edx
	popq	%rax
	.cfi_def_cfa_offset 8
	jmp	__cxa_atexit            # TAILCALL
.Lfunc_end1:
	.size	_GLOBAL__sub_I_test2.cpp, .Lfunc_end1-_GLOBAL__sub_I_test2.cpp
	.cfi_endproc
                                        # -- End function
	.type	_ZStL8__ioinit,@object  # @_ZStL8__ioinit
	.local	_ZStL8__ioinit
	.comm	_ZStL8__ioinit,1,1
	.hidden	__dso_handle
	.section	.init_array,"aw",@init_array
	.p2align	3
	.quad	_GLOBAL__sub_I_test2.cpp
	.ident	"clang version 10.0.0-4ubuntu1 "
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym _GLOBAL__sub_I_test2.cpp
	.addrsig_sym _ZStL8__ioinit
	.addrsig_sym __dso_handle
