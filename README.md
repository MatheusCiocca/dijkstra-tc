# Caminhos mínimos de fonte única com pesos não negativos

Trabalho de Teoria da Computação.
Implementação de **Dijkstra** em Python, com comparação complementar com **A\***.

Dado um grafo direcionado com pesos não negativos e um vértice de origem, o
programa calcula a menor distância da origem até **todos** os vértices, exporta
relatórios em JSON/CSV/HTML e gera gráficos.

## Execução

### Com Docker (recomendado)

Com o Docker instalado e em execução, a partir da raiz do projeto:

```bash
bash executar_docker.bash
```

O script constrói a imagem e executa todos os exemplos, datasets e gráficos.
As saídas ficam em `resultados/`. Use `--help` para ver a ajuda.

### Com Python

Requer **Python 3.10 ou posterior**. Em Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p resultados
```

No Windows, crie o ambiente com `py -m venv .venv` e ative com
`.venv\Scripts\Activate.ps1` no PowerShell.

Execução mínima — uma origem, todos os vértices:

```bash
python main.py exemplos/grafo.json 0 --relatorio resultados/distancias.json
```

Saída esperada:

| Vértice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Distância | 0 | 2 | 5 | 1 | 4 | 5 | 5 | 8 | 10 | 9 |

Comparando Dijkstra e A\* com gráficos:

```bash
python main.py exemplos/grafo.json 0 9 \
  --relatorio resultados/comparacao.json \
  --grafico resultados/grafo.png \
  --comparacao resultados/metricas.png
```

Todas as opções: `python main.py --help` ou [Uso da linha de comando](docs/uso.md).

### Testes

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Documentação

| Tópico | Conteúdo |
|---|---|
| [Problema, entrada e restrições](docs/problema.md) | Definição formal, formatos aceitos e limites da entrada. |
| [Algoritmo e correção](docs/algoritmo.md) | Passo a passo, prova da escolha gulosa e contraexemplo com peso negativo. |
| [Complexidade e classe P](docs/complexidade.md) | Limites de tempo e espaço, e por que o problema é tratável. |
| [Uso da linha de comando](docs/uso.md) | Todas as opções, API Python, VS Code e Docker manual. |
| [Formatos e datasets](docs/datasets.md) | JSON e CSV, exemplos incluídos e geração reproduzível. |
| [Relatórios e visualização](docs/relatorios.md) | Campos das métricas, formatos de saída e gráficos. |
| [A\* e heurísticas](docs/a-estrela.md) | Bônus: consistência da heurística e exemplo didático. |
| [Aplicações](docs/aplicacoes.md) | Como modelar situações reais com fonte única. |
| [Arquitetura e SOLID](docs/arquitetura.md) | Estrutura de pastas, responsabilidades e princípios. |
| [Testes e verificação](docs/testes.md) | Suíte de testes, análise estática e cobertura. |

## Estrutura do projeto

```text
.
├── caminhos_minimos/   # Dijkstra, grafo, leitura e gravação
├── complementos/       # A*, avaliação, datasets, relatórios e gráficos
├── docs/               # Documentação por tópico
├── exemplos/           # Grafos de entrada e demonstrações
├── tests/              # Testes
└── main.py             # Ponto de entrada
```

## Integrantes

| Integrante | Matrícula |
|---|---:|
| Mariana Padilha | 2410100712 |
| Emanuel Carricio | 2310100403 |
| Matheus Ciocca | 2310101609 |
| Rafaela Nunes | 2510101040 |
| Livia Barbosa | 2310100418 |
