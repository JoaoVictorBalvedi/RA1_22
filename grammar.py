# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

"""Gramatica LL(1), FIRST, FOLLOW e tabela de analise.

Observacao importante:
A linguagem usa RPN e tudo comeca por LPAREN, entao a implementacao do parser
usa um pequeno lookahead interno apos LPAREN para distinguir START, END,
expressao, IF e WHILE. A tabela abaixo documenta a gramatica usada.
"""

EPSILON = "ε"
EOF = "EOF"


def construirGramatica():
    return {
        "programa": [["inicio", "lista_comandos", "fim", "EOF"]],
        "inicio": [["START_STMT"]],
        "fim": [["END_STMT"]],
        "lista_comandos": [["comando", "lista_comandos"], [EPSILON]],
        "comando": [["expressao"], ["decisao"], ["laco"]],
        "expressao": [["LPAREN", "conteudo_expr", "RPAREN"]],
        "conteudo_expr": [
            ["operando"],
            ["operando", "MEM"],
            ["operando", "RES"],
            ["operando", "IDENTIFIER"],
            ["operando", "operando", "OPERATOR"],
            ["operando", "operando", "REL_OPERATOR"],
        ],
        "operando": [["NUMBER"], ["IDENTIFIER"], ["MEM"], ["expressao"]],
        "decisao": [["LPAREN", "expressao", "bloco", "IF", "RPAREN"]],
        "laco": [["LPAREN", "expressao", "bloco", "WHILE", "RPAREN"]],
        "bloco": [["LPAREN", "lista_comandos", "RPAREN"]],
    }


def eh_terminal(simbolo, gramatica):
    return simbolo not in gramatica and simbolo != EPSILON


def calcularFirst(gramatica):
    first = {nt: set() for nt in gramatica}

    mudou = True
    while mudou:
        mudou = False
        for nt, producoes in gramatica.items():
            for producao in producoes:
                if producao == [EPSILON]:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        mudou = True
                    continue

                adiciona_epsilon = True
                for simbolo in producao:
                    if eh_terminal(simbolo, gramatica):
                        if simbolo not in first[nt]:
                            first[nt].add(simbolo)
                            mudou = True
                        adiciona_epsilon = False
                        break

                    antes = len(first[nt])
                    first[nt].update(first[simbolo] - {EPSILON})
                    if len(first[nt]) != antes:
                        mudou = True

                    if EPSILON not in first[simbolo]:
                        adiciona_epsilon = False
                        break

                if adiciona_epsilon:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        mudou = True
    return first


def firstDaSequencia(sequencia, first, gramatica):
    resultado = set()

    if not sequencia or sequencia == [EPSILON]:
        return {EPSILON}

    for simbolo in sequencia:
        if eh_terminal(simbolo, gramatica):
            resultado.add(simbolo)
            return resultado

        resultado.update(first[simbolo] - {EPSILON})
        if EPSILON not in first[simbolo]:
            return resultado

    resultado.add(EPSILON)
    return resultado


def calcularFollow(gramatica, first):
    follow = {nt: set() for nt in gramatica}
    follow["programa"].add(EOF)

    mudou = True
    while mudou:
        mudou = False
        for nt, producoes in gramatica.items():
            for producao in producoes:
                for i, simbolo in enumerate(producao):
                    if simbolo not in gramatica:
                        continue

                    beta = producao[i + 1:]
                    first_beta = firstDaSequencia(beta, first, gramatica)

                    antes = len(follow[simbolo])
                    follow[simbolo].update(first_beta - {EPSILON})
                    if EPSILON in first_beta or not beta:
                        follow[simbolo].update(follow[nt])

                    if len(follow[simbolo]) != antes:
                        mudou = True

    return follow


def construirTabelaLl1(gramatica, first, follow):
    tabela = {}
    conflitos = []

    for nt, producoes in gramatica.items():
        for producao in producoes:
            first_prod = firstDaSequencia(producao, first, gramatica)

            for terminal in first_prod - {EPSILON}:
                chave = (nt, terminal)
                if chave in tabela and tabela[chave] != producao:
                    conflitos.append((chave, tabela[chave], producao))
                tabela[chave] = producao

            if EPSILON in first_prod:
                for terminal in follow[nt]:
                    chave = (nt, terminal)
                    if chave in tabela and tabela[chave] != producao:
                        conflitos.append((chave, tabela[chave], producao))
                    tabela[chave] = producao

    return tabela, conflitos


def construirResumoGramatica():
    gramatica = construirGramatica()
    first = calcularFirst(gramatica)
    follow = calcularFollow(gramatica, first)
    tabela, conflitos = construirTabelaLl1(gramatica, first, follow)
    return {
        "gramatica": gramatica,
        "first": {k: sorted(v) for k, v in first.items()},
        "follow": {k: sorted(v) for k, v in follow.items()},
        "tabela": {f"{nt}, {terminal}": prod for (nt, terminal), prod in tabela.items()},
        "conflitos": conflitos,
    }
