# Funcionamento e correção de Dijkstra

[← Voltar ao README](../README.md)

## Passos do algoritmo

1. Inicializa a origem com distância zero e os demais vértices com infinito.
2. Seleciona, por busca linear, o vértice ainda não fixado de menor estimativa.
3. Se a menor estimativa é infinita, encerra: os restantes são inalcançáveis.
4. Fixa o vértice e relaxa suas arestas: se `d[u] + w(u,v) < d[v]`, atualiza
   a distância e registra `u` como predecessor de `v`.
5. Repete até esgotar os alcançáveis. Na consulta a um destino, pode parar
   quando esse destino é fixado.

## Execução passo a passo

Exemplo de `exemplos/grafo.csv`, origem A (valores após o relaxamento):

| Vértice fixado | d(A) | d(B) | d(C) | d(D) |
|---|---:|---:|---:|---:|
| Inicialização | 0 | ∞ | ∞ | ∞ |
| A | 0 | 4 | 1 | ∞ |
| C | 0 | 3 | 1 | 6 |
| B | 0 | 3 | 1 | 4 |
| D | 0 | 3 | 1 | 4 |

## Por que a escolha gulosa é segura?

O invariante é: **todo vértice fixado já tem sua distância mínima correta**.
A origem satisfaz essa propriedade, pois pesos não negativos não permitem
um caminho de custo menor que zero até ela.

Suponha que o próximo vértice escolhido, `u`, tivesse um caminho mais barato
que `d[u]`. Nesse caminho, considere o primeiro vértice ainda não fixado, `y`,
e seu predecessor já fixado, `x`. Ao processar `x`, o relaxamento já teria
atribuído a `y` uma estimativa no máximo igual ao custo do prefixo até `y`.
Como o restante do caminho tem custo não negativo, teríamos `d[y] < d[u]`.
Isso contradiz a escolha de `u` como menor estimativa. Logo, fixar `u` é seguro.
A explicação acompanha a [aula de Dijkstra do MIT](https://courses.csail.mit.edu/6.006/fall11/lectures/lecture16.pdf).

## Contraexemplo com peso negativo

Considere `A → B = 2`, `A → C = 5`, `C → B = -4` e `B → D = 2`.
Não existe ciclo nesse grafo.

Uma versão de Dijkstra que ignorasse a restrição fixaria A, B, D e C,
retornando `d(B)=2` e `d(D)=4`. Porém, `A → C → B` custa 1 e
`A → C → B → D` custa 3. A aresta negativa melhora um vértice já fixado,
invalidando o argumento anterior. Um peso negativo pode causar erro, mesmo
sem um ciclo negativo; isso não significa que toda entrada negativa falhe.

```bash
python exemplos/contraexemplo.py
```

Esse arquivo é uma demonstração deliberadamente incorreta fora das restrições.
O resolvedor principal rejeita a entrada antes de iniciar a busca.

## Próximos tópicos

- [Complexidade e classe P](complexidade.md)
- [A* e heurísticas](a-estrela.md)
