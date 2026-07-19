"""
fetch_douay_rheims.py

Downloads the Douay-Rheims Bible (Challoner revision, public domain,
Project Gutenberg eBook #1581) and splits it into one plain-text file per
book under data/raw/douay_rheims/, matching the book names in
data/metadata/canon_lists.json so
src/data_loader.load_raw_text('douay_rheims', book) can find them.

This edition contains the full 73-book Catholic canon (the Protestant 39
plus the 7 deuterocanonical books, with the Esther/Daniel additions folded
into those books rather than split out separately) — it is used as the
Catholic-canon source, independent of the KJV, so all Catholic-only text
comes from one consistent translation. Orthodox-only books (1 Esdras,
3 Maccabees, Prayer of Manasseh, Psalm 151) still need a separate source
(e.g. Brenton's Septuagint).

Usage:
    python src/fetch_douay_rheims.py
"""

import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).parent))
from data_loader import RAW_DATA_DIR, load_canon_list  # noqa: E402

GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/1581/pg1581.txt"

# Marks the end of the canonical text — a transcriber's note followed by
# the prayer of Manasses and 3/4 Esdras (explicitly flagged in the source
# as "not receiued into the Canon of Diuine Scriptures by the Catholique
# Church") come after this heading, right after Revelation ends.
CANON_END_MARKER = "APPENDICES"

# Book headings exactly as they appear (all-caps) in the Gutenberg text,
# in the same order as load_canon_list('catholic') (Old Testament — the
# Protestant 39 plus the 7 deuterocanonical additions — then New
# Testament).
GUTENBERG_TITLES = [
    "THE BOOK OF GENESIS",
    "THE BOOK OF EXODUS",
    "THE BOOK OF LEVITICUS",
    "THE BOOK OF NUMBERS",
    "THE BOOK OF DEUTERONOMY",
    "THE BOOK OF JOSUE",
    "THE BOOK OF JUDGES",
    "THE BOOK OF RUTH",
    "THE FIRST BOOK OF SAMUEL, OTHERWISE CALLED THE FIRST BOOK OF KINGS",
    "THE SECOND BOOK OF SAMUEL, OTHERWISE CALLED THE SECOND BOOK OF KINGS",
    "THE THIRD BOOK OF KINGS",
    "THE FOURTH BOOK OF KINGS",
    "THE FIRST BOOK OF PARALIPOMENON",
    "THE SECOND BOOK OF PARALIPOMENON",
    "THE FIRST BOOK OF ESDRAS",
    "THE BOOK OF NEHEMIAS, WHICH IS CALLED THE SECOND OF ESDRAS",
    "THE BOOK OF ESTHER",
    "THE BOOK OF JOB",
    "THE BOOK OF PSALMS",
    "THE BOOK OF PROVERBS",
    "ECCLESIASTES",
    "SOLOMON’S CANTICLE OF CANTICLES",
    "THE PROPHECY OF ISAIAS",
    "THE PROPHECY OF JEREMIAS",
    "THE LAMENTATIONS OF JEREMIAS",
    "THE PROPHECY OF EZECHIEL",
    "THE PROPHECY OF DANIEL",
    "THE PROPHECY OF OSEE",
    "THE PROPHECY OF JOEL",
    "THE PROPHECY OF AMOS",
    "THE PROPHECY OF ABDIAS",
    "THE PROPHECY OF JONAS",
    "THE PROPHECY OF MICHEAS",
    "THE PROPHECY OF NAHUM",
    "THE PROPHECY OF HABACUC",
    "THE PROPHECY OF SOPHONIAS",
    "THE PROPHECY OF AGGEUS",
    "THE PROPHECY OF ZACHARIAS",
    "THE PROPHECY OF MALACHIAS",
    # Deuterocanonical additions (Catholic-only)
    "THE BOOK OF TOBIAS",
    "THE BOOK OF JUDITH",
    "THE FIRST BOOK OF MACHABEES",
    "THE SECOND BOOK OF MACHABEES",
    "THE BOOK OF WISDOM",
    "ECCLESIASTICUS",
    "THE PROPHECY OF BARUCH",
    # New Testament
    "THE HOLY GOSPEL OF JESUS CHRIST ACCORDING TO SAINT MATTHEW",
    "THE HOLY GOSPEL OF JESUS CHRIST ACCORDING TO ST. MARK",
    "THE HOLY GOSPEL OF JESUS CHRIST ACCORDING TO ST. LUKE",
    "THE HOLY GOSPEL OF JESUS CHRIST ACCORDING TO ST. JOHN",
    "THE ACTS OF THE APOSTLES",
    "THE EPISTLE OF ST. PAUL THE APOSTLE TO THE ROMANS",
    "THE FIRST EPISTLE OF ST. PAUL TO THE CORINTHIANS",
    "THE SECOND EPISTLE OF ST. PAUL TO THE CORINTHIANS",
    "THE EPISTLE OF ST. PAUL TO THE GALATIANS",
    "THE EPISTLE OF ST. PAUL TO THE EPHESIANS",
    "THE EPISTLE OF ST. PAUL TO THE PHILIPPIANS",
    "THE EPISTLE OF ST. PAUL TO THE COLOSSIANS",
    "THE FIRST EPISTLE OF ST. PAUL TO THE THESSALONIANS",
    "THE SECOND EPISTLE OF ST. PAUL TO THE THESSALONIANS",
    "THE FIRST EPISTLE OF ST. PAUL TO TIMOTHY",
    "THE SECOND EPISTLE OF ST. PAUL TO TIMOTHY",
    "THE EPISTLE OF ST. PAUL TO TITUS",
    "THE EPISTLE OF ST. PAUL TO PHILEMON",
    "THE EPISTLE OF ST. PAUL TO THE HEBREWS",
    "THE CATHOLIC EPISTLE OF ST. JAMES THE APOSTLE",
    "THE FIRST EPISTLE OF ST. PETER THE APOSTLE",
    "THE SECOND EPISTLE OF ST. PETER THE APOSTLE",
    "THE FIRST EPISTLE OF ST. JOHN THE APOSTLE",
    "THE SECOND EPISTLE OF ST. JOHN THE APOSTLE",
    "THE THIRD EPISTLE OF ST. JOHN THE APOSTLE",
    "THE CATHOLIC EPISTLE OF ST. JUDE",
    "THE APOCALYPSE OF ST. JOHN THE APOSTLE",
]


