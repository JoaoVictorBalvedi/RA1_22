# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: RA1 22


def registrarConstante(valor, contexto):
    valor_str = str(valor)
    if valor_str not in contexto["constantes"]:
        rotulo = f"const_{len(contexto['constantes'])}"
        contexto["constantes"][valor_str] = rotulo
    return contexto["constantes"][valor_str]


def registrarVariavel(nome, contexto):
    if nome not in contexto["variaveis"]:
        contexto["variaveis"][nome] = f"var_{nome}"
    return contexto["variaveis"][nome]


def novoRotulo(contexto, prefixo):
    valor = contexto["rotulo"]
    contexto["rotulo"] += 1
    return f"{prefixo}_{valor}"


def gerarCodigoNo(no, contexto):
    tipo = no["tipo"]
    codigo = []

    if tipo == "numero":
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
        indice_alvo = contexto["indice_atual"] - no["indice"]
        if indice_alvo < 0:
            raise ValueError(f"RES({no['indice']}): resultado anterior inexistente")
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
        verdadeiro = novoRotulo(contexto, "cmp_true")
        fim = novoRotulo(contexto, "cmp_end")

        codigo.extend(gerarCodigoNo(no["esquerda"], contexto))
        codigo.append("VPUSH {d0}")
        codigo.extend(gerarCodigoNo(no["direita"], contexto))
        codigo.append("VPOP {d1}")
        codigo.append("VCMPE.F64 d1, d0")
        codigo.append("VMRS APSR_nzcv, FPSCR")

        salto = {
            ">": "BGT",
            "<": "BLT",
            ">=": "BGE",
            "<=": "BLE",
            "==": "BEQ",
            "!=": "BNE",
        }[no["operador"]]

        codigo.append(f"{salto} {verdadeiro}")
        codigo.append("MOV r0, #0")
        codigo.append(f"B {fim}")
        codigo.append(f"{verdadeiro}:")
        codigo.append("MOV r0, #1")
        codigo.append(f"{fim}:")
        codigo.append("VMOV s0, r0")
        codigo.append("VCVT.F64.S32 d0, s0")

    elif tipo == "if":
        fim = novoRotulo(contexto, "if_end")
        codigo.extend(gerarCodigoNo(no["condicao"], contexto))
        codigo.append("VCVT.S32.F64 s0, d0")
        codigo.append("VMOV r0, s0")
        codigo.append("CMP r0, #0")
        codigo.append(f"BEQ {fim}")
        codigo.extend(gerarCodigoNo(no["comando"], contexto))
        codigo.append(f"{fim}:")

    elif tipo == "while":
        inicio = novoRotulo(contexto, "while_start")
        fim = novoRotulo(contexto, "while_end")
        codigo.append(f"{inicio}:")
        codigo.extend(gerarCodigoNo(no["condicao"], contexto))
        codigo.append("VCVT.S32.F64 s0, d0")
        codigo.append("VMOV r0, s0")
        codigo.append("CMP r0, #0")
        codigo.append(f"BEQ {fim}")
        codigo.extend(gerarCodigoNo(no["comando"], contexto))
        codigo.append(f"B {inicio}")
        codigo.append(f"{fim}:")

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


def gerarAssembly(arvore):
    comandos = arvore["comandos"] if arvore["tipo"] == "programa" else arvore
    contexto = {
        "constantes": {},
        "variaveis": {},
        "usa_div_int": False,
        "usa_mod_int": False,
        "usa_pow_int": False,
        "indice_atual": 0,
        "rotulo": 0,
    }

    corpo = []
    for i, comando in enumerate(comandos):
        contexto["indice_atual"] = i
        corpo.append(f"    @ --- comando {i} ---")
        linhas = gerarCodigoNo(comando, contexto)
        corpo.extend("    " + linha if not linha.endswith(":") else linha for linha in linhas)
        corpo.append(f"    LDR r0, =result_{i}")
        corpo.append("    VSTR.F64 d0, [r0]")
        corpo.append("")

    if comandos:
        corpo.append("    @ --- exibe ultimo resultado nos LEDs ---")
        corpo.append(f"    LDR r0, =result_{len(comandos) - 1}")
        corpo.append("    VLDR.F64 d0, [r0]")
        corpo.append("    VCVT.S32.F64 s0, d0")
        corpo.append("    VMOV r1, s0")
        corpo.append("    LDR r0, =0xFF200000")
        corpo.append("    STR r1, [r0]")
        corpo.append("")

    linhas_data = [".data", ".align 3"]
    for valor, rotulo in contexto["constantes"].items():
        linhas_data.append(f"{rotulo}: .double {valor}")

    linhas_data.append("mem_slot: .double 0.0")

    for _, rotulo in contexto["variaveis"].items():
        linhas_data.append(f"{rotulo}: .double 0.0")

    for i in range(len(comandos)):
        linhas_data.append(f"result_{i}: .double 0.0")

    linhas_text = ["", ".text", ".global _start", "_start:"]
    linhas_text.extend(corpo)
    linhas_text.extend(["fim:", "    B fim"])
    linhas_text.extend(gerarRotinasAuxiliares(contexto))

    return "\n".join(linhas_data + linhas_text)
