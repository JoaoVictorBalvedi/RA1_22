# Ultima execucao

Arquivo de entrada: `teste1.txt`
Assembly gerado: `teste1.s`
Total de tokens: 85
Total de comandos na AST: 14

## Derivacao registrada

- programa -> inicio comandos fim EOF
- inicio -> START_LINE
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> NUMBER
- resto_estrutura -> IDENT_ASSIGN RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> NUMBER
- resto_estrutura -> IDENT_ASSIGN RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> NUMBER
- elemento -> NUMBER
- resto_estrutura -> elemento OPERATOR RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento REL_OPERATOR RPAREN
- elemento -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> IDENT_REST
- resto_estrutura -> elemento OPERATOR RPAREN
- resto_estrutura -> elemento IF RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> NUMBER
- resto_estrutura -> elemento REL_OPERATOR RPAREN
- elemento -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> IDENT_ELEM
- elemento -> NUMBER
- resto_estrutura -> elemento OPERATOR RPAREN
- resto_estrutura -> IDENT_ASSIGN RPAREN
- resto_estrutura -> elemento WHILE RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> NUMBER
- resto_estrutura -> RES RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> NUMBER
- resto_estrutura -> MEM_ASSIGN RPAREN
- comando -> estrutura_parentesizada
- estrutura_parentesizada -> LPAREN elemento resto_estrutura
- elemento -> MEM_ELEM
- resto_estrutura -> RPAREN
- fim -> END_LINE

## Resultado

- Analise lexica concluida com sucesso.
- Analise sintatica LL(1) concluida com sucesso.
- Arvore sintatica gerada em `arvore_sintatica.json`.
- Codigo Assembly gerado em `teste1.s`.
