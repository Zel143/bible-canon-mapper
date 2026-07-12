"""
fetch_kjv.py

Downloads the King James Version from Project Gutenberg (public domain,
eBook #10) and splits it into one plain-text file per book under
data/raw/kjv/, matching the book names in data/metadata/canon_lists.json
so src/data_loader.load_raw_text('kjv', book) can find them.

This edition does not include the Apocrypha, so it only covers the
Protestant 66-book list — Catholic/Orthodox-only books need a separate
source (e.g. Douay-Rheims, Brenton's Septuagint).

Usage:
    python src/fetch_kjv.py
"""

import re
import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).parent))
from data_loader import RAW_DATA_DIR, load_canon_list  # noqa: E402

GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/10/pg10.txt"

# Book headings exactly as they appear in the Gutenberg text, in the same
# order as load_canon_list('protestant') (Old Testament, then New Testament).
GUTENBERG_TITLES = [
    "The First Book of Moses: Called Genesis",
    "The Second Book of Moses: Called Exodus",
    "The Third Book of Moses: Called Leviticus",
    "The Fourth Book of Moses: Called Numbers",
    "The Fifth Book of Moses: Called Deuteronomy",
    "The Book of Joshua",
    "The Book of Judges",
    "The Book of Ruth",
    "The First Book of Samuel",
    "The Second Book of Samuel",
    "The First Book of the Kings",
    "The Second Book of the Kings",
    "The First Book of the Chronicles",
    "The Second Book of the Chronicles",
    "Ezra",
    "The Book of Nehemiah",
    "The Book of Esther",
    "The Book of Job",
    "The Book of Psalms",
    "The Proverbs",
    "Ecclesiastes",
    "The Song of Solomon",
    "The Book of the Prophet Isaiah",
    "The Book of the Prophet Jeremiah",
    "The Lamentations of Jeremiah",
    "The Book of the Prophet Ezekiel",
    "The Book of Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "The Gospel According to Saint Matthew",
    "The Gospel According to Saint Mark",
    "The Gospel According to Saint Luke",
    "The Gospel According to Saint John",
    "The Acts of the Apostles",
    "The Epistle of Paul the Apostle to the Romans",
    "The First Epistle of Paul the Apostle to the Corinthians",
    "The Second Epistle of Paul the Apostle to the Corinthians",
    "The Epistle of Paul the Apostle to the Galatians",
    "The Epistle of Paul the Apostle to the Ephesians",
    "The Epistle of Paul the Apostle to the Philippians",
    "The Epistle of Paul the Apostle to the Colossians",
    "The First Epistle of Paul the Apostle to the Thessalonians",
    "The Second Epistle of Paul the Apostle to the Thessalonians",
    "The First Epistle of Paul the Apostle to Timothy",
    "The Second Epistle of Paul the Apostle to Timothy",
    "The Epistle of Paul the Apostle to Titus",
    "The Epistle of Paul the Apostle to Philemon",
    "The Epistle of Paul the Apostle to the Hebrews",
    "The General Epistle of James",
    "The First Epistle General of Peter",
    "The Second General Epistle of Peter",
    "The First Epistle General of John",
    "The Second Epistle General of John",
    "The Third Epistle General of John",
    "The General Epistle of Jude",
    "The Revelation of Saint John the Divine",
]


def download_source_text() -> str:
    response = requests.get(GUTENBERG_URL, timeout=30)
    response.raise_for_status()
    return response.text


def strip_gutenberg_boilerplate(text: str) -> str:
    start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", text)
    end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", text)
    if not start_match or not end_match:
        raise ValueError("Could not find Project Gutenberg start/end markers")
    return text[start_match.end():end_match.start()]


def find_body_start(text: str) -> int:
    """Skip the table of contents by finding the second (real) occurrence
    of the Old Testament heading, which precedes the actual book text."""
    heading = "The Old Testament of the King James Version of the Bible"
    first = text.find(heading)
    second = text.find(heading, first + 1)
    if second == -1:
        raise ValueError("Could not locate start of body text after table of contents")
    return second


def _is_real_heading(text: str, match_start: int) -> bool:
    """1-2 Samuel and 1-2 Kings each carry a historical alternate-name
    subtitle (e.g. "Otherwise Called: The First Book of the Kings") that
    reuses another book's title text right before its own body starts.
    Those subtitle occurrences must not be mistaken for the real heading."""
    lookback = text[max(0, match_start - 80):match_start]
    return "Called:" not in lookback


def split_into_books(text: str) -> dict:
    """Split body text into {gutenberg_title: book_text} using GUTENBERG_TITLES
    as section boundaries."""
    positions = []
    for title in GUTENBERG_TITLES:
        idx = -1
        search_from = 0
        while True:
            idx = text.find(title, search_from)
            if idx == -1:
                raise ValueError(f"Could not find real heading in source text: {title!r}")
            if _is_real_heading(text, idx):
                break
            search_from = idx + len(title)
        positions.append((idx, title))
    positions.sort()

    books = {}
    for i, (idx, title) in enumerate(positions):
        section_start = idx + len(title)
        section_end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        section = text[section_start:section_end]
        # Malachi's section runs up to the Matthew heading and picks up the
        # OT/NT divider ("***" plus the New Testament section title) along
        # the way — strip it so only real book content remains.
        section = re.sub(
            r"\*\*\*\s*The New Testament of the King James Bible\s*\Z", "", section
        )
        books[title] = section.strip()
    return books


def main():
    print(f"Downloading KJV from {GUTENBERG_URL} ...")
    raw = download_source_text()

    body = strip_gutenberg_boilerplate(raw)
    body = body[find_body_start(body):]
    books_by_title = split_into_books(body)

    canonical_books = load_canon_list("protestant")
    if len(canonical_books) != len(GUTENBERG_TITLES):
        raise ValueError(
            f"Expected {len(GUTENBERG_TITLES)} books to match the protestant canon list, "
            f"got {len(canonical_books)}"
        )

    out_dir = RAW_DATA_DIR / "kjv"
    out_dir.mkdir(parents=True, exist_ok=True)

    for canonical_name, gutenberg_title in zip(canonical_books, GUTENBERG_TITLES):
        book_text = books_by_title[gutenberg_title]
        out_path = out_dir / f"{canonical_name}.txt"
        out_path.write_text(book_text, encoding="utf-8")

    print(f"Wrote {len(canonical_books)} book files to {out_dir}")


if __name__ == "__main__":
    main()
