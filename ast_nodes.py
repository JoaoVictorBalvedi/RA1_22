# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

"""Nos da arvore sintatica abstrata (AST)."""


def criarNoPrograma(comandos):
    return {"tipo": "programa", "comandos": comandos}


def criarNoNumero(valor):
    return {"tipo": "numero", "valor": valor}


def criarNoMemLeitura():
    return {"tipo": "mem_leitura"}


def criarNoMemEscrita(valor):
    return {"tipo": "mem_escrita", "valor": valor}


def criarNoRes(indice):
    return {"tipo": "res", "indice": int(float(indice))}


def criarNoOperacao(operador, esquerda, direita):
    return {"tipo": "operacao", "operador": operador, "esquerda": esquerda, "direita": direita}


def criarNoComparacao(operador, esquerda, direita):
    return {"tipo": "comparacao", "operador": operador, "esquerda": esquerda, "direita": direita}


def criarNoVarLeitura(nome):
    return {"tipo": "var_leitura", "nome": nome}


def criarNoVarEscrita(nome, valor):
    return {"tipo": "var_escrita", "nome": nome, "valor": valor}


def criarNoIf(condicao, corpo):
    return {"tipo": "if", "condicao": condicao, "corpo": corpo}


def criarNoWhile(condicao, corpo):
    return {"tipo": "while", "condicao": condicao, "corpo": corpo}
