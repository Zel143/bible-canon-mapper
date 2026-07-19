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
    Build a directed graph representing translation lineage: which source
    texts and prior translations fed into which later translations.

    Edges are sourced against docs/historical_notes.md (see the
    "Sourcing the Translation Lineage Graph" entry, 2026-07-19) and carry
    `date` (approximate) and `note` attributes. A `note` either cites a
    reference number from historical_notes.md's References list, or
    flags an edge as something other than a straightforward source-text
    translation (e.g. "reference, not primary source" for a text a
    translator consulted but didn't translate from; "standardization,
    not translation" for the Masoretes' codification of an existing
    Hebrew tradition rather than a translation into a new language).

    Two corrections against the original placeholder edges, documented
    in historical_notes.md: the Septuagint does not descend from the
    Masoretic Text (the Masoretes postdate the LXX translators by
    roughly a millennium, and the LXX's Hebrew Vorlage differed from the
    proto-Masoretic tradition in places); and no documented textual
    dependency of the KJV on Luther's Bible was found, so that edge was
    dropped in favor of the actual documented English-Bible lineage
    (Tyndale -> Great Bible -> Bishops' Bible -> KJV).
    """
    G = nx.DiGraph()
    lineage_edges = [
        # Hebrew and Greek source traditions
        ("Hebrew Source Texts (Second Temple era, textually plural)", "Septuagint (LXX)",
         "c. 250-132 BC", "translation; LXX's Hebrew Vorlage differed from the "
         "proto-Masoretic tradition in places, per Dead Sea Scroll evidence [7]"),
        ("Hebrew Source Texts (Second Temple era, textually plural)", "Masoretic Text",
         "dominant by 1st c. AD; vocalized/codified by the Masoretes c. 7th-10th c. AD",
         "standardization, not translation"),

        # Latin tradition
        ("Septuagint (LXX)", "Old Latin (Vetus Latina)", "c. 2nd c. AD",
         "Old Testament translated from the LXX, not from Hebrew"),
        ("Masoretic Text", "Vulgate", "382-405 AD",
         "protocanonical OT translated directly from Hebrew (hebraica veritas); "
         "Jerome used the pre-codification 4th-c. form of this tradition [12]"),
        ("Old Latin (Vetus Latina)", "Vulgate", "382-405 AD",
         "most deuterocanonical books (Wisdom, Sirach, Baruch, 1-2 Maccabees) retained "
         "from the Vetus Latina, not retranslated by Jerome [12]"),
        ("Greek New Testament (1st c. manuscripts)", "Vulgate", "382-405 AD",
         "NT is a revision of the Old Latin Gospels against Greek manuscripts, "
         "not a fresh translation [13]"),
        ("Vulgate", "Douay-Rheims (NT 1582, OT 1609-10)", "1582 / 1609-10",
         "sole primary source text, per the Council of Trent's 1546 decree "
         "naming the Vulgate authoritative [2]"),

        # German tradition
        ("Masoretic Text", "Luther's Bible (1534)", "1534",
         "OT translated from Hebrew (Bomberg/Ben Chayyim ed., 1524-25) [10]"),
        ("Erasmus's Greek NT (Textus Receptus)", "Luther's Bible (1534)", "1534",
         "NT translated from Erasmus's 2nd ed. Greek NT, 1519 [11]"),
        ("Vulgate", "Luther's Bible (1534)", "1534",
         "reference, not primary source (Bugenhagen brought the Vulgate "
         "for comparison, per collaborators' accounts) [10]"),

        # English tradition
        ("Erasmus's Greek NT (Textus Receptus)", "Tyndale's Bible (NT 1526, Pentateuch 1530)",
         "1526", "NT translated from Erasmus's Greek NT"),
        ("Masoretic Text", "Tyndale's Bible (NT 1526, Pentateuch 1530)", "1530",
         "Pentateuch translated from Hebrew"),
        ("Tyndale's Bible (NT 1526, Pentateuch 1530)", "Great Bible (1539)", "1539", ""),
        ("Tyndale's Bible (NT 1526, Pentateuch 1530)", "Geneva Bible (1560)", "1560", ""),
        ("Great Bible (1539)", "Bishops' Bible (1568)", "1568", ""),
        ("Bishops' Bible (1568)", "King James Version (1611)", "1611",
         "named base text in the 1604 translators' instructions, rule 1 [8]"),
        ("Tyndale's Bible (NT 1526, Pentateuch 1530)", "King James Version (1611)", "1611",
         "translators instructed to prefer Tyndale's wording where it fit better; "
         "Nielson & Skousen (1998) sampling estimate: ~84% of KJV NT wording [8][9]"),
        ("Geneva Bible (1560)", "King James Version (1611)", "1611",
         "translators instructed to prefer Geneva's wording where it fit better [8]"),
        ("Masoretic Text", "King James Version (1611)", "1611",
         "OT translated from the Bomberg/Ben Chayyim Hebrew edition, 1524-25 [14]"),
        ("Erasmus's Greek NT (Textus Receptus)", "King James Version (1611)", "1611",
         "NT translated from the Textus Receptus tradition (Beza's editions, "
         "building on Erasmus)"),
    ]
    for source, target, date, note in lineage_edges:
        G.add_edge(source, target, date=date, note=note)
    return G


if __name__ == "__main__":
    print("graph_builder.py — run as a script for quick manual testing.")
