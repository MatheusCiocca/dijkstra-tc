# Formatos de entrada e datasets

[← Voltar ao README](../README.md)

## Formatos aceitos

JSON preferencial: objeto de adjacência, como `exemplos/grafo.json`:

```json
{"A": {"B": 4, "C": 1}, "B": {"D": 1}, "C": {"B": 2, "D": 5}, "D": {}}
```

Também se aceita um envelope com a única chave `grafo` ou `graph` contendo
um grafo não vazio. CSV preferencial: `origem,destino,peso`, nesta ordem:

```csv
origem,destino,peso
A,B,4
A,C,1
B,D,1
C,B,2
C,D,5
isolado,,
```

Uma linha com destino e peso vazios declara um vértice isolado. O cabeçalho
antigo `source,target,weight` continua aceito. A gravação usa português.

## Datasets incluídos

| Dataset | Características | Consulta sugerida |
|---|---|---|
| `exemplos/grafo.json` | 10 vértices, 26 arcos com pesos não negativos | `0 → 9`, custo 9 |
| `exemplos/grafo.csv` | 4 vértices, 5 arcos; menos arestas não implica menor custo | `A → D`, custo 4 |
| `exemplos/desvios.json` | 4 vértices; permite demonstrar orientação por heurística | `A → D`, custo 4 |
| `exemplos/desconexo.json` | Aresta de custo zero e vértice isolado | `A → D`, inalcançável |

`exemplos/heuristica_desvios.json` é uma tabela de estimativas, não um grafo.
Os datasets são exemplos didáticos, não dados coletados de uma aplicação real.

## Geração de datasets reproduzíveis

```bash
python -m complementos.gerar_dataset --saida resultados/datasets --semente 42
```

Gera seis grafos: 10, 50 e 100 vértices, cada tamanho com probabilidade de aresta
0,1 e 0,5. Para cada par ordenado de vértices distintos, a inclusão de uma
aresta é sorteada independentemente; os pesos são inteiros de 1 a 100.
A geração custa `O(V²)`, pode produzir grafos desconexos e não garante caminhos.
A semente permite repetir os dados no mesmo ambiente Python.

A pasta recebe os seis datasets em JSON. A saída padrão é `resultados/datasets`.
O script cria a pasta de saída e substitui arquivos homônimos ao ser repetido.

Para usar a geração diretamente, importe `gerar_grafo_aleatorio` de
`complementos.gerar_dataset` e chame `gerar_grafo_aleatorio(50, 0.2, 42)`.

## Respostas dos datasets gerados

Esse comando gera apenas as entradas. `bash executar_docker.bash` também calcula
as respostas dos seis grafos usando Dijkstra, com origem `0`:

| Entrada em `resultados/datasets/` | Respostas em `resultados/respostas/` |
|---|---|
| `grafo_10_10.json` | `grafo_10_10.json` e `grafo_10_10.txt` |
| `grafo_10_50.json` | `grafo_10_50.json` e `grafo_10_50.txt` |
| `grafo_50_10.json` | `grafo_50_10.json` e `grafo_50_10.txt` |
| `grafo_50_50.json` | `grafo_50_50.json` e `grafo_50_50.txt` |
| `grafo_100_10.json` | `grafo_100_10.json` e `grafo_100_10.txt` |
| `grafo_100_50.json` | `grafo_100_50.json` e `grafo_100_50.txt` |

O TXT mostra as distâncias por vértice e o vetor completo. O JSON inclui as
distâncias, a ordem dos vértices e as métricas de execução. Vértices sem caminho
aparecem como `inalcançável` no TXT e `null` no JSON.

As imagens ficam em `resultados/grafos/`, com o mesmo nome do dataset e extensão
`.png`. Por exemplo, `grafo_100_50.json` gera `resultados/grafos/grafo_100_50.png`.
Sobre a omissão dos rótulos de peso em grafos densos, veja
[Relatórios e visualização](relatorios.md#por-que-os-pesos-não-aparecem-em-alguns-grafos).

Para resolver um dataset já gerado, diretamente com Python:

```bash
python main.py resultados/datasets/grafo_10_10.json 0 \
  --relatorio resultados/respostas/grafo_10_10.json
```

## Próximos tópicos

- [Relatórios, métricas e visualização](relatorios.md)
- [Uso da linha de comando](uso.md)
