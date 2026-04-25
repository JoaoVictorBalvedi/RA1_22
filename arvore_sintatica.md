# Arvore Sintatica

Gerada a partir do arquivo `teste1.txt`.

## Codigo-fonte

```
(START)
(10 X)
(20 Y)
(X Y +)
(Y X -)
(X Y *)
(Y X |)
(Y X /)
(Y X %)
(2.0 3 ^)
((X Y <) (X Y +) IF)
((X 12 <) ((X 1 +) X) WHILE)
(1 RES)
(99.9 MEM)
(MEM)
(END)
```

## Representacao em arvore

**programa** (14 comandos)
  - *comando 0:*
    var_escrita: `X`
      - *valor:*
        numero: `10`
  - *comando 1:*
    var_escrita: `Y`
      - *valor:*
        numero: `20`
  - *comando 2:*
    operacao: `+`
      - *esquerda:*
        var_leitura: `X`
      - *direita:*
        var_leitura: `Y`
  - *comando 3:*
    operacao: `-`
      - *esquerda:*
        var_leitura: `Y`
      - *direita:*
        var_leitura: `X`
  - *comando 4:*
    operacao: `*`
      - *esquerda:*
        var_leitura: `X`
      - *direita:*
        var_leitura: `Y`
  - *comando 5:*
    operacao: `|`
      - *esquerda:*
        var_leitura: `Y`
      - *direita:*
        var_leitura: `X`
  - *comando 6:*
    operacao: `/`
      - *esquerda:*
        var_leitura: `Y`
      - *direita:*
        var_leitura: `X`
  - *comando 7:*
    operacao: `%`
      - *esquerda:*
        var_leitura: `Y`
      - *direita:*
        var_leitura: `X`
  - *comando 8:*
    operacao: `^`
      - *esquerda:*
        numero: `2.0`
      - *direita:*
        numero: `3`
  - *comando 9:*
    if
      - *condicao:*
        comparacao: `<`
          - *esquerda:*
            var_leitura: `X`
          - *direita:*
            var_leitura: `Y`
      - *comando:*
        operacao: `+`
          - *esquerda:*
            var_leitura: `X`
          - *direita:*
            var_leitura: `Y`
  - *comando 10:*
    while
      - *condicao:*
        comparacao: `<`
          - *esquerda:*
            var_leitura: `X`
          - *direita:*
            numero: `12`
      - *comando:*
        var_escrita: `X`
          - *valor:*
            operacao: `+`
              - *esquerda:*
                var_leitura: `X`
              - *direita:*
                numero: `1`
  - *comando 11:*
    res: `1`
  - *comando 12:*
    mem_escrita
      - *valor:*
        numero: `99.9`
  - *comando 13:*
    mem_leitura

## JSON completo

Ver arquivo `arvore_sintatica.json` para a representacao completa em JSON.
