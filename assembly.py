# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

"""Gerador de Assembly ARMv7 DE1-SOC a partir da AST."""


def registrarConstante(valor, contexto):
    if valor not in contexto["constantes"]:
        rotulo = f"const_{len(contexto['constantes'])}"
        contexto["constantes"][valor] = rotulo
    return contexto["constantes"][valor]


def registrarVariavel(nome, contexto):
    if nome not in contexto["variaveis"]:
        contexto["variaveis"][nome] = f"var_{nome}"
    return contexto["variaveis"][nome]


def novoLabel(contexto, prefixo):
    label = f"{prefixo}_{contexto['label_id']}"
    contexto["label_id"] += 1
    return label


def gerarCodigoNo(no, contexto):
    tipo = no["tipo"]
    codigo = []

    if tipo == "programa":
        for comando in no["comandos"]:
            codigo.extend(gerarCodigoNo(comando, contexto))
            codigo.append(f"LDR r0, =result_{contexto['indice_resultado']}")
            codigo.append("VSTR.F64 d0, [r0]")
            codigo.append("")
            contexto["indice_resultado"] += 1

    elif tipo == "numero":
        rotulo = registrarConstante(no["valor"], contexto)
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "mem_leitura":
        codigo.append("LDR r0, =mem_slot")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "mem_escrita":
        codigo.extend(gerarCodigoNo(no["valor"], contexto))
        codigo.append("LDR r0, =mem_slot")
        codigo.append("VSTR.F64 d0, [r0]")

    elif tipo == "res":
        indice_alvo = contexto["indice_resultado"] - no["indice"]
        if indice_alvo < 0:
            raise ValueError(f"RES({no['indice']}): nao ha resultado anterior suficiente")
        codigo.append(f"LDR r0, =result_{indice_alvo}")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "var_leitura":
        rotulo = registrarVariavel(no["nome"], contexto)
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "var_escrita":
        rotulo = registrarVariavel(no["nome"], contexto)
        codigo.extend(gerarCodigoNo(no["valor"], contexto))
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VSTR.F64 d0, [r0]")

    elif tipo == "operacao":
        codigo.extend(gerarCodigoNo(no["esquerda"], contexto))
        codigo.append("VPUSH {d0}")
        codigo.extend(gerarCodigoNo(no["direita"], contexto))
        codigo.append("VPOP {d1}")

        operador = no["operador"]
        if operador == "+":
            codigo.append("VADD.F64 d0, d1, d0")
        elif operador == "-":
            codigo.append("VSUB.F64 d0, d1, d0")
        elif operador == "*":
            codigo.append("VMUL.F64 d0, d1, d0")
        elif operador == "|":
            codigo.append("VDIV.F64 d0, d1, d0")
        elif operador == "/":
            contexto["usa_div_int"] = True
            codigo.append("BL div_int_double")
        elif operador == "%":
            contexto["usa_mod_int"] = True
            codigo.append("BL mod_int_double")
        elif operador == "^":
            contexto["usa_pow_int"] = True
            codigo.append("BL pow_int_double")
        else:
            raise ValueError(f"Operador desconhecido: {operador}")

    elif tipo == "comparacao":
        # Resultado: d0 = 1.0 se verdadeiro, 0.0 se falso.
        label_true = novoLabel(contexto, "cmp_true")
        label_end = novoLabel(contexto, "cmp_end")

        codigo.extend(gerarCodigoNo(no["esquerda"], contexto))
        codigo.append("VPUSH {d0}")
        codigo.extend(gerarCodigoNo(no["direita"], contexto))
        codigo.append("VPOP {d1}")
        codigo.append("VCMP.F64 d1, d0")
        codigo.append("VMRS APSR_nzcv, FPSCR")

        op = no["operador"]
        mapa = {
            ">": "BGT",
            "<": "BLT",
            ">=": "BGE",
            "<=": "BLE",
            "==": "BEQ",
            "!=": "BNE",
        }
        if op not in mapa:
            raise ValueError(f"Operador relacional desconhecido: {op}")

        codigo.append(f"{mapa[op]} {label_true}")
        codigo.append("LDR r0, =const_false")
        codigo.append("VLDR.F64 d0, [r0]")
        codigo.append(f"B {label_end}")
        codigo.append(f"{label_true}:")
        codigo.append("LDR r0, =const_true")
        codigo.append("VLDR.F64 d0, [r0]")
        codigo.append(f"{label_end}:")

    elif tipo == "if":
        label_fim = novoLabel(contexto, "if_fim")
        codigo.extend(gerarCodigoNo(no["condicao"], contexto))
        codigo.append("VCMP.F64 d0, #0")
        codigo.append("VMRS APSR_nzcv, FPSCR")
        codigo.append(f"BEQ {label_fim}")
        for comando in no["corpo"]:
            codigo.extend(gerarCodigoNo(comando, contexto))
            codigo.append("")
        codigo.append(f"{label_fim}:")

    elif tipo == "while":
        label_inicio = novoLabel(contexto, "while_inicio")
        label_fim = novoLabel(contexto, "while_fim")
        codigo.append(f"{label_inicio}:")
        codigo.extend(gerarCodigoNo(no["condicao"], contexto))
        codigo.append("VCMP.F64 d0, #0")
        codigo.append("VMRS APSR_nzcv, FPSCR")
        codigo.append(f"BEQ {label_fim}")
        for comando in no["corpo"]:
            codigo.extend(gerarCodigoNo(comando, contexto))
            codigo.append("")
        codigo.append(f"B {label_inicio}")
        codigo.append(f"{label_fim}:")

    else:
        raise ValueError(f"Tipo de no desconhecido: {tipo}")

    return codigo


