"""Demonstração isolada da falha de Dijkstra com peso negativo, fora das
restrições do projeto."""

from math import inf


def demonstrar_falha_com_peso_negativo() -> dict[str, int | float]:
    """Roda Dijkstra sem validação sobre um grafo com peso negativo e retorna as
    distâncias.

    Reproduz o contraexemplo do README: a aresta negativa ``C -> B`` melhora
    um vértice (``B``) já fixado, invalidando o argumento de correção do
    algoritmo. O resolvedor principal (:mod:`caminhos_minimos`) rejeita essa
    entrada antes de iniciar a busca; esta função existe só para ilustrar o
    erro que ocorreria sem essa validação.
    """
    grafo = {"A": {"B": 2, "C": 5}, "B": {"D": 2}, "C": {"B": -4}, "D": {}}
    distancias = dict.fromkeys(grafo, inf)
    distancias["A"] = 0
    fixados: set[str] = set()
    while len(fixados) < len(grafo):
        atual = min(
            (vertice for vertice in grafo if vertice not in fixados),
            key=distancias.__getitem__,
        )
        fixados.add(atual)
        for vizinho, peso in grafo[atual].items():
            if vizinho not in fixados:
                distancias[vizinho] = min(distancias[vizinho], distancias[atual] + peso)
    return distancias


if __name__ == "__main__":
    print("Demonstração fora das restrições: A→B=2, A→C=5, C→B=-4, B→D=2")
    print(f"Dijkstra sem validação: {demonstrar_falha_com_peso_negativo()}")
    print("Resultado correto: A=0, B=1, C=5, D=3 (caminho A→C→B→D).")
    print("O resolvedor do projeto rejeita essa entrada antes da busca.")
