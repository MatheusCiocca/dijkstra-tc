# Bônus: A* e heurísticas

[← Voltar ao README](../README.md)

As funções `a_estrela()` e `a_estrela_distancias()` ficam em
`complementos/a_estrela.py`. Para usar a API diretamente:

```python
from complementos.a_estrela import a_estrela, a_estrela_distancias
```

## Requisito da heurística

A* prioriza `f(v) = g(v) + h(v)`: custo já percorrido mais estimativa até o
destino. Como a implementação não reabre vértices fixados, exige uma
heurística **consistente**: `h(u) ≤ w(u,v) + h(v)` para toda aresta, com
`h(destino)=0` e valores finitos não negativos. A validação verifica essas
condições no grafo inteiro. Apenas ser admissível (não superestimar o custo
restante) não basta para esta versão sem reabertura. Veja as
[notas de busca informada da UC Berkeley](https://inst.eecs.berkeley.edu/~cs188/fa22/assets/notes/cs188-fa22-note02.pdf).

Sem `--heuristica`, usa-se `h=0`, equivalente a Dijkstra, inclusive na ordem de
visita com os mesmos empates. Pequenas diferenças de tempo não demonstram
superioridade do A*. Ambos compartilham o núcleo de busca.

## Exemplo didático

```bash
python main.py exemplos/desvios.json A D \
  --heuristica exemplos/heuristica_desvios.json \
  --relatorio resultados/heuristica.json \
  --comparacao resultados/heuristica.png
```

Na consulta isolada até D, `a_estrela()` fixa 3 vértices e
`dijkstra_com_caminho()` fixa 4; ambos encontram `A → C → D`, de custo 4.
Já a avaliação acima mede o vetor completo: `a_estrela_distancias()` continua
após D, processando todos os vértices alcançáveis, assim como Dijkstra.

O arquivo de heurística contém estimativas para **esse destino D**:
`A=4, B=10, C=2, D=0`. Esses valores foram calculados manualmente para um exemplo
pequeno e não representam o custo de construir uma heurística em uma aplicação
real. Menos vértices fixados não garante menor tempo total, pois há validação
adicional. Com estimativa `O(1)` por vértice, ambos mantêm o limite
`O(V² + E)` nesta implementação sobre um grafo explícito.

## Próximos tópicos

- [Algoritmo e correção](algoritmo.md)
- [Complexidade e classe P](complexidade.md)