def gerarRotinasAuxiliares(contexto):
    rotinas = []

    if contexto["usa_div_int"] or contexto["usa_mod_int"]:
        rotinas.extend([
            "",
            "@ sdiv_software: r1 / r0 -> quociente em r2, resto em r3",
            "sdiv_software:",
            "    MOV r2, #0",
            "sdiv_loop:",
            "    CMP r1, r0",
            "    BLT sdiv_fim",
            "    SUB r1, r1, r0",
            "    ADD r2, r2, #1",
            "    B sdiv_loop",
            "sdiv_fim:",
            "    MOV r3, r1",
            "    BX lr",
        ])

    if contexto["usa_div_int"]:
        rotinas.extend([
            "",
            "div_int_double:",
            "    PUSH {lr}",
            "    VCVT.S32.F64 s2, d1",
            "    VCVT.S32.F64 s0, d0",
            "    VMOV r1, s2",
            "    VMOV r0, s0",
            "    BL sdiv_software",
            "    VMOV s0, r2",
            "    VCVT.F64.S32 d0, s0",
            "    POP {lr}",
            "    BX lr",
        ])

    if contexto["usa_mod_int"]:
        rotinas.extend([
            "",
            "mod_int_double:",
            "    PUSH {lr}",
            "    VCVT.S32.F64 s2, d1",
            "    VCVT.S32.F64 s0, d0",
            "    VMOV r1, s2",
            "    VMOV r0, s0",
            "    BL sdiv_software",
            "    VMOV s0, r3",
            "    VCVT.F64.S32 d0, s0",
            "    POP {lr}",
            "    BX lr",
        ])

    if contexto["usa_pow_int"]:
        rotinas.extend([
            "",
            "pow_int_double:",
            "    PUSH {lr}",
            "    VCVT.S32.F64 s0, d0",
            "    VMOV r0, s0",
            "    VMOV.F64 d2, #1.0",
            "pow_loop:",
            "    CMP r0, #0",
            "    BEQ pow_fim",
            "    VMUL.F64 d2, d2, d1",
            "    SUB r0, r0, #1",
            "    B pow_loop",
            "pow_fim:",
            "    VMOV.F64 d0, d2",
            "    POP {lr}",
            "    BX lr",
        ])

    return rotinas


def contar_comandos_top_level(arvore):
    return len(arvore.get("comandos", []))


def gerarAssembly(arvore):
    contexto = {
        "constantes": {},
        "variaveis": {},
        "usa_div_int": False,
        "usa_mod_int": False,
        "usa_pow_int": False,
        "indice_resultado": 0,
        "label_id": 0,
    }

    corpo = gerarCodigoNo(arvore, contexto)

    total = max(1, contexto["indice_resultado"])
    corpo.append("@ --- exibe ultimo resultado nos LEDs ---")
    corpo.append(f"LDR r0, =result_{total - 1}")
    corpo.append("VLDR.F64 d0, [r0]")
    corpo.append("VCVT.S32.F64 s0, d0")
    corpo.append("VMOV r1, s0")
    corpo.append("LDR r0, =0xFF200000")
    corpo.append("STR r1, [r0]")
    corpo.append("")

    linhas_data = [".data", ".align 3"]
    linhas_data.append("const_true: .double 1.0")
    linhas_data.append("const_false: .double 0.0")

    for valor, rotulo in contexto["constantes"].items():
        linhas_data.append(f"{rotulo}: .double {valor}")

    linhas_data.append("mem_slot: .double 0.0")

    for _, rotulo in contexto["variaveis"].items():
        linhas_data.append(f"{rotulo}: .double 0.0")

    for i in range(total):
        linhas_data.append(f"result_{i}: .double 0.0")

    linhas_text = [".text", ".global _start", "_start:"]
    linhas_text.extend("    " + linha if linha and not linha.endswith(":") and not linha.startswith("@") else linha for linha in corpo)
    linhas_text.extend(["fim:", "    B fim"])
    linhas_text.extend(gerarRotinasAuxiliares(contexto))

    return "\n".join(linhas_data + [""] + linhas_text)
