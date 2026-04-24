# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

"""Analisador lexico da Fase 2.

Le codigo-fonte da linguagem RPN e gera uma lista de tokens.
Mantem a base da Fase 1, mas adicionando START, END, IF, WHILE,
operadores relacionais e ajusta os operadores conforme o enunciado:
| = divisao real, / = divisao inteira.
"""

from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int

    def as_tuple(self):
        return (self.tipo, self.valor)

    def __repr__(self):
        return f"Token({self.tipo!r}, {self.valor!r}, linha={self.linha}, coluna={self.coluna})"


PALAVRAS_RESERVADAS = {
    "START": "START",
    "END": "END",
    "MEM": "MEM",
    "RES": "RES",
    "IF": "IF",
    "WHILE": "WHILE",
}

OPERADORES_ARITMETICOS = {"+", "-", "*", "|", "/", "%", "^"}
OPERADORES_RELACIONAIS_1 = {">", "<"}
OPERADORES_RELACIONAIS_2 = {">=", "<=", "==", "!="}


def fim_de_token(c):
    return c is None or c.isspace() or c in "()"


def ler_numero(linha_texto, i, num_linha):
    inicio = i
    estado = "inteiro"

    while i < len(linha_texto):
        c = linha_texto[i]

        if estado == "inteiro":
            if c.isdigit():
                i += 1
            elif c == ".":
                estado = "decimal_obrigatorio"
                i += 1
            else:
                break

        elif estado == "decimal_obrigatorio":
            if c.isdigit():
                estado = "decimal"
                i += 1
            else:
                trecho = linha_texto[inicio:i]
                raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: numero invalido '{trecho}'")

        elif estado == "decimal":
            if c.isdigit():
                i += 1
            elif c == ".":
                trecho = linha_texto[inicio:i + 1]
                raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: numero com mais de um ponto '{trecho}'")
            else:
                break

    lexema = linha_texto[inicio:i]
    return Token("NUMBER", lexema, num_linha, inicio + 1), i


def ler_palavra(linha_texto, i, num_linha):
    inicio = i

    while i < len(linha_texto) and (linha_texto[i].isupper() or linha_texto[i].isdigit() or linha_texto[i] == "_"):
        i += 1

    lexema = linha_texto[inicio:i]
    prox = linha_texto[i] if i < len(linha_texto) else None

    if not fim_de_token(prox):
        raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: palavra invalida iniciando em '{linha_texto[inicio:i+1]}'")

    tipo = PALAVRAS_RESERVADAS.get(lexema, "IDENTIFIER")
    return Token(tipo, lexema, num_linha, inicio + 1), i


def ler_operador(linha_texto, i, num_linha):
    inicio = i
    c = linha_texto[i]
    prox = linha_texto[i + 1] if i + 1 < len(linha_texto) else None
    dois = c + prox if prox is not None else c

    if dois in OPERADORES_RELACIONAIS_2:
        depois = linha_texto[i + 2] if i + 2 < len(linha_texto) else None
        if fim_de_token(depois):
            return Token("REL_OPERATOR", dois, num_linha, inicio + 1), i + 2
        raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: operador invalido '{dois + depois}'")

    if c in OPERADORES_RELACIONAIS_1:
        if fim_de_token(prox):
            return Token("REL_OPERATOR", c, num_linha, inicio + 1), i + 1
        raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: operador invalido '{c + prox}'")

    if c in OPERADORES_ARITMETICOS:
        if fim_de_token(prox):
            return Token("OPERATOR", c, num_linha, inicio + 1), i + 1
        raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: operador invalido '{c + prox}'")

    raise ValueError(f"Erro lexico na linha {num_linha}, coluna {inicio + 1}: operador invalido '{c}'")


def tokenizar_linha(linha_texto, num_linha):
    tokens = []
    i = 0

    while i < len(linha_texto):
        c = linha_texto[i]

        if c.isspace():
            i += 1
        elif c == "(":
            tokens.append(Token("LPAREN", c, num_linha, i + 1))
            i += 1
        elif c == ")":
            tokens.append(Token("RPAREN", c, num_linha, i + 1))
            i += 1
        elif c.isdigit():
            token, i = ler_numero(linha_texto, i, num_linha)
            tokens.append(token)
        elif c.isupper():
            token, i = ler_palavra(linha_texto, i, num_linha)
            tokens.append(token)
        elif c in "+-*|/%^><=!":
            token, i = ler_operador(linha_texto, i, num_linha)
            tokens.append(token)
        else:
            raise ValueError(f"Erro lexico na linha {num_linha}, coluna {i + 1}: caractere invalido '{c}'")

    return tokens


def lerTokens(nome_arquivo):
    """Le um arquivo inteiro e retorna todos os tokens em uma unica lista."""
    todos = []
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for num_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()
            if not linha:
                continue
            my_tokens = tokenizar_linha(linha, num_linha)
            if len(my_tokens) == 3 and my_tokens[0].tipo == "LPAREN" and my_tokens[2].tipo == "RPAREN" and my_tokens[1].tipo == "START":
                todos.append(Token("START_STMT", "(START)", num_linha, 1))
            elif len(my_tokens) == 3 and my_tokens[0].tipo == "LPAREN" and my_tokens[2].tipo == "RPAREN" and my_tokens[1].tipo == "END":
                todos.append(Token("END_STMT", "(END)", num_linha, 1))
            else:
                todos.extend(my_tokens)
    todos.append(Token("EOF", "EOF", -1, -1))
    return todos


# Compatibilidade com a Fase 1: tokeniza uma expressao isolada e retorna tuplas.
def parseExpressao(linha):
    return [token.as_tuple() for token in tokenizar_linha(linha, 1)]
