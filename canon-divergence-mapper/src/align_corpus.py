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

# Canonical text source per tradition, picked so each tradition's shared
# books are read from the translation closest to that tradition's own
# textual basis, now that KJV/Douay-Rheims/Septuagint are all fetched and
# a given book (e.g. Genesis) may exist in more than one source:
#   - protestant: KJV — Masoretic-based OT, the only Protestant-specific
#     source fetched.
#   - catholic: Douay-Rheims — Vulgate-based, one consistent translation
#     covering the full 73-book Catholic canon.
#   - orthodox: Septuagint (Brenton) — the Old Testament, Greek-based, is
#     the Orthodox canon's actual textual basis (Septuagint > Masoretic
#     for this tradition specifically). Brenton's translation has no New
#     Testament, so Orthodox NT books fall back to KJV, whose Textus
#     Receptus is closer to the Byzantine text Orthodox churches use
#     liturgically than the Vulgate-derived Douay-Rheims NT.
CANONICAL_SOURCES = {
    "protestant": "kjv",
    "catholic": "douay_rheims",
    "orthodox": "septuagint",
}
ORTHODOX_NT_FALLBACK = "kjv"


def get_source(tradition: str, book: str) -> str:
    """Return the data_loader source key to use for `book` within `tradition`."""
    if tradition not in CANONICAL_SOURCES:
        raise ValueError(f"Unknown tradition: {tradition!r}")

    source = CANONICAL_SOURCES[tradition]
    if tradition == "orthodox":
        new_testament_books = set(load_canon_list("protestant")[-27:])
        if book in new_testament_books:
            return ORTHODOX_NT_FALLBACK
    return source


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
