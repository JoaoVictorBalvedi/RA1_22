# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

"""Parser sintatico descendente recursivo para a Fase 2."""

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


class ErroSintatico(ValueError):
    pass


class ParserLL1:
    def __init__(self, tokens, tabela_ll1=None):
        self.tokens = tokens
        self.i = 0
        self.tabela_ll1 = tabela_ll1 or {}

    def atual(self):
        if self.i >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.i]

    def proximo(self, deslocamento=1):
        pos = self.i + deslocamento
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]

    def erro(self, mensagem):
        token = self.atual()
        raise ErroSintatico(
            f"Erro sintatico na linha {token.linha}, coluna {token.coluna}: {mensagem}. "
            f"Encontrado {token.tipo}('{token.valor}')"
        )

    def consumir(self, tipo, valor=None):
        token = self.atual()
        if token.tipo != tipo:
            self.erro(f"esperado token {tipo}")
        if valor is not None and token.valor != valor:
            self.erro(f"esperado valor {valor}")
        self.i += 1
        return token

    def parsear_programa(self):
        self.consumir("START_STMT")

        comandos = []
        while self.atual().tipo != "END_STMT":
            if self.atual().tipo == "EOF":
                self.erro("programa terminou antes de (END)")
            comandos.append(self.parsear_comando())

        self.consumir("END_STMT")
        self.consumir("EOF")
        return criarNoPrograma(comandos)

    def parsear_comando(self):
        if self.atual().tipo != "LPAREN":
            self.erro("comando deve iniciar com '('")

        # Decisao/laco sao formas: ( expressao bloco IF/WHILE )
        # Expressao simples tambem comeca com LPAREN. Por isso parseamos o conteudo
        # e decidimos pelo token antes do RPAREN.
        return self.parsear_expressao_ou_controle()

    def parsear_expressao_ou_controle(self):
        self.consumir("LPAREN")

        # Leitura simples: (MEM) ou (VAR)
        if self.atual().tipo == "MEM" and self.proximo().tipo == "RPAREN":
            self.consumir("MEM")
            self.consumir("RPAREN")
            return criarNoMemLeitura()

        if self.atual().tipo == "IDENTIFIER" and self.proximo().tipo == "RPAREN":
            nome = self.consumir("IDENTIFIER").valor
            self.consumir("RPAREN")
            return criarNoVarLeitura(nome)

        primeiro = self.parsear_operando()

        # Depois do primeiro item, pode ser RES, MEM, IDENTIFIER, segundo operando ou bloco.
        if self.atual().tipo == "RES":
            if primeiro["tipo"] != "numero":
                self.erro("RES deve receber numero como indice")
            self.consumir("RES")
            self.consumir("RPAREN")
            return criarNoRes(primeiro["valor"])

        if self.atual().tipo == "MEM" and self.proximo().tipo == "RPAREN":
            self.consumir("MEM")
            self.consumir("RPAREN")
            return criarNoMemEscrita(primeiro)

        if self.atual().tipo == "IDENTIFIER" and self.proximo().tipo == "RPAREN":
            nome = self.consumir("IDENTIFIER").valor
            self.consumir("RPAREN")
            return criarNoVarEscrita(nome, primeiro)

        # Estruturas de controle: ( condicao bloco IF ) ou ( condicao bloco WHILE )
        if self.atual().tipo == "LPAREN" and self._parece_bloco_de_comandos():
            corpo = self.parsear_bloco()
            if self.atual().tipo == "IF":
                self.consumir("IF")
                self.consumir("RPAREN")
                return criarNoIf(primeiro, corpo)
            if self.atual().tipo == "WHILE":
                self.consumir("WHILE")
                self.consumir("RPAREN")
                return criarNoWhile(primeiro, corpo)
            self.erro("esperado IF ou WHILE apos bloco")

        segundo = self.parsear_operando()

        if self.atual().tipo == "OPERATOR":
            operador = self.consumir("OPERATOR").valor
            self.consumir("RPAREN")
            return criarNoOperacao(operador, primeiro, segundo)

        if self.atual().tipo == "REL_OPERATOR":
            operador = self.consumir("REL_OPERATOR").valor
            self.consumir("RPAREN")
            return criarNoComparacao(operador, primeiro, segundo)

        self.erro("esperado operador aritmetico ou relacional")

    def _parece_bloco_de_comandos(self):
        # Neste projeto, bloco eh sempre uma lista de comandos entre parenteses:
        # ( comando comando ... ). Como comando tambem comeca com LPAREN, o bloco
        # tambem comeca com dois LPAREN quando nao esta vazio.
        return self.atual().tipo == "LPAREN"

    def parsear_bloco(self):
        self.consumir("LPAREN")
        comandos = []
        while self.atual().tipo != "RPAREN":
            if self.atual().tipo == "EOF":
                self.erro("bloco terminou sem ')'")
            comandos.append(self.parsear_comando())
        self.consumir("RPAREN")
        return comandos

    def parsear_operando(self):
        token = self.atual()

        if token.tipo == "NUMBER":
            return criarNoNumero(self.consumir("NUMBER").valor)

        if token.tipo == "IDENTIFIER":
            return criarNoVarLeitura(self.consumir("IDENTIFIER").valor)

        if token.tipo == "MEM":
            self.consumir("MEM")
            return criarNoMemLeitura()

        if token.tipo == "LPAREN":
            return self.parsear_expressao_ou_controle()

        self.erro("esperado operando")


def parsear(tokens, tabela_ll1=None):
    parser = ParserLL1(tokens, tabela_ll1)
    return parser.parsear_programa()
