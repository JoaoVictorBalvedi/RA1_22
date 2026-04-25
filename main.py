# Integrantes do grupo (ordem alfabetica):
# Joao Victor Balvedi - @JoaoVictorBalvedi
#
# Nome do grupo no Canvas: RA1 22

import json
import os
import sys

from lexer import lerTokens
from grammar import construirTudoLl1
from syntactic_parser import parsear
from assembly import gerarAssembly
from results import resumo_terminal


def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def salvar_texto(nome_arquivo, conteudo):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def arvore_para_linhas(no, nivel=0):
    indent = "  " * nivel
    tipo = no.get("tipo", "?")
    linhas = []

    if tipo == "programa":
        linhas.append(f"{indent}**programa** ({len(no['comandos'])} comandos)")
        for i, cmd in enumerate(no["comandos"]):
            linhas.append(f"{indent}  - *comando {i}:*")
            linhas.extend(arvore_para_linhas(cmd, nivel + 2))
    elif tipo == "numero":
        linhas.append(f"{indent}numero: `{no['valor']}`")
    elif tipo == "operacao":
        linhas.append(f"{indent}operacao: `{no['operador']}`")
        linhas.append(f"{indent}  - *esquerda:*")
        linhas.extend(arvore_para_linhas(no["esquerda"], nivel + 2))
        linhas.append(f"{indent}  - *direita:*")
        linhas.extend(arvore_para_linhas(no["direita"], nivel + 2))
    elif tipo == "comparacao":
        linhas.append(f"{indent}comparacao: `{no['operador']}`")
        linhas.append(f"{indent}  - *esquerda:*")
        linhas.extend(arvore_para_linhas(no["esquerda"], nivel + 2))
        linhas.append(f"{indent}  - *direita:*")
        linhas.extend(arvore_para_linhas(no["direita"], nivel + 2))
    elif tipo == "var_leitura":
        linhas.append(f"{indent}var_leitura: `{no['nome']}`")
    elif tipo == "var_escrita":
        linhas.append(f"{indent}var_escrita: `{no['nome']}`")
        linhas.append(f"{indent}  - *valor:*")
        linhas.extend(arvore_para_linhas(no["valor"], nivel + 2))
    elif tipo == "mem_leitura":
        linhas.append(f"{indent}mem_leitura")
    elif tipo == "mem_escrita":
        linhas.append(f"{indent}mem_escrita")
        linhas.append(f"{indent}  - *valor:*")
        linhas.extend(arvore_para_linhas(no["valor"], nivel + 2))
    elif tipo == "res":
        linhas.append(f"{indent}res: `{no['indice']}`")
    elif tipo == "if":
        linhas.append(f"{indent}if")
        linhas.append(f"{indent}  - *condicao:*")
        linhas.extend(arvore_para_linhas(no["condicao"], nivel + 2))
        linhas.append(f"{indent}  - *comando:*")
        linhas.extend(arvore_para_linhas(no["comando"], nivel + 2))
    elif tipo == "while":
        linhas.append(f"{indent}while")
        linhas.append(f"{indent}  - *condicao:*")
        linhas.extend(arvore_para_linhas(no["condicao"], nivel + 2))
        linhas.append(f"{indent}  - *comando:*")
        linhas.extend(arvore_para_linhas(no["comando"], nivel + 2))
    else:
        linhas.append(f"{indent}{tipo}")

    return linhas


def gerar_arvore_md(nome_entrada, arvore):
    with open(nome_entrada, "r", encoding="utf-8") as f:
        codigo_fonte = f.read().strip()

    linhas = []
    linhas.append("# Arvore Sintatica")
    linhas.append("")
    linhas.append(f"Gerada a partir do arquivo `{nome_entrada}`.")
    linhas.append("")
    linhas.append("## Codigo-fonte")
    linhas.append("")
    linhas.append("```")
    linhas.append(codigo_fonte)
    linhas.append("```")
    linhas.append("")
    linhas.append("## Representacao em arvore")
    linhas.append("")
    linhas.extend(arvore_para_linhas(arvore))
    linhas.append("")
    linhas.append("## JSON completo")
    linhas.append("")
    linhas.append("Ver arquivo `arvore_sintatica.json` para a representacao completa em JSON.")
    linhas.append("")
    return "\n".join(linhas)


def gerar_relatorio_execucao(nome_entrada, tokens, resultado_parse, nome_assembly):
    linhas = []
    linhas.append("# Ultima execucao")
    linhas.append("")
    linhas.append(f"Arquivo de entrada: `{nome_entrada}`")
    linhas.append(f"Assembly gerado: `{nome_assembly}`")
    linhas.append(f"Total de tokens: {len(tokens) - 1}")
    linhas.append(f"Total de comandos na AST: {len(resultado_parse['arvore']['comandos'])}")
    linhas.append("")
    linhas.append("## Derivacao registrada")
    linhas.append("")
    for passo in resultado_parse["derivacao"]:
        linhas.append(f"- {passo}")
    linhas.append("")
    linhas.append("## Resultado")
    linhas.append("")
    linhas.append("- Analise lexica concluida com sucesso.")
    linhas.append("- Analise sintatica LL(1) concluida com sucesso.")
    linhas.append("- Arvore sintatica gerada em `arvore_sintatica.json`.")
    linhas.append(f"- Codigo Assembly gerado em `{nome_assembly}`.")
    linhas.append("")
    return "\n".join(linhas)


def main():
    if len(sys.argv) != 2:
        print("Uso: ./AnalisadorSintatico teste1.txt")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    if not os.path.exists(arquivo_entrada):
        print(f"Arquivo nao encontrado: {arquivo_entrada}")
        sys.exit(1)

    base, _ = os.path.splitext(os.path.basename(arquivo_entrada))
    arquivo_assembly = f"{base}.s"
    arquivo_tokens = f"{base}_tokens.json"
    arquivo_arvore = "arvore_sintatica.json"
    arquivo_arvore_md = "arvore_sintatica.md"
    arquivo_execucao = "ultima_execucao.md"

    try:
        dados_ll1 = construirTudoLl1()
        if dados_ll1["conflitos"]:
            print("A gramatica possui conflitos LL(1):")
            for conflito in dados_ll1["conflitos"]:
                print(conflito)
            sys.exit(1)

        tokens = lerTokens(arquivo_entrada)
        resultado_parse = parsear(tokens, dados_ll1["tabela"])
        codigo_assembly = gerarAssembly(resultado_parse["arvore"])

        salvar_json(arquivo_tokens, [token.to_dict() for token in tokens if token.tipo != "EOF"])
        salvar_json(arquivo_arvore, resultado_parse["arvore"])
        salvar_texto(arquivo_assembly, codigo_assembly)
        salvar_texto(
            arquivo_arvore_md,
            gerar_arvore_md(arquivo_entrada, resultado_parse["arvore"]),
        )
        salvar_texto(
            arquivo_execucao,
            gerar_relatorio_execucao(arquivo_entrada, tokens, resultado_parse, arquivo_assembly),
        )

        resumo_terminal(
            arquivo_entrada,
            arquivo_assembly,
            arquivo_tokens,
            arquivo_arvore,
            arquivo_arvore_md,
            arquivo_execucao,
            len(resultado_parse["arvore"]["comandos"]),
        )

    except (ValueError, SyntaxError) as erro:
        print(str(erro))
        sys.exit(1)


if __name__ == "__main__":
    main()