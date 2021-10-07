	.text
	.file	"test2.cpp"
	.globl	_Z5test2PfS_S_i         # -- Begin function _Z5test2PfS_S_i
	.p2align	4, 0x90
	.type	_Z5test2PfS_S_i,@function
_Z5test2PfS_S_i:                        # @_Z5test2PfS_S_i
	.cfi_startproc
# %bb.0:
	xorl	%r8d, %r8d
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_7:                                #   in Loop: Header=BB0_1 Depth=1
	addl	$1, %r8d
	cmpl	$20000000, %r8d         # imm = 0x1312D00
	je	.LBB0_8
.LBB0_1:                                # =>This Loop Header: Depth=1
                                        #     Child Loop BB0_2 Depth 2
	xorl	%ecx, %ecx
	jmp	.LBB0_2
	.p2align	4, 0x90
.LBB0_6:                                #   in Loop: Header=BB0_2 Depth=2
	addq	$2, %rcx
	cmpq	$1024, %rcx             # imm = 0x400
	je	.LBB0_7
.LBB0_2:                                #   Parent Loop BB0_1 Depth=1
                                        # =>  This Inner Loop Header: Depth=2
	movl	(%rdi,%rcx,4), %eax
	movl	%eax, (%rdx,%rcx,4)
	movss	(%rsi,%rcx,4), %xmm0    # xmm0 = mem[0],zero,zero,zero
	movd	%eax, %xmm1
	ucomiss	%xmm1, %xmm0
	jbe	.LBB0_4
# %bb.3:                                #   in Loop: Header=BB0_2 Depth=2
	movss	%xmm0, (%rdx,%rcx,4)
.LBB0_4:                                #   in Loop: Header=BB0_2 Depth=2
	movl	4(%rdi,%rcx,4), %eax
	movl	%eax, 4(%rdx,%rcx,4)
	movss	4(%rsi,%rcx,4), %xmm0   # xmm0 = mem[0],zero,zero,zero
	movd	%eax, %xmm1
	ucomiss	%xmm1, %xmm0
	jbe	.LBB0_6
# %bb.5:                                #   in Loop: Header=BB0_2 Depth=2
	movss	%xmm0, 4(%rdx,%rcx,4)
	jmp	.LBB0_6
.LBB0_8:
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
