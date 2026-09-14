"""Medição de algoritmos recebidos como funções e textos dos limites teóricos
usados nos relatórios."""

from collections.abc import Callable, Mapping
from statistics import median, pstdev
from time import perf_counter
from typing import Any

from caminhos_minimos.grafo import Grafo, Peso


def _aquecer_algoritmos(
    grafo: Grafo,
    origem: str,
    algoritmos: Mapping[str, Callable[[Grafo, str], list[Peso]]],
) -> dict[str, list[Peso]]:
    """Executa cada algoritmo uma vez (aquecimento) e valida o formato do retorno.

    Retorna o vetor de distâncias de cada algoritmo, usado como referência
    para checar a estabilidade entre repetições em :func:`_medir_tempos_execucao`.
    """
    quantidade_vertices = len(grafo)
    distancias_referencia = {}
    for nome_algoritmo, algoritmo in algoritmos.items():
        vetor_distancias = algoritmo(grafo, origem)
        if (
            not isinstance(vetor_distancias, list)
            or len(vetor_distancias) != quantidade_vertices
        ):
            raise ValueError(
                f"o algoritmo {nome_algoritmo!r} deve retornar um vetor com "
                f"{quantidade_vertices} distâncias"
            )
        distancias_referencia[nome_algoritmo] = vetor_distancias.copy()
    return distancias_referencia


def _medir_tempos_execucao(
    grafo: Grafo,
    origem: str,
    algoritmos: Mapping[str, Callable[[Grafo, str], list[Peso]]],
    repeticoes: int,
    distancias_referencia: dict[str, list[Peso]],
) -> dict[str, list[float]]:
    """Mede, em milissegundos, o tempo de cada repetição de cada algoritmo.

    Alterna a ordem de execução entre repetições para reduzir viés de cache e
    de aquecimento entre os algoritmos comparados. Levanta ``ValueError`` se
    algum algoritmo produzir um vetor de distâncias diferente do de referência.
    """
    tempos_por_algoritmo_ms: dict[str, list[float]] = {
        nome_algoritmo: [] for nome_algoritmo in algoritmos
    }
    for indice_repeticao in range(repeticoes):
        ordem_execucao = list(algoritmos)
        if indice_repeticao % 2:
            ordem_execucao.reverse()
        for nome_algoritmo in ordem_execucao:
            inicio_execucao = perf_counter()
            vetor_distancias = algoritmos[nome_algoritmo](grafo, origem)
            tempo_execucao_ms = (perf_counter() - inicio_execucao) * 1000
            tempos_por_algoritmo_ms[nome_algoritmo].append(tempo_execucao_ms)
            if vetor_distancias != distancias_referencia[nome_algoritmo]:
                raise ValueError(
                    f"o algoritmo {nome_algoritmo!r} produziu resultados inconsistentes"
                )
    return tempos_por_algoritmo_ms


def avaliar(
    grafo: Grafo,
    origem: str,
    algoritmos: Mapping[str, Callable[[Grafo, str], list[Peso]]],
    repeticoes: int = 7,
) -> list[dict[str, Any]]:
    """Avalia ``algoritmos`` sobre ``grafo`` a partir de ``origem`` e mede seus tempos.

    Cada função em ``algoritmos`` deve aceitar ``(grafo, origem)`` e retornar
    uma lista com uma distância por vértice, na ordem das chaves de ``grafo``.
    Executa uma repetição de aquecimento por algoritmo (fora da medição) e,
    em seguida, ``repeticoes`` medições, verificando a estabilidade dos
    resultados entre elas. Retorna uma lista com um dicionário de métricas por
    algoritmo: distâncias, tempo mediano e desvio padrão (em milissegundos),
    tamanho da instância e complexidade teórica.
    """
    if (
        isinstance(repeticoes, bool)
        or not isinstance(repeticoes, int)
        or repeticoes < 1
    ):
        raise ValueError("repetições deve ser um inteiro positivo")
    quantidade_vertices = len(grafo)
    quantidade_arestas = sum(len(vizinhos) for vizinhos in grafo.values())
    complexidades_por_algoritmo = {
        "dijkstra": "O(V² + E) em tempo; O(V) em espaço auxiliar",
        "a_estrela": "O(V² + E) em tempo; O(V) em espaço auxiliar; h consistente",
    }
    distancias_referencia = _aquecer_algoritmos(grafo, origem, algoritmos)
    tempos_por_algoritmo_ms = _medir_tempos_execucao(
        grafo, origem, algoritmos, repeticoes, distancias_referencia
    )
    resultados = []
    for nome_algoritmo, vetor_distancias in distancias_referencia.items():
        resultados.append(
            {
                "algoritmo": nome_algoritmo,
                "origem": origem,
                "ordem_vertices": list(grafo),
                "distancias": vetor_distancias,
                "tempo_execucao_ms": median(tempos_por_algoritmo_ms[nome_algoritmo]),
                "desvio_tempo_ms": pstdev(tempos_por_algoritmo_ms[nome_algoritmo]),
                "repeticoes": repeticoes,
                "vertices": quantidade_vertices,
                "arestas": quantidade_arestas,
                "complexidade": complexidades_por_algoritmo.get(
                    nome_algoritmo, "não informada"
                ),
            }
        )
    return resultados
