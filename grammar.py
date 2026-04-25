# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: RA1 22

EPSILON = "ε"
EOF = "EOF"


TERMINAIS = {
    "START_LINE",
    "END_LINE",
    "LPAREN",
    "RPAREN",
    "NUMBER",
    "IDENT_ELEM",
    "IDENT_REST",
    "IDENT_ASSIGN",
    "MEM_ELEM",
    "MEM_REST",
    "MEM_ASSIGN",
    "RES",
    "IF",
    "WHILE",
    "OPERATOR",
    "REL_OPERATOR",
    "EOF",
}


def construirGramatica():
    # Gramatica fatorada para documentacao e construcao da tabela LL(1).
    # A implementacao do parser usa as mesmas decisoes por lookahead.
    return {
        "programa": [["inicio", "lista_comandos", "fim", "EOF"]],
        "inicio": [["START_LINE"]],
        "fim": [["END_LINE"]],
        "lista_comandos": [["comando", "lista_comandos"], [EPSILON]],
        "comando": [["estrutura"]],
        "estrutura": [["LPAREN", "elemento", "resto"]],
        "elemento": [["NUMBER"], ["IDENT_ELEM"], ["MEM_ELEM"], ["estrutura"]],
        "resto": [
            ["RPAREN"],
            ["RES", "RPAREN"],
            ["MEM_ASSIGN", "RPAREN"],
            ["IDENT_ASSIGN", "RPAREN"],
            ["elemento2", "operador_final", "RPAREN"],
        ],
        "operador_final": [["OPERATOR"], ["REL_OPERATOR"], ["IF"], ["WHILE"]],
        "elemento2": [["NUMBER"], ["IDENT_REST"], ["MEM_REST"], ["estrutura"]],
    }


def _eh_terminal(simbolo):
    return simbolo in TERMINAIS or simbolo == EPSILON


def calcularFirst(gramatica):
    first = {nao_terminal: set() for nao_terminal in gramatica}

    mudou = True
    while mudou:
        mudou = False

        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                if producao == [EPSILON]:
                    if EPSILON not in first[nao_terminal]:
                        first[nao_terminal].add(EPSILON)
                        mudou = True
                    continue

                todos_aceitam_epsilon = True
                for simbolo in producao:
                    if simbolo == EPSILON:
                        conjunto = {EPSILON}
                    elif _eh_terminal(simbolo):
                        conjunto = {simbolo}
                    else:
                        conjunto = first[simbolo]

                    antes = len(first[nao_terminal])
                    first[nao_terminal].update(conjunto - {EPSILON})
                    if len(first[nao_terminal]) != antes:
                        mudou = True

                    if EPSILON not in conjunto:
                        todos_aceitam_epsilon = False
                        break

                if todos_aceitam_epsilon and EPSILON not in first[nao_terminal]:
                    first[nao_terminal].add(EPSILON)
                    mudou = True

    return first


def firstDaSequencia(sequencia, first):
    resultado = set()

    if not sequencia or sequencia == [EPSILON]:
        return {EPSILON}

    for simbolo in sequencia:
        if simbolo == EPSILON:
            conjunto = {EPSILON}
        elif _eh_terminal(simbolo):
            conjunto = {simbolo}
        else:
            conjunto = first[simbolo]

        resultado.update(conjunto - {EPSILON})

        if EPSILON not in conjunto:
            return resultado

    resultado.add(EPSILON)
    return resultado


def calcularFollow(gramatica, first):
    follow = {nao_terminal: set() for nao_terminal in gramatica}
    follow["programa"].add(EOF)

    mudou = True
    while mudou:
        mudou = False

        for origem, producoes in gramatica.items():
            for producao in producoes:
                for indice, simbolo in enumerate(producao):
                    if simbolo not in gramatica:
                        continue

                    beta = producao[indice + 1:]
                    first_beta = firstDaSequencia(beta, first)

                    antes = len(follow[simbolo])
                    follow[simbolo].update(first_beta - {EPSILON})

                    if EPSILON in first_beta or not beta:
                        follow[simbolo].update(follow[origem])

                    if len(follow[simbolo]) != antes:
                        mudou = True

    return follow


def construirTabelaLl1(gramatica, first, follow):
    tabela = {}
    conflitos = []

    for nao_terminal, producoes in gramatica.items():
        tabela[nao_terminal] = {}
        for producao in producoes:
            first_producao = firstDaSequencia(producao, first)

            for terminal in first_producao - {EPSILON}:
                existente = tabela[nao_terminal].get(terminal)
                if existente is None:
                    tabela[nao_terminal][terminal] = producao
                elif existente != producao:
                    conflitos.append(
                        f"Conflito em ({nao_terminal}, {terminal}): {existente} vs {producao}"
                    )

            if EPSILON in first_producao:
                for terminal in follow[nao_terminal]:
                    existente = tabela[nao_terminal].get(terminal)
                    if existente is None:
                        tabela[nao_terminal][terminal] = producao
                    elif existente != producao:
                        conflitos.append(
                            f"Conflito em ({nao_terminal}, {terminal}): {existente} vs {producao}"
                        )

    return tabela, conflitos


def construirTudoLl1():
    gramatica = construirGramatica()
    first = calcularFirst(gramatica)
    follow = calcularFollow(gramatica, first)
    tabela, conflitos = construirTabelaLl1(gramatica, first, follow)
    return {
        "gramatica": gramatica,
        "first": first,
        "follow": follow,
        "tabela": tabela,
        "conflitos": conflitos,
    }
