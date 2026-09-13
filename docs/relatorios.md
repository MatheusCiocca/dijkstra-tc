# Relatórios, métricas e visualização

[← Voltar ao README](../README.md)

## Campos do relatório

| Métrica/campo | Interpretação |
|---|---|
| `distancias` | Vetor com as distâncias mínimas da origem até todos os vértices. |
| `ordem_vertices` | Identifica o vértice correspondente a cada posição do vetor. |
| `tempo_execucao_ms` | Mediana das execuções medidas, em milissegundos. |
| `desvio_tempo_ms` | Desvio padrão populacional dos tempos, em milissegundos. |
| `repeticoes`, `vertices`, `arestas` | Número de medições e tamanho da instância; arcos opostos contam separadamente. |
| `origem`, `conjunto_dados` | Origem da busca completa e arquivo de entrada. |
| `destino_heuristica`, `heuristica` | Referência usada para ordenar a busca completa do A*; aparece na comparação. |
| `complexidade` | Limite teórico, não uma estimativa derivada do cronômetro. |

## Como os tempos são medidos

Há uma execução de aquecimento por algoritmo e sete repetições por padrão.
A ordem dos algoritmos alterna entre repetições. Cada chamada medida inclui
validação, busca completa e construção do vetor de distâncias. Para A*, inclui
também a avaliação e validação da heurística. Exclui leitura, impressão,
exportação, gráficos e a consulta separada usada para destacar um caminho.
Uma tabela de heurística já carregada não inclui no tempo o esforço de produzi-la.
Para conclusões mais gerais, varie sementes, tamanhos dos grafos e origens.

Uso direto da avaliação:

```python
from caminhos_minimos.algoritmos import dijkstra
from complementos.avaliacao import avaliar

resultados = avaliar(grafo, origem, {"dijkstra": dijkstra}, repeticoes=7)
```

Cada função recebida deve aceitar `(grafo, origem)` e retornar uma lista com
uma distância por vértice, na ordem das chaves do grafo. A avaliação verifica
o formato e a estabilidade entre execuções; essa verificação não prova a
correção matemática dos resultados.

## Formatos de saída

JSON mantém o vetor como lista e usa `null` para distância inalcançável.
CSV e HTML apresentam o vetor como texto, com `inalcançável` nas posições sem
caminho. O HTML escapa os dados de entrada. Para escolher o formato, altere a
extensão do `--relatorio`:

```bash
python main.py exemplos/grafo.csv A D --relatorio resultados/comparacao.csv
python main.py exemplos/grafo.csv A D --relatorio resultados/comparacao.html
python main.py exemplos/desconexo.json A D --relatorio resultados/desconexo.json
```

## Gráficos

`--grafico` desenha o grafo, preserva isolados e destaca o caminho selecionado
em vermelho. `--comparacao` gera barras de mediana e desvio padrão dos tempos
de cálculo do vetor completo; também pode ser usado sem destino para Dijkstra.
As imagens são salvas sem abrir uma janela; desenhos grandes podem ficar pouco
legíveis. O custo do posicionamento visual não está incluído na complexidade
de Dijkstra. Use `resultados/` para gerar relatórios e imagens.

### Por que os pesos não aparecem em alguns grafos?

Cada peso é escrito perto da aresta correspondente. Quando há muitas arestas,
as linhas se cruzam e os números ficam uns sobre os outros, dificultando
identificar a qual ligação cada valor pertence. Isso é a sobreposição de rótulos.

A visualização em `complementos/visualizacao.py` usa este critério:

- **Até 80 arestas:** mostra os pesos junto às arestas.
- **Mais de 80 arestas:** mantém todos os vértices e arestas, mas omite os
  rótulos dos pesos. Também aumenta a imagem, usa linhas mais finas e
  transparentes e distribui os vértices em círculo para facilitar a leitura.

O limite de 80 é uma escolha de apresentação, não uma restrição de Dijkstra.
Essa mudança afeta somente o desenho: todos os pesos continuam presentes no
dataset e são usados no cálculo das distâncias. Mesmo com esses ajustes,
grafos com milhares de arestas ainda podem ter muitas linhas sobrepostas.

Para consultar um peso exato, abra o JSON correspondente em
`resultados/datasets/`. Por exemplo, no trecho `"0": {"3": 12}`, a aresta
direcionada de `0` para `3` tem peso `12`. Já os arquivos em
`resultados/respostas/` mostram as menores distâncias acumuladas desde a
origem, que podem envolver várias arestas.

## Próximos tópicos

- [Complexidade e classe P](complexidade.md)
- [Testes e verificação](testes.md)
