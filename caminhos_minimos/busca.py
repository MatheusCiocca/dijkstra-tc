"""Núcleo interno de busca compartilhado por Dijkstra e A*.

Implementa a seleção gulosa do vértice de menor prioridade (distância, no caso
de Dijkstra; distância mais heurística, no caso de A*), a validação de
heurísticas consistentes e a reconstrução do caminho até um destino.

Detalhe de implementação usado por :mod:`caminhos_minimos.algoritmos` e por
:mod:`complementos.a_estrela`; não faz parte da API pública do projeto, que é
exposta por essas duas funções (``dijkstra``, ``dijkstra_com_caminho`` e
``a_estrela``).
"""

from dataclasses import dataclass
from math import inf

from caminhos_minimos.grafo import (
    Grafo,
    Heuristica,
    Peso,
    somar_custos,
    validar_grafo,
    validar_numero_nao_negativo,
)


@dataclass
class _ResultadoBusca:
    """Resultado bruto de uma busca: distâncias, predecessores e vértices fixados."""

    distancias: dict[str, Peso]
    anteriores: dict[str, str]
    vertices_expandidos: int


def reconstruir_caminho(
    anteriores: dict[str, str], origem: str, destino: str
) -> list[str]:
    """Reconstrói o caminho de ``origem`` até ``destino`` a partir dos predecessores.

    Retorna a lista vazia quando ``destino`` não foi alcançado pela busca.
    """
    if destino != origem and destino not in anteriores:
        return []
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anteriores[caminho[-1]])
    return list(reversed(caminho))


def _calcular_heuristica_consistente(
    grafo: Grafo, destino: str | None, heuristica: Heuristica | None
) -> dict[str, Peso]:
    """Calcula e valida as estimativas de heurística para todos os vértices.

    Sem ``heuristica``, retorna zero para todos os vértices (equivalente a
    Dijkstra). Com ``heuristica``, exige um ``destino``, valores não negativos,
    estimativa zero no destino e consistência (`h(u) <= w(u,v) + h(v)`) em
    todas as arestas do grafo.
    """
    if heuristica is None:
        return dict.fromkeys(grafo, 0)
    if destino is None:
        raise ValueError("a heurística exige um destino")
    estimativas = {vertice: heuristica(vertice, destino) for vertice in grafo}
    for estimativa in estimativas.values():
        validar_numero_nao_negativo(estimativa, "heurística")
    if estimativas[destino] != 0:
        raise ValueError("a heurística no destino deve ser zero")
    for origem, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            if estimativas[origem] > somar_custos(peso, estimativas[vizinho]):
                raise ValueError(
                    "a heurística deve ser consistente em todas as arestas"
                )
    return estimativas


def executar_busca(
    grafo: Grafo,
    origem: str,
    destino: str | None = None,
    heuristica: Heuristica | None = None,
    *,
    parar_no_destino: bool = True,
) -> _ResultadoBusca:
    """Executa a busca gulosa de fonte única (Dijkstra ou A*, conforme a heurística).

    A cada passo, fixa o vértice não visitado de menor prioridade (distância
    mais heurística) e relaxa suas arestas de saída. Sem ``heuristica``, o
    comportamento é o de Dijkstra puro. Com ``parar_no_destino=True``, encerra
    assim que ``destino`` é fixado; caso contrário, prossegue até esgotar os
    vértices alcançáveis, retornando o vetor completo de distâncias.
    """
    validar_grafo(grafo)
    if origem not in grafo:
        raise KeyError(f"vértice de origem inexistente: {origem!r}")
    if destino is not None and destino not in grafo:
        raise KeyError(f"vértice de destino inexistente: {destino!r}")
    estimativas = _calcular_heuristica_consistente(grafo, destino, heuristica)
    distancias = dict.fromkeys(grafo, inf)
    prioridades = dict.fromkeys(grafo, inf)
    anteriores: dict[str, str] = {}
    visitados: set[str] = set()
    distancias[origem] = 0
    prioridades[origem] = estimativas[origem]

    while len(visitados) < len(grafo):
        candidatos = (vertice for vertice in grafo if vertice not in visitados)
        atual = min(candidatos, key=prioridades.__getitem__, default=None)
        if atual is None or prioridades[atual] == inf:
            break
        visitados.add(atual)
        if parar_no_destino and atual == destino:
            break
        for vizinho, peso in grafo[atual].items():
            if vizinho in visitados:
                continue
            nova_distancia = somar_custos(distancias[atual], peso)
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                prioridades[vizinho] = somar_custos(
                    nova_distancia, estimativas[vizinho]
                )
                anteriores[vizinho] = atual
    return _ResultadoBusca(distancias, anteriores, len(visitados))
