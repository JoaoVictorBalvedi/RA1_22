# Gramatica LL(1), FIRST, FOLLOW e Tabela de Analise

## Sintaxe das estruturas de controle

A linguagem usa notacao polonesa reversa. As estruturas de controle foram definidas tambem em formato pos-fixado:

- Decisao: `(condicao comando IF)`
- Repeticao: `(condicao comando WHILE)`

Exemplos:

```txt
((X Y <) (X Y +) IF)
((X 12 <) ((X 1 +) X) WHILE)
```

## Regras de producao

- `programa -> inicio lista_comandos fim EOF`
- `inicio -> START_LINE`
- `fim -> END_LINE`
- `lista_comandos -> comando lista_comandos | ε`
- `comando -> estrutura`
- `estrutura -> LPAREN elemento resto`
- `elemento -> NUMBER | IDENT_ELEM | MEM_ELEM | estrutura`
- `resto -> RPAREN | RES RPAREN | MEM_ASSIGN RPAREN | IDENT_ASSIGN RPAREN | elemento2 operador_final RPAREN`
- `operador_final -> OPERATOR | REL_OPERATOR | IF | WHILE`
- `elemento2 -> NUMBER | IDENT_REST | MEM_REST | estrutura`

## Conjuntos FIRST

- `FIRST(programa) = {START_LINE}`
- `FIRST(inicio) = {START_LINE}`
- `FIRST(fim) = {END_LINE}`
- `FIRST(lista_comandos) = {LPAREN, ε}`
- `FIRST(comando) = {LPAREN}`
- `FIRST(estrutura) = {LPAREN}`
- `FIRST(elemento) = {IDENT_ELEM, LPAREN, MEM_ELEM, NUMBER}`
- `FIRST(elemento2) = {IDENT_REST, LPAREN, MEM_REST, NUMBER}`
- `FIRST(resto) = {IDENT_ASSIGN, IDENT_REST, LPAREN, MEM_ASSIGN, MEM_REST, NUMBER, RES, RPAREN}`
- `FIRST(operador_final) = {IF, OPERATOR, REL_OPERATOR, WHILE}`

## Conjuntos FOLLOW

- `FOLLOW(programa) = {EOF}`
- `FOLLOW(inicio) = {LPAREN, END_LINE}`
- `FOLLOW(fim) = {EOF}`
- `FOLLOW(lista_comandos) = {END_LINE}`
- `FOLLOW(comando) = {LPAREN, END_LINE}`
- `FOLLOW(estrutura) = {IDENTIFIER, IF, LPAREN, MEM, NUMBER, OPERATOR, REL_OPERATOR, RES, RPAREN, WHILE}`
- `FOLLOW(elemento) = {IDENTIFIER, IF, LPAREN, MEM, NUMBER, OPERATOR, REL_OPERATOR, RES, RPAREN, WHILE}`
- `FOLLOW(resto) = {IDENTIFIER, IF, LPAREN, MEM, NUMBER, OPERATOR, REL_OPERATOR, RES, RPAREN, WHILE}`
- `FOLLOW(operador_final) = {RPAREN}`

## Tabela de analise LL(1)

| Nao-terminal | Terminal | Producao |
|---|---|---|
| `programa` | `START_LINE` | `programa -> inicio lista_comandos fim EOF` |
| `inicio` | `START_LINE` | `inicio -> START_LINE` |
| `fim` | `END_LINE` | `fim -> END_LINE` |
| `lista_comandos` | `LPAREN` | `lista_comandos -> comando lista_comandos` |
| `lista_comandos` | `END_LINE` | `lista_comandos -> ε` |
| `comando` | `LPAREN` | `comando -> estrutura` |
| `estrutura` | `LPAREN` | `estrutura -> LPAREN elemento resto` |
| `elemento` | `IDENTIFIER` | `elemento -> IDENTIFIER` |
| `elemento` | `LPAREN` | `elemento -> estrutura` |
| `elemento` | `MEM_ELEM` | `elemento -> MEM_ELEM` |
| `elemento` | `NUMBER` | `elemento -> NUMBER` |
| `elemento` | `IDENT_ELEM` | `elemento -> IDENT_ELEM` |
| `resto` | `IDENT_ASSIGN` | `resto -> IDENT_ASSIGN RPAREN` |
| `resto` | `IDENT_REST` | `resto -> elemento2 operador_final RPAREN` |
| `resto` | `LPAREN` | `resto -> elemento2 operador_final RPAREN` |
| `resto` | `MEM_ASSIGN` | `resto -> MEM_ASSIGN RPAREN` |
| `resto` | `MEM_REST` | `resto -> elemento2 operador_final RPAREN` |
| `resto` | `NUMBER` | `resto -> elemento2 operador_final RPAREN` |
| `resto` | `RES` | `resto -> RES RPAREN` |
| `resto` | `RPAREN` | `resto -> RPAREN` |
| `operador_final` | `IF` | `operador_final -> IF` |
| `operador_final` | `OPERATOR` | `operador_final -> OPERATOR` |
| `operador_final` | `REL_OPERATOR` | `operador_final -> REL_OPERATOR` |
| `operador_final` | `WHILE` | `operador_final -> WHILE` |

## Observacao sobre a implementacao

O parser implementado e descendente recursivo e usa a mesma decisao preditiva da tabela. Em comandos com estrutura RPN, a funcao de parsing consome o primeiro elemento e usa o proximo token para selecionar a continuidade da producao fatorada.