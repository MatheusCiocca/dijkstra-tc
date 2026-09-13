# Uso da linha de comando

[← Voltar ao README](../README.md)

Todos os comandos são executados a partir da raiz do projeto. A instalação
mínima está no [README](../README.md#execução); esta página detalha as opções.

## Opções disponíveis

```text
python main.py CONJUNTO_DADOS ORIGEM [DESTINO] [opções]
```

| Argumento | Descrição |
|---|---|
| `conjunto_dados` | Arquivo `.json` ou `.csv` com o grafo. |
| `origem` | Vértice de origem da busca. |
| `destino` | Opcional. Destino da heurística; ativa a comparação com A*. |
| `--relatorio` | Caminho do relatório. Padrão: `resultados/relatorio.json`. A extensão define o formato (`.json`, `.csv`, `.html`). |
| `--grafico` | Imagem do grafo, por exemplo `resultados/grafo.png`. |
| `--comparacao` | Imagem com os tempos de cálculo do vetor completo. |
| `--repeticoes` | Número de medições por algoritmo. Padrão: `7`. |
| `--heuristica` | JSON com a estimativa de cada vértice até o destino. Exige `destino`. |

Use `python main.py --help` para listar as opções. Um arquivo existente no
caminho do relatório será substituído. A pasta do relatório é criada
automaticamente; para as imagens, crie a pasta de saída previamente.
As opções antigas `--report` e `--plot` continuam aceitas por compatibilidade,
mas os exemplos usam português.

## Resolver o enunciado: uma origem, todos os vértices

```bash
python main.py exemplos/grafo.json 0 --relatorio resultados/distancias.json
```

Distâncias esperadas:

| Vértice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Distância | 0 | 2 | 5 | 1 | 4 | 5 | 5 | 8 | 10 | 9 |

A função equivalente é `dijkstra(grafo, origem)`, em `caminhos_minimos/algoritmos.py`.
Ela e `buscar(grafo, origem)` retornam uma lista com todas as distâncias definitivas:

```python
[0, 2, 5, 1, 4, 5, 5, 8, 10, 9]
```

A posição `i` corresponde ao vértice `list(grafo)[i]`; a ordem não é ordenada
automaticamente pelo nome do vértice. A origem tem distância zero e vértices
inalcançáveis recebem `math.inf`. O terminal mostra os vértices e o vetor nessa ordem.
O relatório contém uma linha por algoritmo, com o vetor completo, a ordem dos
vértices e as métricas de tempo. Sem destino, avalia somente Dijkstra.

## Comparar o vetor completo com Dijkstra e A*

```bash
python main.py exemplos/grafo.json 0 9 \
  --repeticoes 15 \
  --relatorio resultados/comparacao.json \
  --grafico resultados/grafo.png \
  --comparacao resultados/metricas.png
```

O terminal mostra **todas** as distâncias. Neste modo, o relatório contém duas
linhas, uma por algoritmo, com o mesmo vetor completo. O destino `9` orienta a
heurística do A*, mas a busca continua até esgotar os vértices alcançáveis.
Todas as execuções medidas calculam o vetor inteiro a partir da mesma origem.

Quando solicitado com `--grafico`, o caminho `0 → 3 → 4 → 6 → 7 → 9`, de custo 9,
é reconstruído separadamente para destaque na imagem, fora da medição.
`dijkstra_com_caminho()` e `a_estrela()` retornam o custo até esse destino,
o caminho e a contagem de vértices fixados. O estado parcial dessas consultas
fica interno. `buscar()`, `dijkstra()` e `a_estrela_distancias()` entregam o
vetor completo; a avaliação usa as duas últimas funções.

## API Python

```python
from caminhos_minimos.algoritmos import dijkstra
from caminhos_minimos.ler_salvar_grafos import carregar_grafo, salvar_grafo

grafo = carregar_grafo("exemplos/grafo.json")
distancias = dijkstra(grafo, "0")
salvar_grafo(grafo, "resultados/copia.csv")
```

## VS Code

Com as extensões Python e Python Debugger, selecione o ambiente `.venv` e
execute a configuração **Depurar caminhos mínimos** com F5. Ela chama `main.py`
com `exemplos/grafo.json`, origem `0`, e salva o relatório em
`resultados/distancias.json`. A descoberta de testes usa `pytest` em `tests/`.

## Docker: execução manual

O script `executar_docker.bash` cobre o fluxo completo. Para uma consulta
avulsa em Linux/macOS:

```bash
mkdir -p resultados
docker build -t caminhos-minimos .
docker run --rm --user "$(id -u):$(id -g)" -e MPLCONFIGDIR=/tmp/matplotlib \
  -v "$(pwd):/app" caminhos-minimos exemplos/grafo.json 0 \
  --relatorio resultados/distancias.json
docker run --rm --user "$(id -u):$(id -g)" -e MPLCONFIGDIR=/tmp/matplotlib \
  -v "$(pwd):/app" caminhos-minimos exemplos/grafo.csv A D \
  --relatorio resultados/comparacao.json --comparacao resultados/metricas.png
```

Os relatórios e gráficos ficam na pasta `resultados/` do projeto. A opção
`--user` evita criar relatórios pertencentes ao usuário root do contêiner.
A imagem usa Python 3.11 e inclui o programa, seus complementos, os exemplos e
as dependências de execução e visualização. Reconstrua a imagem após alterar o código.

### O que o script gera

`bash executar_docker.bash` constrói a imagem, calcula as distâncias, compara
Dijkstra e A*, gera relatórios JSON/CSV/HTML e gráficos, executa os exemplos de
heurística, grafo desconexo e pesos negativos e gera seis datasets com semente 42.
Em seguida, resolve cada dataset com Dijkstra a partir da origem `0` e salva as
distâncias em `resultados/respostas/`, em JSON e TXT. Também desenha cada um dos
seis grafos em `resultados/grafos/`. Arquivos com o mesmo nome são substituídos.
Use `bash executar_docker.bash --help` para consultar a ajuda.

Imagens produzidas:

- `resultados/grafo.png`: grafo com o caminho mínimo destacado.
- `resultados/metricas.png`: tempo mediano e desvio padrão de Dijkstra e A*.
- `resultados/desvios.png` e `resultados/heuristica.png`: caminho e comparação com heurística.
- `resultados/desconexo.png`: grafo com destino inalcançável.
- `resultados/grafos/grafo_<vertices>_<densidade>.png`: imagem de cada um dos seis datasets.

## Próximos tópicos

- [Formatos de entrada e datasets](datasets.md)
- [Relatórios, métricas e visualização](relatorios.md)
