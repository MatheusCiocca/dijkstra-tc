# Complexidade e pertinência à classe P

[← Voltar ao README](../README.md)

## Limites desta implementação

Nesta implementação Python, selecionar o próximo vértice custa `O(V)` e
ocorre no máximo `V` vezes. Cada aresta é examinada no máximo uma vez na busca;
a validação inicial também percorre vértices e arestas. Assim:

- **Tempo:** `O(V² + E)`, ou `O(V²)` no grafo simples representado aqui.
- **Espaço auxiliar:** `O(V)` para distâncias, prioridades, predecessores e visitados.
- **Armazenamento da entrada:** `O(V + E)` para as listas de adjacência.

Esses limites contam operações aritméticas e acessos a dicionários/conjuntos
com custo constante esperado. Inteiros muito grandes exigem considerar o
custo em bits das somas e comparações, que continua polinomial no tamanho da
entrada. Para pesos inteiros codificados em binário com até `b` bits, uma
distância ótima finita pode ser representada com `O(b + log V)` bits, pois há
um caminho ótimo simples com no máximo `V-1` arestas. Pesos racionais com
codificação finita também admitem aritmética exata de custo polinomial.

## Por que o problema está em P

Formalmente, **P é uma classe de problemas de decisão**. A pergunta
“existe caminho de `s` até `t` com custo no máximo `K`?” pertence a P:
calculamos as distâncias e verificamos se `δ(s,t) ≤ K`. A versão que calcula
as distâncias é um problema de função resolvido em tempo polinomial (FP).
É nesse sentido que o problema de otimização do trabalho é tratável em tempo
polinomial. Para as definições, veja a [aula de complexidade do MIT](https://courses.csail.mit.edu/6.006/fall11/lectures/lecture23.pdf).

## Observação sobre implementações alternativas

Uma versão com heap binário e operações adequadas pode atingir
`O((V + E) log V)`. O Python deste trabalho usa seleção linear para facilitar
a explicação; os tempos medidos não substituem a análise assintótica.

## Próximos tópicos

- [Relatórios, métricas e visualização](relatorios.md)
- [Aplicações](aplicacoes.md)
