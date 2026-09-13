# Aplicações: como modelar situações reais

[← Voltar ao README](../README.md)

| Situação | Vértices | Arestas e pesos | Utilidade da fonte única |
|---|---|---|---|
| Entregas a partir de um depósito | Cruzamentos e endereços | Ruas, com distância ou tempo não negativo | Calcular custos mínimos do depósito até cada endereço. |
| Comunicação em rede | Roteadores | Conexões, com latência ou custo administrativo não negativo | Obter custos de encaminhamento a partir de um roteador. |
| Deslocamento em jogos | Posições ou regiões | Movimentos, com custo de terreno | Encontrar posições mais baratas de alcançar a partir do personagem. |

São modelos ilustrativos. Os pesos são considerados fixos durante uma busca.
O algoritmo não resolve, por si só, a ordem de visita de várias entregas, nem
adapta rotas automaticamente a alterações de trânsito.

## Próximos tópicos

- [Problema, entrada e restrições](problema.md)
- [Formatos de entrada e datasets](datasets.md)
