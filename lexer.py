# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: RA1 22

from dataclasses import dataclass, asdict
import json


@dataclass
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int

    def to_dict(self):
        return asdict(self)


PALAVRAS_RESERVADAS = {
    "START": "START",
    "END": "END",
    "RES": "RES",
    "MEM": "MEM",
    "IF": "IF",
    "WHILE": "WHILE",
}

OPERADORES_ARITMETICOS = {"+", "-", "*", "|", "/", "%", "^"}
OPERADORES_RELACIONAIS_UM = {">", "<"}
OPERADORES_RELACIONAIS_DOIS = {">=", "<=", "==", "!="}


def fim_de_token(c):
    return c is None or c.isspace() or c in "()"

def _linha_eh_inicio_ou_fim(linha_texto, numero_linha):
    linha = linha_texto.strip()
    if linha == "(START)":
        return [Token("START_LINE", "(START)", numero_linha, 1)]
    if linha == "(END)":
        return [Token("END_LINE", "(END)", numero_linha, 1)]
    return None


def tokenizar_linha(linha_texto, numero_linha):
    especiais = _linha_eh_inicio_ou_fim(linha_texto, numero_linha)
    if especiais is not None:
        return especiais

    tokens = []
    i = 0
    pilha_parens = []  # True => proximo elemento apos '(' ainda nao foi lido

    while i < len(linha_texto):
        c = linha_texto[i]
        coluna = i + 1

        if c.isspace():
            i += 1
            continue

        if c == "(":
            if pilha_parens and pilha_parens[-1] is True:
                pilha_parens[-1] = False  # '(' pode ser um elemento do par externo
            tokens.append(Token("LPAREN", c, numero_linha, coluna))
            pilha_parens.append(True)
            i += 1
            continue

        if c == ")":
            tokens.append(Token("RPAREN", c, numero_linha, coluna))
            if pilha_parens:
                pilha_parens.pop()
            i += 1
            continue

        if c.isdigit():
            inicio = i
            estado = "inteiro"

            while i < len(linha_texto):
                atual = linha_texto[i]

                if estado == "inteiro":
                    if atual.isdigit():
                        i += 1
                    elif atual == ".":
                        estado = "decimal_obrigatorio"
                        i += 1
                    else:
                        break

                elif estado == "decimal_obrigatorio":
                    if atual.isdigit():
                        estado = "decimal"
                        i += 1
                    else:
                        parcial = linha_texto[inicio:i]
                        raise ValueError(
                            f"Erro lexico na linha {numero_linha}, coluna {coluna}: numero invalido '{parcial}'"
                        )

                elif estado == "decimal":
                    if atual.isdigit():
                        i += 1
                    elif atual == ".":
                        invalido = linha_texto[inicio:i + 1]
                        raise ValueError(
                            f"Erro lexico na linha {numero_linha}, coluna {coluna}: numero com mais de um ponto '{invalido}'"
                        )
                    else:
                        break

            lexema = linha_texto[inicio:i]
            prox = linha_texto[i] if i < len(linha_texto) else None
            if not fim_de_token(prox) and prox not in OPERADORES_ARITMETICOS and prox not in "><=!":
                raise ValueError(
                    f"Erro lexico na linha {numero_linha}, coluna {coluna}: numero colado em token invalido perto de '{lexema + prox}'"
                )

            tokens.append(Token("NUMBER", lexema, numero_linha, coluna))
            if pilha_parens and pilha_parens[-1] is True:
                pilha_parens[-1] = False
            continue

        if c.isupper():
            inicio = i
            while i < len(linha_texto) and (linha_texto[i].isupper() or linha_texto[i].isdigit() or linha_texto[i] == "_"):
                i += 1

            lexema = linha_texto[inicio:i]
            prox = linha_texto[i] if i < len(linha_texto) else None

            if not fim_de_token(prox):
                raise ValueError(
                    f"Erro lexico na linha {numero_linha}, coluna {coluna}: palavra invalida perto de '{linha_texto[inicio:i + 1]}'"
                )

            tipo_base = PALAVRAS_RESERVADAS.get(lexema, "IDENTIFIER")

            if tipo_base in {"MEM", "IDENTIFIER"} and pilha_parens:
                if pilha_parens[-1] is True:
                    tipo = "MEM_ELEM" if tipo_base == "MEM" else "IDENT_ELEM"
                    pilha_parens[-1] = False
                else:
                    # Se o proximo caractere nao-espaco for ')', este token e alvo de atribuicao: (V MEM) ou (V VAR)
                    j = i
                    while j < len(linha_texto) and linha_texto[j].isspace():
                        j += 1
                    fecha = j < len(linha_texto) and linha_texto[j] == ")"

                    if tipo_base == "MEM":
                        tipo = "MEM_ASSIGN" if fecha else "MEM_REST"
                    else:
                        tipo = "IDENT_ASSIGN" if fecha else "IDENT_REST"
            else:
                tipo = tipo_base

            tokens.append(Token(tipo, lexema, numero_linha, coluna))
            continue

        dois = linha_texto[i:i + 2]
        if dois in OPERADORES_RELACIONAIS_DOIS:
            depois = linha_texto[i + 2] if i + 2 < len(linha_texto) else None
            if not fim_de_token(depois):
                raise ValueError(
                    f"Erro lexico na linha {numero_linha}, coluna {coluna}: operador relacional invalido '{dois + depois}'"
                )
            tokens.append(Token("REL_OPERATOR", dois, numero_linha, coluna))
            i += 2
            continue

        if c in OPERADORES_RELACIONAIS_UM:
            prox = linha_texto[i + 1] if i + 1 < len(linha_texto) else None
            if not fim_de_token(prox):
                raise ValueError(
                    f"Erro lexico na linha {numero_linha}, coluna {coluna}: operador relacional invalido '{c + prox}'"
                )
            tokens.append(Token("REL_OPERATOR", c, numero_linha, coluna))
            i += 1
            continue

        if c in OPERADORES_ARITMETICOS:
            prox = linha_texto[i + 1] if i + 1 < len(linha_texto) else None
            if not fim_de_token(prox):
                raise ValueError(
                    f"Erro lexico na linha {numero_linha}, coluna {coluna}: operador invalido '{c + prox}'"
                )
            tokens.append(Token("OPERATOR", c, numero_linha, coluna))
            i += 1
            continue

        if c == "=":
            raise ValueError(
                f"Erro lexico na linha {numero_linha}, coluna {coluna}: use '==' para comparacao"
            )

        raise ValueError(
            f"Erro lexico na linha {numero_linha}, coluna {coluna}: caractere invalido '{c}'"
        )

    return tokens


def lerTokens(nome_arquivo):
    todos_tokens = []

    if nome_arquivo.lower().endswith(".json"):
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError("Arquivo de tokens JSON invalido: esperado uma lista de tokens")

        for item in dados:
            try:
                todos_tokens.append(
                    Token(
                        item["tipo"],
                        item.get("valor", ""),
                        int(item.get("linha", -1)),
                        int(item.get("coluna", -1)),
                    )
                )
            except Exception as e:
                raise ValueError(f"Token invalido no JSON: {item}") from e

        todos_tokens.append(Token("EOF", "EOF", -1, -1))
        return todos_tokens

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()
            if not linha:
                continue
            todos_tokens.extend(tokenizar_linha(linha, numero_linha))

    todos_tokens.append(Token("EOF", "EOF", -1, -1))
    return todos_tokens
