"""
data_loader.py

Utilities for fetching and loading source texts for canon comparison.
Fill in actual API/source integration as data sourcing is finalized
(e.g., STEP Bible, Bible Gateway API, CCAT digitized texts).
"""

import json
from pathlib import Path

RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
METADATA_DIR = Path(__file__).parent.parent / "data" / "metadata"


CANON_LISTS_PATH = METADATA_DIR / "canon_lists.json"


def load_canon_list(tradition: str) -> list:
    """
    Load the list of books for a given tradition.

    Args:
        tradition: one of "protestant", "catholic", "orthodox"

    Returns:
        List of book names (str), Old Testament followed by New Testament.
        Catholic and Orthodox lists are built additively on top of the
        Protestant list per data/metadata/canon_lists.json.
    """
    with open(CANON_LISTS_PATH, encoding="utf-8") as f:
        canon_data = json.load(f)

    if tradition not in ("protestant", "catholic", "orthodox"):
        raise ValueError(f"Unknown tradition: {tradition!r}")

    protestant_ot = canon_data["protestant"]["old_testament"]
    new_testament = canon_data["protestant"]["new_testament"]

    old_testament = list(protestant_ot)
    if tradition in ("catholic", "orthodox"):
        old_testament += canon_data["catholic"]["old_testament_additions"]
    if tradition == "orthodox":
        old_testament += canon_data["orthodox"]["old_testament_additions"]

    return old_testament + new_testament


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
