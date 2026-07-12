"""
graph_builder.py

Builds NetworkX graph structures representing canon overlap
and translation lineage, for visualization in notebooks/04_visualization.ipynb.
"""

import networkx as nx
from typing import Dict


def build_canon_overlap_graph(matrix: Dict[str, Dict[str, bool]]) -> nx.Graph:
    """
    Build a bipartite-style graph connecting traditions to the books they contain.

    Args:
        matrix: output of align_corpus.align_books()

    Returns:
        networkx.Graph with tradition and book nodes, edges = "contains"
    """
    G = nx.Graph()
    traditions = ("protestant", "catholic", "orthodox")

    for tradition in traditions:
        G.add_node(tradition, node_type="tradition")

    for book, presence in matrix.items():
        G.add_node(book, node_type="book")
        for tradition in traditions:
            if presence[tradition]:
                G.add_edge(tradition, book)

    return G


def build_translation_lineage_graph() -> nx.DiGraph:
    """
    Build a directed graph representing translation lineage
    (e.g., Septuagint -> Vulgate -> Luther's Bible -> KJV -> modern translations).

    Placeholder edges — refine with actual historical sourcing/dating.
    """
    G = nx.DiGraph()
    lineage_edges = [
        ("Hebrew Masoretic Text", "Septuagint"),
        ("Septuagint", "Vulgate"),
        ("Hebrew Masoretic Text", "Vulgate"),
        ("Vulgate", "Luther's Bible (1534)"),
        ("Hebrew Masoretic Text", "Luther's Bible (1534)"),
        ("Vulgate", "Douay-Rheims (1610)"),
        ("Luther's Bible (1534)", "King James Version (1611)"),
        ("Hebrew Masoretic Text", "King James Version (1611)"),
    ]
    G.add_edges_from(lineage_edges)
    return G


if __name__ == "__main__":
    print("graph_builder.py — run as a script for quick manual testing.")
