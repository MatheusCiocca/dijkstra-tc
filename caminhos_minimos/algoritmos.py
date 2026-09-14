"""Consultas de caminhos mínimos com Dijkstra: vetor completo ou caminho até um
destino."""

from caminhos_minimos.busca import executar_busca, reconstruir_caminho
from caminhos_minimos.grafo import Grafo, Peso


def buscar(grafo: Grafo, origem: str) -> list[Peso]:
    """Calcula, com Dijkstra, a distância mínima de ``origem`` até cada vértice.

    Retorna um vetor na ordem das chaves de ``grafo``; vértices inalcançáveis
    recebem ``math.inf``.
    """
    resultado = executar_busca(grafo, origem)
    return [resultado.distancias[vertice] for vertice in grafo]


def dijkstra(grafo: Grafo, origem: str) -> list[Peso]:
    """Alias de :func:`buscar`, usado pela avaliação e pelo relatório do enunciado."""
    return buscar(grafo, origem)


def dijkstra_com_caminho(
    grafo: Grafo, origem: str, destino: str
) -> tuple[Peso, list[str], int]:
    """Calcula, com Dijkstra, o custo e o caminho de ``origem`` até ``destino``.

    Encerra a busca assim que ``destino`` é fixado. Retorna o custo mínimo, o
    caminho como lista de vértices (vazia se inalcançável) e a quantidade de
    vértices fixados até a parada.
    """
    resultado = executar_busca(grafo, origem, destino)
    caminho = reconstruir_caminho(resultado.anteriores, origem, destino)
    return resultado.distancias[destino], caminho, resultado.vertices_expandidos
