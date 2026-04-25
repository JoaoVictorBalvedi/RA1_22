# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: RA1 22

from ast_nodes import (
    criarNoPrograma,
    criarNoNumero,
    criarNoMemLeitura,
    criarNoMemEscrita,
    criarNoRes,
    criarNoOperacao,
    criarNoComparacao,
    criarNoVarLeitura,
    criarNoVarEscrita,
    criarNoIf,
    criarNoWhile,
)


class ParserLL1:
    def __init__(self, tokens, tabela_ll1=None):
        self.tokens = tokens
        self.i = 0
        self.tabela_ll1 = tabela_ll1 or {}
        self.derivacao = []
        self.pilha_analise = ["programa"]

    def atual(self):
        return self.tokens[self.i]

    _TIPO_LEGIVEL = {
        "START_LINE":   "START",
        "END_LINE":     "END",
        "IDENT_ELEM":   "IDENTIFIER",
        "IDENT_REST":   "IDENTIFIER",
        "IDENT_ASSIGN": "IDENTIFIER",
        "MEM_ELEM":     "MEM",
        "MEM_REST":     "MEM",
        "MEM_ASSIGN":   "MEM",
    }

    def erro(self, mensagem):
        token = self.atual()
        local = "fim do arquivo" if token.tipo == "EOF" else f"linha {token.linha}, coluna {token.coluna}"
        tipo_exibido = self._TIPO_LEGIVEL.get(token.tipo, token.tipo)
        raise SyntaxError(f"Erro sintatico em {local}: {mensagem}. Token encontrado: {tipo_exibido}('{token.valor}')")

    def consumir(self, tipo, valor=None):
        token = self.atual()
        if token.tipo != tipo:
            esperado = tipo if valor is None else f"{tipo}('{valor}')"
            self.erro(f"esperado {esperado}")
        if valor is not None and token.valor != valor:
            self.erro(f"esperado {tipo}('{valor}')")
        self.i += 1
        return token

    def parsear_programa(self):
        self.derivacao.append("programa -> inicio comandos fim EOF")
        self.parsear_inicio()

        comandos = []
        while not self.eh_fim_programa():
            comandos.append(self.parsear_comando())

        self.parsear_fim()
        self.consumir("EOF")
        return criarNoPrograma(comandos)

    def eh_fim_programa(self):
        return self.atual().tipo == "END_LINE"

    def parsear_inicio(self):
        self.derivacao.append("inicio -> START_LINE")
        self.consumir("START_LINE")

    def parsear_fim(self):
        self.derivacao.append("fim -> END_LINE")
        self.consumir("END_LINE")

    def parsear_comando(self):
        self.derivacao.append("comando -> estrutura_parentesizada")
        return self.parsear_estrutura_parentesizada()

    def parsear_elemento(self):
        token = self.atual()

        if token.tipo == "NUMBER":
            self.derivacao.append("elemento -> NUMBER")
            return criarNoNumero(self.consumir("NUMBER").valor)

        if token.tipo == "IDENT_ELEM":
            self.derivacao.append("elemento -> IDENT_ELEM")
            return criarNoVarLeitura(self.consumir("IDENT_ELEM").valor)

        if token.tipo == "IDENT_REST":
            self.derivacao.append("elemento -> IDENT_REST")
            return criarNoVarLeitura(self.consumir("IDENT_REST").valor)

        if token.tipo == "MEM_ELEM":
            self.derivacao.append("elemento -> MEM_ELEM")
            self.consumir("MEM_ELEM")
            return criarNoMemLeitura()

        if token.tipo == "MEM_REST":
            self.derivacao.append("elemento -> MEM_REST")
            self.consumir("MEM_REST")
            return criarNoMemLeitura()

        if token.tipo == "LPAREN":
            self.derivacao.append("elemento -> estrutura_parentesizada")
            return self.parsear_estrutura_parentesizada()

        self.erro("esperado numero, identificador, MEM ou subexpressao")

    def parsear_estrutura_parentesizada(self):
        self.derivacao.append("estrutura_parentesizada -> LPAREN elemento resto_estrutura")
        self.consumir("LPAREN")

        if self.atual().tipo in {"START", "END"}:
            self.erro("START e END so podem aparecer no inicio e no fim do programa")

        primeiro = self.parsear_elemento()
        token = self.atual()

        # Leitura simples: (MEM) ou (VAR)
        if token.tipo == "RPAREN":
            if primeiro["tipo"] not in {"mem_leitura", "var_leitura"}:
                self.erro("estrutura com apenas um elemento so pode ser leitura de MEM ou variavel")
            self.derivacao.append("resto_estrutura -> RPAREN")
            self.consumir("RPAREN")
            return primeiro

        # Comando (N RES)
        if token.tipo == "RES":
            self.derivacao.append("resto_estrutura -> RES RPAREN")
            if primeiro["tipo"] != "numero":
                self.erro("RES deve receber numero inteiro como indice")
            self.consumir("RES")
            self.consumir("RPAREN")
            return criarNoRes(primeiro["valor"])

        # Comando (V MEM). So e escrita quando MEM vem imediatamente antes de ')'.
        # Caso contrario, MEM e tratado como segundo operando de uma operacao.
        if token.tipo == "MEM_ASSIGN":
            self.derivacao.append("resto_estrutura -> MEM_ASSIGN RPAREN")
            self.consumir("MEM_ASSIGN")
            self.consumir("RPAREN")
            return criarNoMemEscrita(primeiro)

        # Comando (V VAR). So e escrita quando IDENTIFIER vem imediatamente antes de ')'.
        # Caso contrario, IDENTIFIER e tratado como segundo operando de uma operacao.
        if token.tipo == "IDENT_ASSIGN":
            self.derivacao.append("resto_estrutura -> IDENT_ASSIGN RPAREN")
            nome = self.consumir("IDENT_ASSIGN").valor
            self.consumir("RPAREN")
            return criarNoVarEscrita(nome, primeiro)

        segundo = self.parsear_elemento()
        token = self.atual()

        if token.tipo == "OPERATOR":
            self.derivacao.append("resto_estrutura -> elemento OPERATOR RPAREN")
            operador = self.consumir("OPERATOR").valor
            self.consumir("RPAREN")
            return criarNoOperacao(operador, primeiro, segundo)

        if token.tipo == "REL_OPERATOR":
            self.derivacao.append("resto_estrutura -> elemento REL_OPERATOR RPAREN")
            operador = self.consumir("REL_OPERATOR").valor
            self.consumir("RPAREN")
            return criarNoComparacao(operador, primeiro, segundo)

        if token.tipo == "IF":
            self.derivacao.append("resto_estrutura -> elemento IF RPAREN")
            self.consumir("IF")
            self.consumir("RPAREN")
            return criarNoIf(primeiro, segundo)

        if token.tipo == "WHILE":
            self.derivacao.append("resto_estrutura -> elemento WHILE RPAREN")
            self.consumir("WHILE")
            self.consumir("RPAREN")
            return criarNoWhile(primeiro, segundo)

        self.erro("esperado operador aritmetico, operador relacional, IF ou WHILE")


def parsear(tokens, tabela_ll1=None):
    parser = ParserLL1(tokens, tabela_ll1)
    arvore = parser.parsear_programa()
    return {
        "arvore": arvore,
        "derivacao": parser.derivacao,
        "pilha_final": parser.pilha_analise,
    }