def download_source_text() -> str:
    response = requests.get(GUTENBERG_URL, timeout=30)
    response.raise_for_status()
    # Gutenberg serves \r\n line endings; normalize to \n so Path.write_text's
    # platform newline translation (on Windows: \n -> \r\n) doesn't double them
    # into \r\r\n.
    return response.text.replace("\r\n", "\n")


def strip_gutenberg_boilerplate(text: str) -> str:
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE BIBLE, DOUAY-RHEIMS, COMPLETE ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE BIBLE, DOUAY-RHEIMS, COMPLETE ***"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        raise ValueError("Could not find Project Gutenberg start/end markers")
    return text[start + len(start_marker):end]


def find_body_start(text: str) -> int:
    """Skip the table of contents by finding the second (real) occurrence
    of the Old Testament heading, which precedes the actual book text."""
    heading = "THE OLD TESTAMENT"
    first = text.find(heading)
    second = text.find(heading, first + 1)
    if second == -1:
        raise ValueError("Could not locate start of body text after table of contents")
    return second


def find_body_end(text: str) -> int:
    """Trim off the non-canonical appendix (Prayer of Manasses, 3/4 Esdras)
    that follows the Apocalypse in this edition."""
    end = text.find(CANON_END_MARKER)
    if end == -1:
        raise ValueError(f"Could not locate canon end marker {CANON_END_MARKER!r}")
    return end


def split_into_books(text: str) -> dict:
    """Split body text into {gutenberg_title: book_text} using GUTENBERG_TITLES
    as section boundaries."""
    positions = []
    for title in GUTENBERG_TITLES:
        idx = text.find(title)
        if idx == -1:
            raise ValueError(f"Could not find heading in source text: {title!r}")
        positions.append((idx, title))
    positions.sort()

    books = {}
    for i, (idx, title) in enumerate(positions):
        section_start = idx + len(title)
        section_end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        books[title] = text[section_start:section_end].strip()
    return books


def main():
    print(f"Downloading Douay-Rheims from {GUTENBERG_URL} ...")
    raw = download_source_text()

    body = strip_gutenberg_boilerplate(raw)
    body = body[find_body_start(body):find_body_end(body)]
    books_by_title = split_into_books(body)

    canonical_books = load_canon_list("catholic")
    if len(canonical_books) != len(GUTENBERG_TITLES):
        raise ValueError(
            f"Expected {len(GUTENBERG_TITLES)} books to match the catholic canon list, "
            f"got {len(canonical_books)}"
        )

    out_dir = RAW_DATA_DIR / "douay_rheims"
    out_dir.mkdir(parents=True, exist_ok=True)

    for canonical_name, gutenberg_title in zip(canonical_books, GUTENBERG_TITLES):
        book_text = books_by_title[gutenberg_title]
        out_path = out_dir / f"{canonical_name}.txt"
        out_path.write_text(book_text, encoding="utf-8")

    print(f"Wrote {len(canonical_books)} book files to {out_dir}")


if __name__ == "__main__":
    main()
