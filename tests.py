# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

from lexer import lerTokens
from grammar import construirResumoGramatica
from syntactic_parser import parsear


def testar_arquivo(nome, deve_passar=True):
    try:
        tokens = lerTokens(nome)
        resumo = construirResumoGramatica()
        arvore = parsear(tokens, resumo["tabela"])
        if deve_passar:
            print(f"[OK] {nome} aceito. Comandos: {len(arvore['comandos'])}")
        else:
            print(f"[FALHOU] {nome} deveria ser rejeitado")
    except Exception as erro:
        if deve_passar:
            print(f"[FALHOU] {nome} deveria passar, mas deu erro: {erro}")
        else:
            print(f"[OK] {nome} rejeitado: {erro}")


if __name__ == "__main__":
    testar_arquivo("teste1.txt", True)
    testar_arquivo("teste2.txt", True)
    testar_arquivo("teste3.txt", True)
    testar_arquivo("teste_erro_lexico.txt", False)
    testar_arquivo("teste_erro_sintatico.txt", False)
