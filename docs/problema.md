# Problema, entrada e restrições

[← Voltar ao README](../README.md)

Dado um grafo ponderado e uma origem, queremos minimizar a **soma dos pesos**
das arestas percorridas. Minimizar o número de arestas é outro objetivo:
`A → B`, de custo 4, tem menos arestas que `A → C → B`, de custo `1 + 2 = 3`,
mas é mais caro.

## Definição formal

| Elemento | Definição |
|---|---|
| Problema | Encontrar a menor distância de uma origem até cada vértice. |
| Instância | Um grafo finito `G = (V, E)`, uma função de pesos `w` e uma origem `s ∈ V`. |
| Entrada | Dicionário de adjacência ou arquivo JSON/CSV com pesos não negativos, mais a origem. |
| Saída | Vetor de distâncias mínimas da origem até todos os vértices, na ordem de inserção das chaves do grafo. |
| Sem caminho | Infinito na API Python; `null` no relatório JSON; “inalcançável” no terminal e nas tabelas. |
| Origem | Tem distância zero até si mesma, inclusive quando está isolada. |

## Restrições

Os vértices são textos não vazios, como `"A"` e `"0"`. Os pesos são inteiros
ou números de ponto flutuante finitos e não negativos; zero é permitido.
Booleanos, `NaN`, infinito e pesos negativos são rejeitados, mesmo em componentes
inalcançáveis. A origem e o destino opcional devem existir. Um grafo vazio pode
ser armazenado, mas não possui uma origem válida para executar a busca.

O grafo é **direcionado**. Para representar uma ligação nos dois sentidos,
informe ambas as arestas. São permitidos ciclos, laços e vértices isolados.
Há no máximo uma aresta por par ordenado: o CSV rejeita duplicatas, e as chaves
do JSON devem ser únicas. Ao usar a API, todos os destinos devem ser chaves do
dicionário; durante a importação, destinos implícitos são completados com `{}`.

## Precisão numérica

Para os experimentos e a análise exata, use pesos inteiros (por exemplo,
centavos ou metros). Decimais usam a aritmética aproximada de `float`; um
estouro numérico é reportado como erro. Os algoritmos não alteram o grafo recebido.

## Próximos tópicos

- [Algoritmo e correção](algoritmo.md)
- [Complexidade e classe P](complexidade.md)
- [Formatos de entrada e datasets](datasets.md)
