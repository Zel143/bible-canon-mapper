"""
align_corpus.py

Aligns parallel verses/books across different canon traditions
to support comparative analysis (overlap, topic modeling, etc.).
"""

import sys
from pathlib import Path
from typing import Dict, List

sys.path.append(str(Path(__file__).parent))
from data_loader import load_canon_list, load_raw_text  # noqa: E402

# Text-source scope (changed 2026-07-22): the corpus is restricted to the
# Protestant Bible only — the 66-book Protestant canon, read from the KJV.
# The Douay-Rheims and Septuagint fetchers/raw data still exist (and the
# old per-tradition source mapping is in git history) but are no longer
# part of the active text pipeline. Canon *lists* for catholic/orthodox
# remain available via data_loader.load_canon_list for metadata-level
# comparison (e.g. the canon overlap matrix), which uses no text.
CANONICAL_SOURCES = {
    "protestant": "kjv",
}


def get_source(tradition: str, book: str) -> str:
    """Return the data_loader source key to use for `book` within `tradition`."""
    if tradition not in CANONICAL_SOURCES:
        raise ValueError(
            f"No text source for tradition {tradition!r}: the corpus is "
            "restricted to the Protestant canon (KJV) as of 2026-07-22"
        )
    return CANONICAL_SOURCES[tradition]


def load_book_text(tradition: str, book: str) -> str:
    """Load `book`'s text using the canonical source for `tradition`."""
    if book not in load_canon_list(tradition):
        raise ValueError(f"{book!r} is not in the {tradition} canon")
    return load_raw_text(get_source(tradition, book), book)


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
