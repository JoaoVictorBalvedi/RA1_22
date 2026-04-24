# Grupo: <RA2_22>
# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: <RA2_22>

import json
import sys
from pathlib import Path

from lexer import lerTokens
from grammar import construirResumoGramatica
from syntactic_parser import parsear, ErroSintatico
from assembly import gerarAssembly


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def salvar_texto(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def arvore_para_markdown(arvore):
    return "# Árvore Sintática da Última Execução\n\n```json\n" + json.dumps(arvore, indent=2, ensure_ascii=False) + "\n```\n"


def gramatica_para_markdown(resumo):
    linhas = ["# Gramática LL(1), FIRST, FOLLOW e Tabela de Análise", ""]

    linhas.append("## Regras de Produção")
    for nt, producoes in resumo["gramatica"].items():
        alternativas = [" ".join(p) for p in producoes]
        linhas.append(f"- `{nt} -> {' | '.join(alternativas)}`")

    linhas.append("\n## FIRST")
    for nt, valores in resumo["first"].items():
        linhas.append(f"- `FIRST({nt}) = {{{', '.join(valores)}}}`")

    linhas.append("\n## FOLLOW")
    for nt, valores in resumo["follow"].items():
        linhas.append(f"- `FOLLOW({nt}) = {{{', '.join(valores)}}}`")

    linhas.append("\n## Tabela LL(1)")
    for chave, producao in resumo["tabela"].items():
        linhas.append(f"- `M[{chave}] = {' '.join(producao)}`")

    linhas.append("\n## Conflitos")
    if resumo["conflitos"]:
        for conflito in resumo["conflitos"]:
            linhas.append(f"- `{conflito}`")
    else:
        linhas.append("- Nenhum conflito detectado pela construção automática da tabela.")

    return "\n".join(linhas) + "\n"


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py teste1.txt")
        sys.exit(1)

    arquivo_entrada = Path(sys.argv[1])
    if not arquivo_entrada.exists():
        print(f"Arquivo nao encontrado: {arquivo_entrada}")
        sys.exit(1)

    try:
        tokens = lerTokens(str(arquivo_entrada))
        resumo = construirResumoGramatica()
        arvore = parsear(tokens, resumo["tabela"])
        assembly = gerarAssembly(arvore)
    except (ValueError, ErroSintatico) as erro:
        print(erro)
        sys.exit(1)

    base = arquivo_entrada.with_suffix("")
    salvar_json(base.with_name(base.name + "_tokens.json"), [t.__dict__ for t in tokens])
    salvar_json(base.with_name(base.name + "_arvore.json"), arvore)
    salvar_texto(base.with_name(base.name + ".s"), assembly)
    salvar_texto(base.with_name("gramatica_ll1.md"), gramatica_para_markdown(resumo))
    salvar_texto(base.with_name("arvore_ultima_execucao.md"), arvore_para_markdown(arvore))

    print(f"Arquivo processado: {arquivo_entrada}")
    print(f"Tokens salvos em: {base.name}_tokens.json")
    print(f"Arvore salva em: {base.name}_arvore.json")
    print(f"Assembly salvo em: {base.name}.s")
    print("Documentacao gerada: gramatica_ll1.md e arvore_ultima_execucao.md")


if __name__ == "__main__":
    main()
