# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: RA1 22

from lexer import lerTokens
from grammar import construirTudoLl1
from syntactic_parser import parsear


def deve_passar(nome_arquivo):
    dados = construirTudoLl1()
    tokens = lerTokens(nome_arquivo)
    parsear(tokens, dados["tabela"])
    print(f"[OK] {nome_arquivo} aceito")


def deve_falhar(nome_arquivo):
    dados = construirTudoLl1()
    try:
        tokens = lerTokens(nome_arquivo)
        parsear(tokens, dados["tabela"])
        print(f"[FALHOU] {nome_arquivo} deveria ser rejeitado")
    except (ValueError, SyntaxError) as erro:
        print(f"[OK] {nome_arquivo} rejeitado: {erro}")


def main():
    deve_passar("teste1.txt")
    deve_passar("teste2.txt")
    deve_passar("teste3.txt")
    deve_falhar("teste_erro_lexico.txt")
    deve_falhar("teste_erro_sintatico.txt")


if __name__ == "__main__":
    main()
