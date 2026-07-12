"""
align_corpus.py

Aligns parallel verses/books across different canon traditions
to support comparative analysis (overlap, topic modeling, etc.).
"""

from typing import Dict, List


def align_books(protestant_books: List[str], catholic_books: List[str], orthodox_books: List[str]) -> Dict[str, Dict[str, bool]]:
    """
    Build a presence/absence matrix showing which tradition includes which book.

    Returns:
        Dict mapping book name -> {"protestant": bool, "catholic": bool, "orthodox": bool}
    """
    all_books = set(protestant_books) | set(catholic_books) | set(orthodox_books)
    matrix = {}
    for book in sorted(all_books):
        matrix[book] = {
            "protestant": book in protestant_books,
            "catholic": book in catholic_books,
            "orthodox": book in orthodox_books,
        }
    return matrix


def unique_to_tradition(matrix: Dict[str, Dict[str, bool]], tradition: str) -> List[str]:
    """Return books present only in the specified tradition."""
    others = [t for t in ("protestant", "catholic", "orthodox") if t != tradition]
    return [
        book for book, presence in matrix.items()
        if presence[tradition] and not any(presence[o] for o in others)
    ]


if __name__ == "__main__":
    print("align_corpus.py — run as a script for quick manual testing.")
