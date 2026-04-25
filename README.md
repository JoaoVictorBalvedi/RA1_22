# Analisador Sintatico LL(1) — Linguagem RPN

**Disciplina:** Construção de Interpretadores  
**Grupo no Canvas:** RA1 22

## Integrantes em ordem alfabetica

| Nome | GitHub |
|---|---|
| Joao Victor Balvedi | @JoaoVictorBalvedi |

## Descricao

Este projeto implementa a segunda fase do trabalho: um analisador sintatico LL(1) para uma linguagem simples em notacao polonesa reversa (RPN). O programa:

1. le um arquivo `.txt` informado por argumento de linha de comando;
2. executa a analise lexica e gera tokens;
3. valida a estrutura do programa com um parser descendente recursivo LL(1);
4. gera a arvore sintatica em JSON;
5. gera codigo Assembly ARMv7 para o ambiente CPUlator DE1-SoC;
6. salva um relatorio da ultima execucao.

## Como executar

```bash
chmod +x ./AnalisadorSintatico
./AnalisadorSintatico teste1.txt
```

Tambem podem ser usados:

```bash
./AnalisadorSintatico teste2.txt
./AnalisadorSintatico teste3.txt
```

## Como rodar os testes

```bash
python tests.py
```

## Arquivos principais

| Arquivo | Funcao |
|---|---|
| `main.py` | Integra lexer, gramatica, parser, AST e Assembly |
| `lexer.py` | Implementa `lerTokens(arquivo)` |
| `grammar.py` | Implementa `construirGramatica`, FIRST, FOLLOW e tabela LL(1) |
| `syntactic_parser.py` | Implementa `parsear(tokens, tabela_ll1)` |
| `ast_nodes.py` | Define os nos da arvore sintatica |
| `assembly.py` | Implementa `gerarAssembly(arvore)` |
| `tests.py` | Executa testes validos e invalidos |
| `gramatica_ll1.md` | Documenta gramatica, FIRST, FOLLOW e tabela LL(1) |

## Sintaxe da linguagem

Todo programa deve comecar com:

```txt
(START)
```

E terminar com:

```txt
(END)
```

As expressoes seguem o formato RPN:

```txt
(A B operador)
```

Exemplos:

```txt
(3 4 +)
(10 2 /)
((3 4 +) (2 5 *) |)
```

## Operadores

| Operador | Significado |
|---|---|
| `+` | soma |
| `-` | subtracao |
| `*` | multiplicacao |
| `|` | divisao real |
| `/` | divisao inteira |
| `%` | resto da divisao inteira |
| `^` | potenciacao |

## Comandos especiais

| Comando | Significado |
|---|---|
| `(N RES)` | acessa o resultado de N comandos anteriores |
| `(V MEM)` | grava V na memoria especial MEM |
| `(MEM)` | le a memoria especial MEM |
| `(V X)` | grava V na variavel X |
| `(X)` | le a variavel X |

## Estruturas de controle adotadas

As estruturas de controle tambem seguem notacao pos-fixada.

### Decisao

```txt
(condicao comando IF)
```

Exemplo:

```txt
((X Y <) (X Y +) IF)
```

Significado: se `X < Y`, executa `(X Y +)`.

### Repeticao

```txt
(condicao comando WHILE)
```

Exemplo:

```txt
((X 12 <) ((X 1 +) X) WHILE)
```

Significado: enquanto `X < 12`, executa `((X 1 +) X)`.

## Saidas geradas

Ao executar:

```bash
./AnalisadorSintatico teste1.txt
```

sao gerados:

| Arquivo | Conteudo |
|---|---|
| `teste1.s` | Assembly ARMv7 |
| `teste1_tokens.json` | tokens da entrada |
| `arvore_sintatica.json` | arvore sintatica da ultima execucao |
| `arvore_sintatica.md` | arvore sintatica em formato markdown |
| `ultima_execucao.md` | relatorio da ultima execucao |

## CPUlator

O arquivo `.s` pode ser testado no CPUlator ARMv7 DE1-SoC. O ultimo resultado tambem e enviado para os LEDs no endereco `0xFF200000`.
