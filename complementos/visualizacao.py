"""Desenho dos grafos e das métricas de tempo com Matplotlib e NetworkX."""

from itertools import pairwise
from math import isfinite
from pathlib import Path
from typing import Any

import matplotlib
import networkx as nx

from caminhos_minimos.grafo import Grafo, validar_grafo

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def desenhar_grafo(
    grafo: Grafo, caminho: list[str] | None = None, saida: str | Path = "grafo.png"
) -> None:
    """Desenha ``grafo`` e salva a imagem em ``saida``, destacando ``caminho`` em
    vermelho.

    Com mais de 80 arestas, omite os rótulos de peso e ajusta o layout
    (circular, linhas mais finas e transparentes) para reduzir a sobreposição
    de rótulos; todos os vértices e arestas continuam desenhados.
    """
    validar_grafo(grafo)
    rede: nx.DiGraph[str] = nx.DiGraph()
    rede.add_nodes_from(grafo)
    for origem, vizinhos in grafo.items():
        for destino, peso in vizinhos.items():
            rede.add_edge(origem, destino, weight=peso)
    quantidade_vertices = rede.number_of_nodes()
    quantidade_arestas = rede.number_of_edges()
    grafo_denso = quantidade_arestas > 80
    grafo_desconexo = quantidade_vertices > 0 and not nx.is_weakly_connected(rede)
    if grafo_denso or grafo_desconexo:
        posicoes = nx.circular_layout(rede)
    else:
        # weight=None é válido em tempo de execução (trata arestas como sem peso),
        # mas o stub de tipos do NetworkX só declara `weight: str`.
        posicoes = nx.spring_layout(rede, seed=42, weight=None)  # type: ignore[arg-type]
    arestas_caminho = set(pairwise(caminho or []))
    cor_aresta = (0.30, 0.47, 0.72, 0.15) if grafo_denso else "#4c78a8"
    cores = [
        "crimson" if aresta in arestas_caminho else cor_aresta
        for aresta in rede.edges()
    ]
    figura, eixo = plt.subplots(figsize=(14, 10) if grafo_denso else (9, 6))
    try:
        nx.draw(
            rede,
            posicoes,
            ax=eixo,
            with_labels=True,
            node_color="#f2cf5b",
            edge_color=cores,
            arrows=True,
            node_size=max(120, 6500 // max(quantidade_vertices, 10)),
            font_size=8 if grafo_denso else 10,
            arrowsize=6 if grafo_denso else 10,
            width=0.5 if grafo_denso else 1,
            connectionstyle="arc3,rad=0.08",
        )
        if not grafo_denso:
            nx.draw_networkx_edge_labels(
                rede,
                posicoes,
                ax=eixo,
                edge_labels=nx.get_edge_attributes(rede, "weight"),
                connectionstyle="arc3,rad=0.08",
            )
        titulo = "Caminho mínimo em vermelho" if caminho else "Grafo direcionado"
        titulo += f" — {quantidade_vertices} vértices, {quantidade_arestas} arestas"
        if grafo_denso:
            titulo += "\nPesos disponíveis no arquivo do dataset"
        eixo.set_title(titulo)
        figura.tight_layout()
        figura.savefig(saida, dpi=160)
    finally:
        plt.close(figura)


def desenhar_comparacao(resultados: list[dict[str, Any]], saida: str | Path) -> None:
    """Desenha, em barras, o tempo mediano e o desvio padrão de cada algoritmo avaliado.

    Espera o formato retornado por :func:`complementos.avaliacao.avaliar`.
    """
    nomes = [resultado["algoritmo"] for resultado in resultados]
    metricas = [
        ("tempo_execucao_ms", "Tempo mediano", "Milissegundos"),
        ("desvio_tempo_ms", "Desvio padrão do tempo", "Milissegundos"),
    ]
    figura, eixos = plt.subplots(1, 2, figsize=(10, 4))
    try:
        for eixo, (campo, titulo, unidade) in zip(eixos, metricas, strict=True):
            valores = [resultado[campo] for resultado in resultados]
            valores_finitos = [
                valor if valor is not None and isfinite(valor) else 0
                for valor in valores
            ]
            barras = eixo.bar(nomes, valores_finitos, color=["#4c78a8", "#e08d3c"])
            for barra, valor in zip(barras, valores, strict=True):
                if valor is None or not isfinite(valor):
                    eixo.annotate("inalcançável", (barra.get_x(), 0), rotation=90)
            eixo.set_title(titulo)
            eixo.set_ylabel(unidade)
            eixo.grid(axis="y", alpha=0.3)
        figura.tight_layout()
        figura.savefig(saida, dpi=160)
    finally:
        plt.close(figura)
