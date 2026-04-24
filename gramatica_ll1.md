# Gramática LL(1), FIRST, FOLLOW e Tabela de Análise

## Regras de Produção
- `programa -> inicio lista_comandos fim EOF`
- `inicio -> START_STMT`
- `fim -> END_STMT`
- `lista_comandos -> comando lista_comandos | ε`
- `comando -> expressao | decisao | laco`
- `expressao -> LPAREN conteudo_expr RPAREN`
- `conteudo_expr -> operando | operando MEM | operando RES | operando IDENTIFIER | operando operando OPERATOR | operando operando REL_OPERATOR`
- `operando -> NUMBER | IDENTIFIER | MEM | expressao`
- `decisao -> LPAREN expressao bloco IF RPAREN`
- `laco -> LPAREN expressao bloco WHILE RPAREN`
- `bloco -> LPAREN lista_comandos RPAREN`

## FIRST
- `FIRST(programa) = {START_STMT}`
- `FIRST(inicio) = {START_STMT}`
- `FIRST(fim) = {END_STMT}`
- `FIRST(lista_comandos) = {LPAREN, ε}`
- `FIRST(comando) = {LPAREN}`
- `FIRST(expressao) = {LPAREN}`
- `FIRST(conteudo_expr) = {IDENTIFIER, LPAREN, MEM, NUMBER}`
- `FIRST(operando) = {IDENTIFIER, LPAREN, MEM, NUMBER}`
- `FIRST(decisao) = {LPAREN}`
- `FIRST(laco) = {LPAREN}`
- `FIRST(bloco) = {LPAREN}`

## FOLLOW
- `FOLLOW(programa) = {EOF}`
- `FOLLOW(inicio) = {END_STMT, LPAREN}`
- `FOLLOW(fim) = {EOF}`
- `FOLLOW(lista_comandos) = {END_STMT, RPAREN}`
- `FOLLOW(comando) = {END_STMT, LPAREN, RPAREN}`
- `FOLLOW(expressao) = {END_STMT, IDENTIFIER, LPAREN, MEM, NUMBER, OPERATOR, REL_OPERATOR, RES, RPAREN}`
- `FOLLOW(conteudo_expr) = {RPAREN}`
- `FOLLOW(operando) = {IDENTIFIER, LPAREN, MEM, NUMBER, OPERATOR, REL_OPERATOR, RES, RPAREN}`
- `FOLLOW(decisao) = {END_STMT, LPAREN, RPAREN}`
- `FOLLOW(laco) = {END_STMT, LPAREN, RPAREN}`
- `FOLLOW(bloco) = {IF, WHILE}`

## Tabela LL(1)
- `M[programa, START_STMT] = inicio lista_comandos fim EOF`
- `M[inicio, START_STMT] = START_STMT`
- `M[fim, END_STMT] = END_STMT`
- `M[lista_comandos, LPAREN] = comando lista_comandos`
- `M[lista_comandos, END_STMT] = ε`
- `M[lista_comandos, RPAREN] = ε`
- `M[comando, LPAREN] = laco`
- `M[expressao, LPAREN] = LPAREN conteudo_expr RPAREN`
- `M[conteudo_expr, NUMBER] = operando operando REL_OPERATOR`
- `M[conteudo_expr, MEM] = operando operando REL_OPERATOR`
- `M[conteudo_expr, IDENTIFIER] = operando operando REL_OPERATOR`
- `M[conteudo_expr, LPAREN] = operando operando REL_OPERATOR`
- `M[operando, NUMBER] = NUMBER`
- `M[operando, IDENTIFIER] = IDENTIFIER`
- `M[operando, MEM] = MEM`
- `M[operando, LPAREN] = expressao`
- `M[decisao, LPAREN] = LPAREN expressao bloco IF RPAREN`
- `M[laco, LPAREN] = LPAREN expressao bloco WHILE RPAREN`
- `M[bloco, LPAREN] = LPAREN lista_comandos RPAREN`

## Conflitos
- `(('comando', 'LPAREN'), ['expressao'], ['decisao'])`
- `(('comando', 'LPAREN'), ['decisao'], ['laco'])`
- `(('conteudo_expr', 'NUMBER'), ['operando'], ['operando', 'MEM'])`
- `(('conteudo_expr', 'MEM'), ['operando'], ['operando', 'MEM'])`
- `(('conteudo_expr', 'IDENTIFIER'), ['operando'], ['operando', 'MEM'])`
- `(('conteudo_expr', 'LPAREN'), ['operando'], ['operando', 'MEM'])`
- `(('conteudo_expr', 'NUMBER'), ['operando', 'MEM'], ['operando', 'RES'])`
- `(('conteudo_expr', 'MEM'), ['operando', 'MEM'], ['operando', 'RES'])`
- `(('conteudo_expr', 'IDENTIFIER'), ['operando', 'MEM'], ['operando', 'RES'])`
- `(('conteudo_expr', 'LPAREN'), ['operando', 'MEM'], ['operando', 'RES'])`
- `(('conteudo_expr', 'NUMBER'), ['operando', 'RES'], ['operando', 'IDENTIFIER'])`
- `(('conteudo_expr', 'MEM'), ['operando', 'RES'], ['operando', 'IDENTIFIER'])`
- `(('conteudo_expr', 'IDENTIFIER'), ['operando', 'RES'], ['operando', 'IDENTIFIER'])`
- `(('conteudo_expr', 'LPAREN'), ['operando', 'RES'], ['operando', 'IDENTIFIER'])`
- `(('conteudo_expr', 'NUMBER'), ['operando', 'IDENTIFIER'], ['operando', 'operando', 'OPERATOR'])`
- `(('conteudo_expr', 'MEM'), ['operando', 'IDENTIFIER'], ['operando', 'operando', 'OPERATOR'])`
- `(('conteudo_expr', 'IDENTIFIER'), ['operando', 'IDENTIFIER'], ['operando', 'operando', 'OPERATOR'])`
- `(('conteudo_expr', 'LPAREN'), ['operando', 'IDENTIFIER'], ['operando', 'operando', 'OPERATOR'])`
- `(('conteudo_expr', 'NUMBER'), ['operando', 'operando', 'OPERATOR'], ['operando', 'operando', 'REL_OPERATOR'])`
- `(('conteudo_expr', 'MEM'), ['operando', 'operando', 'OPERATOR'], ['operando', 'operando', 'REL_OPERATOR'])`
- `(('conteudo_expr', 'IDENTIFIER'), ['operando', 'operando', 'OPERATOR'], ['operando', 'operando', 'REL_OPERATOR'])`
- `(('conteudo_expr', 'LPAREN'), ['operando', 'operando', 'OPERATOR'], ['operando', 'operando', 'REL_OPERATOR'])`
