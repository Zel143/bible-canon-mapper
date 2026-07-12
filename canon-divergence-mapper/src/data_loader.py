"""
data_loader.py

Utilities for fetching and loading source texts for canon comparison.
Fill in actual API/source integration as data sourcing is finalized
(e.g., STEP Bible, Bible Gateway API, CCAT digitized texts).
"""

import os
import json
from pathlib import Path

RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
METADATA_DIR = Path(__file__).parent.parent / "data" / "metadata"


def load_canon_list(tradition: str) -> list:
    """
    Load the list of books for a given tradition.

    Args:
        tradition: one of "protestant", "catholic", "orthodox"

    Returns:
        List of book names (str). Currently a placeholder —
        replace with parsed data from canon_lists.csv once created.
    """
    raise NotImplementedError(
        "Convert data/metadata/canon_lists.md into structured CSV/JSON, "
        "then implement parsing here."
    )


def load_raw_text(source: str, book: str) -> str:
    """
    Load raw text for a given source translation and book.

    Args:
        source: e.g. "kjv", "douay_rheims", "septuagint", "vulgate"
        book: book name, e.g. "Genesis", "Tobit"

    Returns:
        Raw text string for the requested book.
    """
    file_path = RAW_DATA_DIR / source / f"{book}.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"No raw text found at {file_path}")
    return file_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    print("data_loader.py — run as a script for quick manual testing.")
