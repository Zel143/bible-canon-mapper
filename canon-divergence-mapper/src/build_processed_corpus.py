"""
build_processed_corpus.py

Builds the cleaned corpus in data/processed/ from the raw KJV texts
fetched by fetch_kjv.py, via align_corpus.load_book_text. As of
2026-07-22 the text pipeline is restricted to the Protestant Bible only
(66-book Protestant canon, KJV text) — see align_corpus.CANONICAL_SOURCES.

Writes:
  data/processed/protestant/<book>.txt   -- cleaned text, one file per book
  data/processed/corpus_manifest.json    -- canon overlap matrix (from
                                             align_corpus.align_books;
                                             metadata-only, uses no text)
                                             plus per-book source/length
                                             metadata

Cleaning removes non-scriptural editorial matter (book introductions,
"<Book> Chapter N" headings, per-chapter summary blurbs) and verse-number
prefixes, which the Gutenberg KJV edition includes inline.

Usage:
    python src/build_processed_corpus.py
"""

import json
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from align_corpus import align_books, get_source, load_book_text  # noqa: E402
from data_loader import load_canon_list  # noqa: E402

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
TRADITIONS = ("protestant",)
VERSE_PREFIX_RE = re.compile(r"^\d+:\d+\.?\s*")
INLINE_VERSE_RE = re.compile(r"\s\d+:\d+\.?(?=\s)")


def clean_verse_style(raw: str) -> str:
    """For KJV/Douay-Rheims raw text: drop paragraphs that aren't verses
    (book introductions, chapter headings, chapter summaries) and strip
    the leading 'chapter:verse' marker from the ones that are. Some
    chapters (e.g. genealogies) pack several verses into one paragraph
    without a blank line between them, so also strip any 'chapter:verse'
    markers embedded mid-paragraph."""
    kept = []
    for para in re.split(r"\n\s*\n", raw.strip()):
        para = para.strip()
        match = VERSE_PREFIX_RE.match(para)
        if not match:
            continue
        para = re.sub(r"\s+", " ", para[match.end():]).strip()
        para = INLINE_VERSE_RE.sub("", para)
        kept.append(para)
    return "\n\n".join(kept)


def clean_prose_style(raw: str) -> str:
    """For sources already stripped to plain prose (Septuagint): just
    normalize whitespace."""
    text = re.sub(r"[ \t]+", " ", raw.strip())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def clean_text(source: str, raw: str) -> str:
    if source in ("kjv", "douay_rheims"):
        return clean_verse_style(raw)
    return clean_prose_style(raw)


def main():
    matrix = align_books(
        load_canon_list("protestant"),
        load_canon_list("catholic"),
        load_canon_list("orthodox"),
    )
    manifest = {"canon_overlap_matrix": matrix, "books": {}}
    counts = {tradition: 0 for tradition in TRADITIONS}

    for tradition in TRADITIONS:
        out_dir = PROCESSED_DIR / tradition
        out_dir.mkdir(parents=True, exist_ok=True)

        for book in load_canon_list(tradition):
            source = get_source(tradition, book)
            cleaned = clean_text(source, load_book_text(tradition, book))

            (out_dir / f"{book}.txt").write_text(cleaned, encoding="utf-8")
            counts[tradition] += 1

            manifest["books"].setdefault(book, {})[tradition] = {
                "source": source,
                "chars": len(cleaned),
                "words": len(cleaned.split()),
            }

    manifest_path = PROCESSED_DIR / "corpus_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    for tradition in TRADITIONS:
        print(f"Wrote {counts[tradition]} cleaned book files to {PROCESSED_DIR / tradition}")
    print(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    main()
