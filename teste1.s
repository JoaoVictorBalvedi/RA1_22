.data
.align 3
const_0: .double 10
const_1: .double 20
const_2: .double 2.0
const_3: .double 3
const_4: .double 12
const_5: .double 1
const_6: .double 99.9
mem_slot: .double 0.0
var_X: .double 0.0
var_Y: .double 0.0
result_0: .double 0.0
result_1: .double 0.0
result_2: .double 0.0
result_3: .double 0.0
result_4: .double 0.0
result_5: .double 0.0
result_6: .double 0.0
result_7: .double 0.0
result_8: .double 0.0
result_9: .double 0.0
result_10: .double 0.0
result_11: .double 0.0
result_12: .double 0.0
result_13: .double 0.0

.text
.global _start
_start:
    @ --- comando 0 ---
    LDR r0, =const_0
    VLDR.F64 d0, [r0]
    LDR r0, =var_X
    VSTR.F64 d0, [r0]
    LDR r0, =result_0
    VSTR.F64 d0, [r0]

    @ --- comando 1 ---
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
    LDR r0, =var_Y
    VSTR.F64 d0, [r0]
    LDR r0, =result_1
    VSTR.F64 d0, [r0]

    @ --- comando 2 ---
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    LDR r0, =result_2
    VSTR.F64 d0, [r0]

    @ --- comando 3 ---
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VSUB.F64 d0, d1, d0
    LDR r0, =result_3
    VSTR.F64 d0, [r0]

    @ --- comando 4 ---
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VMUL.F64 d0, d1, d0
    LDR r0, =result_4
    VSTR.F64 d0, [r0]

    @ --- comando 5 ---
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VDIV.F64 d0, d1, d0
    LDR r0, =result_5
    VSTR.F64 d0, [r0]

    @ --- comando 6 ---
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPOP {d1}
    BL div_int_double
    LDR r0, =result_6
    VSTR.F64 d0, [r0]

    @ --- comando 7 ---
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPOP {d1}
    BL mod_int_double
    LDR r0, =result_7
    VSTR.F64 d0, [r0]

    @ --- comando 8 ---
    LDR r0, =const_2
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    VPOP {d1}
    BL pow_int_double
    LDR r0, =result_8
    VSTR.F64 d0, [r0]

    @ --- comando 9 ---
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VCMPE.F64 d1, d0
    VMRS APSR_nzcv, FPSCR
    BLT cmp_true_1
    MOV r0, #0
    B cmp_end_2
cmp_true_1:
    MOV r0, #1
cmp_end_2:
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    CMP r0, #0
    BEQ if_end_0
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =var_Y
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
if_end_0:
    LDR r0, =result_9
    VSTR.F64 d0, [r0]

    @ --- comando 10 ---
while_start_3:
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VCMPE.F64 d1, d0
    VMRS APSR_nzcv, FPSCR
    BLT cmp_true_5
    MOV r0, #0
    B cmp_end_6
cmp_true_5:
    MOV r0, #1
cmp_end_6:
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    CMP r0, #0
    BEQ while_end_4
    LDR r0, =var_X
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    LDR r0, =var_X
    VSTR.F64 d0, [r0]
    B while_start_3
while_end_4:
    LDR r0, =result_10
    VSTR.F64 d0, [r0]

    @ --- comando 11 ---
    LDR r0, =result_10
    VLDR.F64 d0, [r0]
    LDR r0, =result_11
    VSTR.F64 d0, [r0]

    @ --- comando 12 ---
    LDR r0, =const_6
    VLDR.F64 d0, [r0]
    LDR r0, =mem_slot
    VSTR.F64 d0, [r0]
    LDR r0, =result_12
    VSTR.F64 d0, [r0]

    @ --- comando 13 ---
    LDR r0, =mem_slot
    VLDR.F64 d0, [r0]
    LDR r0, =result_13
    VSTR.F64 d0, [r0]

    @ --- exibe ultimo resultado nos LEDs ---
    LDR r0, =result_13
    VLDR.F64 d0, [r0]
    VCVT.S32.F64 s0, d0
    VMOV r1, s0
    LDR r0, =0xFF200000
    STR r1, [r0]

fim:
    B fim

@ sdiv_software: r1 / r0 -> quociente em r2, resto em r3
sdiv_software:
    MOV r2, #0
sdiv_loop:
    CMP r1, r0
    BLT sdiv_fim
    SUB r1, r1, r0
    ADD r2, r2, #1
    B sdiv_loop
sdiv_fim:
    MOV r3, r1
    BX lr

div_int_double:
    PUSH {lr}
    VCVT.S32.F64 s2, d1
    VCVT.S32.F64 s0, d0
    VMOV r1, s2
    VMOV r0, s0
    BL sdiv_software
    VMOV s0, r2
    VCVT.F64.S32 d0, s0
    POP {lr}
    BX lr

mod_int_double:
    PUSH {lr}
    VCVT.S32.F64 s2, d1
    VCVT.S32.F64 s0, d0
    VMOV r1, s2
    VMOV r0, s0
    BL sdiv_software
    VMOV s0, r3
    VCVT.F64.S32 d0, s0
    POP {lr}
    BX lr

pow_int_double:
    PUSH {lr}
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    VMOV.F64 d2, #1.0
pow_loop:
    CMP r0, #0
    BEQ pow_fim
    VMUL.F64 d2, d2, d1
    SUB r0, r0, #1
    B pow_loop
pow_fim:
    VMOV.F64 d0, d2
    POP {lr}
    BX lr