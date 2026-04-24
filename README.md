# Analisador Sintático LL(1) — RPN para Assembly ARMv7

**Disciplina:** Construção de Interpretadores  
**Grupo:** `<RA2_22>`

## Integrantes em ordem alfabética

| Nome | GitHub |
|---|---|
| Joao Victor Balvedi | @JoaoVictorBalvedi |

## Descrição

Este projeto implementa a Fase 2 do trabalho: um analisador sintático para uma linguagem simplificada em notação polonesa reversa, usando parser descendente recursivo LL(1), geração de árvore sintática e geração de Assembly ARMv7 para CPUlator DE1-SOC.

O fluxo geral é:

```text
arquivo fonte -> tokens -> parser LL(1) -> árvore sintática -> assembly
```

## Como executar

```bash
python main.py teste1.txt
```

O programa gera:

- `teste1_tokens.json`
- `teste1_arvore.json`
- `teste1.s`
- `gramatica_ll1.md`
- `arvore_ultima_execucao.md`

## Como rodar testes

```bash
python tests.py
```

## Sintaxe da linguagem

Todo programa deve começar com:

```text
(START)
```

E terminar com:

```text
(END)
```

### Expressões aritméticas

Formato:

```text
(A B op)
```

Operadores:

| Operador | Significado |
|---|---|
| `+` | soma |
| `-` | subtração |
| `*` | multiplicação |
| `|` | divisão real |
| `/` | divisão inteira |
| `%` | resto |
| `^` | potência |

Exemplos:

```text
(3 4 +)
((2 3 *) 4 +)
```

### Memória e resultados

```text
(V MEM)    salva valor em MEM
(MEM)      lê MEM
(V VAR)    salva valor em variável nomeada
(VAR)      lê variável nomeada
(N RES)    lê resultado de N comandos anteriores
```

Exemplos:

```text
(10 X)
(X)
(1 RES)
```

### Operadores relacionais

Formato:

```text
(A B relop)
```

Operadores:

```text
> < >= <= == !=
```

Exemplo:

```text
(X 10 >)
```

### Tomada de decisão

Sintaxe escolhida pelo grupo:

```text
(condicao (comandos) IF)
```

Exemplo:

```text
((X 10 >) ((100 MEM)) IF)
```

### Laço de repetição

Sintaxe escolhida pelo grupo:

```text
(condicao (comandos) WHILE)
```

Exemplo:

```text
((X 10 <) (((X 1 +) X)) WHILE)
```

## Organização dos arquivos

```text
main.py              ponto de entrada
lexer.py             analisador léxico
syntactic_parser.py  parser descendente recursivo
ast_nodes.py         criação dos nós da árvore
grammar.py           gramática, FIRST, FOLLOW e tabela LL(1)
assembly.py          geração de Assembly
tests.py             testes básicos
teste1.txt           teste válido
teste2.txt           teste válido
teste3.txt           teste válido
teste_erro_lexico.txt      teste inválido
teste_erro_sintatico.txt   teste inválido
```

## Observações

A gramática, os conjuntos FIRST/FOLLOW e a tabela LL(1) são gerados no arquivo `gramatica_ll1.md` a cada execução.
