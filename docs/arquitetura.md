# Arquitetura, organização e SOLID

[← Voltar ao README](../README.md)

## Estrutura de pastas

```text
.
├── caminhos_minimos/       # Dijkstra, estrutura do grafo, leitura e gravação
├── complementos/           # A*, avaliação, datasets, relatórios e gráficos
├── docs/                   # Documentação por tópico
├── exemplos/               # Grafos de entrada e demonstrações
├── tests/                  # Testes unitários e de integração
├── resultados/             # Arquivos gerados (criado na execução)
├── main.py
├── Dockerfile
├── executar_docker.bash
├── requirements.txt
└── requirements-dev.txt
```

Execute os comandos a partir da raiz. Para usar a API Python, importe o pacote,
por exemplo: `from caminhos_minimos.algoritmos import dijkstra`.

## Responsabilidade de cada arquivo

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada, argumentos, coordenação e mensagens do terminal. |
| `caminhos_minimos/grafo.py` | Tipos e validação pura das restrições. |
| `caminhos_minimos/algoritmos.py` | Consultas com Dijkstra, com vetor completo ou caminho até um destino. |
| `caminhos_minimos/_busca.py` | Núcleo interno de busca, validação de heurísticas e reconstrução de caminhos, compartilhado por Dijkstra e A*. |
| `caminhos_minimos/ler_salvar_grafos.py` | Leitura e gravação de grafos em arquivos JSON e CSV. |
| `complementos/a_estrela.py` | Consultas complementares com A*, com vetor completo ou caminho até um destino. |
| `complementos/avaliacao.py` | Medição de algoritmos recebidos como funções e textos dos limites teóricos usados nos relatórios. |
| `complementos/relatorios.py` | Exportação das tabelas em três formatos. |
| `complementos/visualizacao.py` | Desenho dos grafos e das métricas. |
| `complementos/gerar_dataset.py` | Geração e gravação de datasets de grafos aleatórios em JSON. |
| `exemplos/contraexemplo.py` | Demonstração isolada da falha com peso negativo. |
| `tests/test_dijkstra.py`, `tests/test_recursos.py` | Testes unitários e de integração. |
| `requirements.txt`, `Dockerfile`, `.dockerignore` | Dependências e ambiente Docker. |
| `executar_docker.bash` | Construção da imagem e execução dos exemplos, gráficos com Matplotlib e datasets. |
| `requirements-dev.txt` | Dependências para testes, análise estática e formatação. |
| `.gitignore`, `.vscode/` | Exclusão de arquivos gerados e configuração opcional do editor. |

## Dependências

As versões das dependências diretas estão fixadas em `requirements.txt`;
dependências transitivas e o sistema operacional ainda podem variar.
O núcleo dos algoritmos usa apenas a **biblioteca padrão**; Matplotlib e
NetworkX são usados para gráficos, e NetworkX também fornece uma referência
independente nos testes.

## Convenções de nomes

Os nomes próprios do projeto usam português, `snake_case` e anotações de tipo.
Nomes obrigatórios de bibliotecas e ferramentas (`main.py`, `test_`, `weight`,
`Dockerfile`, `README.md`) seguem suas convenções. Os módulos Python ficam nos
pacotes `caminhos_minimos` e `complementos`.

## SOLID

A separação de responsabilidades aplica **SRP**. A avaliação recebe funções
com o mesmo contrato, permitindo acrescentar algoritmos sem alterar o medidor
(**OCP** e redução do acoplamento conforme **DIP**). Os algoritmos compartilham
a busca para evitar duplicação. **LSP** e **ISP** são princípios voltados a
subtipos e interfaces; aqui não há hierarquia de herança que exija essa análise.
Não se declara uma certificação “100% SOLID”: a organização é modular e
proporcional ao trabalho acadêmico, com funções pequenas e contratos explícitos.

## Próximos tópicos

- [Testes e verificação](testes.md)
- [Uso da linha de comando](uso.md)
