"""Consultas de caminhos mínimos com A*, com vetor completo ou caminho até um
destino."""

from caminhos_minimos.busca import executar_busca, reconstruir_caminho
from caminhos_minimos.grafo import Grafo, Heuristica, Peso


def a_estrela(
    grafo: Grafo,
    origem: str,
    destino: str,
    heuristica: Heuristica | None = None,
) -> tuple[Peso, list[str], int]:
    """Calcula, com A*, o custo e o caminho de ``origem`` até ``destino``.

    Sem ``heuristica``, o comportamento é equivalente a
    :func:`caminhos_minimos.algoritmos.dijkstra_com_caminho`. A heurística
    deve ser consistente; veja :func:`caminhos_minimos.busca.executar_busca`.
    """
    resultado = executar_busca(grafo, origem, destino, heuristica)
    caminho = reconstruir_caminho(resultado.anteriores, origem, destino)
    return resultado.distancias[destino], caminho, resultado.vertices_expandidos


def a_estrela_distancias(
    grafo: Grafo,
    origem: str,
    destino: str,
    heuristica: Heuristica | None = None,
) -> list[Peso]:
    """Calcula, com A*, a distância mínima de ``origem`` até cada vértice.

    Diferente de :func:`a_estrela`, não interrompe a busca ao fixar
    ``destino``: continua até esgotar os vértices alcançáveis, para permitir a
    comparação do vetor completo com Dijkstra. ``destino`` orienta apenas a
    heurística.
    """
    resultado = executar_busca(
        grafo, origem, destino, heuristica, parar_no_destino=False
    )
    return [resultado.distancias[vertice] for vertice in grafo]
