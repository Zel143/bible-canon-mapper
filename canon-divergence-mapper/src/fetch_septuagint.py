"""
fetch_septuagint.py

Downloads Sir Lancelot Brenton's 1851 English translation of the
Septuagint (public domain, distributed as USFM by eBible.org) and
converts it into one plain-text file per book under data/raw/septuagint/,
matching the book names in data/metadata/canon_lists.json so
src/data_loader.load_raw_text('septuagint', book) can find them.

The Septuagint is the Greek Old Testament that underlies the Orthodox
(and, historically, much of the Catholic) canon — unlike fetch_kjv.py and
fetch_douay_rheims.py, which each cover one tradition's *full* Bible, this
only covers the Old Testament (Brenton's translation has no New
Testament) but covers *all* 50 Orthodox OT books from one consistent
Greek-based translation, including the ones shared with the Protestant
and Catholic lists — useful for translation-lineage comparison against
KJV (Masoretic-based) and Douay-Rheims (Vulgate-based) versions of the
same book.

Some canonical books are assembled from more than one USFM file, per
Brenton's source division:
  - Daniel = DAG (Daniel) + SUS (Susanna) + BEL (Bel and the Dragon),
    matching the Catholic convention (see canon_lists.json) of folding
    the Daniel additions into a single "Daniel" book rather than listing
    them separately.
  - Baruch = BAR (Baruch) + LJE (Epistle of Jeremy), matching the
    Catholic/Vulgate convention of treating the Epistle of Jeremy as
    Baruch chapter 6 (confirmed against data/raw/douay_rheims/Baruch.txt).
  - Psalms / Psalm 151 are both drawn from the PSA file, which bundles
    Psalm 151 as a "supernumerary" 151st chapter — split out at the
    `\\c 151` marker into its own file since canon_lists.json lists it as
    a separate orthodox-only book.

Usage:
    python src/fetch_septuagint.py
"""

import io
import re
import sys
import zipfile
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).parent))
from data_loader import RAW_DATA_DIR, load_canon_list  # noqa: E402

USFM_ZIP_URL = "https://eBible.org/Scriptures/eng-Brenton_usfm.zip"

# canonical book name -> USFM file code(s) to concatenate, in the same
# order as the Old Testament portion of load_canon_list('orthodox').
BOOK_CODES = {
    "Genesis": ["GEN"],
    "Exodus": ["EXO"],
    "Leviticus": ["LEV"],
    "Numbers": ["NUM"],
    "Deuteronomy": ["DEU"],
    "Joshua": ["JOS"],
    "Judges": ["JDG"],
    "Ruth": ["RUT"],
    "1 Samuel": ["1SA"],
    "2 Samuel": ["2SA"],
    "1 Kings": ["1KI"],
    "2 Kings": ["2KI"],
    "1 Chronicles": ["1CH"],
    "2 Chronicles": ["2CH"],
    "Ezra": ["EZR"],
    "Nehemiah": ["NEH"],
    "Esther": ["ESG"],
    "Job": ["JOB"],
    "Psalms": ["PSA"],  # special-cased below: chapters 1-150 only
    "Proverbs": ["PRO"],
    "Ecclesiastes": ["ECC"],
    "Song of Solomon": ["SNG"],
    "Isaiah": ["ISA"],
    "Jeremiah": ["JER"],
    "Lamentations": ["LAM"],
    "Ezekiel": ["EZK"],
    "Daniel": ["DAG", "SUS", "BEL"],
    "Hosea": ["HOS"],
    "Joel": ["JOL"],
    "Amos": ["AMO"],
    "Obadiah": ["OBA"],
    "Jonah": ["JON"],
    "Micah": ["MIC"],
    "Nahum": ["NAM"],
    "Habakkuk": ["HAB"],
    "Zephaniah": ["ZEP"],
    "Haggai": ["HAG"],
    "Zechariah": ["ZEC"],
    "Malachi": ["MAL"],
    "Tobit": ["TOB"],
    "Judith": ["JDT"],
    "1 Maccabees": ["1MA"],
    "2 Maccabees": ["2MA"],
    "Wisdom": ["WIS"],
    "Sirach": ["SIR"],
    "Baruch": ["BAR", "LJE"],
    "1 Esdras": ["1ES"],
    "3 Maccabees": ["3MA"],
    "Prayer of Manasseh": ["MAN"],
    # "Psalm 151" is handled separately: split out of the PSA file.
}

# USFM structural/metadata line tags to drop entirely (not body text).
DROP_LINE_TAGS = {"id", "ide", "h", "toc1", "toc2", "toc3", "toc4", "mt1", "mt2", "mt3", "rem"}


def download_usfm_files() -> dict:
    """Download the USFM zip and return {code: raw_usfm_text}."""
    response = requests.get(USFM_ZIP_URL, timeout=60)
    response.raise_for_status()
    archive = zipfile.ZipFile(io.BytesIO(response.content))

    files = {}
    for name in archive.namelist():
        m = re.match(r"\d+-([A-Z0-9]+)eng-Brenton\.usfm$", name)
        if m:
            files[m.group(1)] = archive.read(name).decode("utf-8")
    return files


def strip_usfm(text: str) -> str:
    """Convert raw USFM markup to plain running text."""
    text = re.sub(r"\\f \+.*?\\f\*", "", text, flags=re.DOTALL)
    text = re.sub(r"\\x .*?\\x\*", "", text, flags=re.DOTALL)

    lines = []
    for line in text.splitlines():
        tag_match = re.match(r"\\(\S+)", line)
        if tag_match and tag_match.group(1).rstrip("*") in DROP_LINE_TAGS:
            continue
        line = re.sub(r"\\c\s+\d+", "", line)
        line = re.sub(r"\\v\s+\d+", "", line)
        line = re.sub(r"\\[A-Za-z0-9]+\*?", "", line)
        lines.append(line.strip())

    joined = "\n".join(lines)
    joined = re.sub(r"[ \t]+", " ", joined)
    joined = re.sub(r"\n{3,}", "\n\n", joined)
    return joined.strip()


def split_psalms(psa_raw: str) -> tuple:
    """Split the PSA file into (psalms_1_150_raw, psalm_151_raw) at the
    `\\c 151` chapter marker."""
    marker = "\\c 151"
    idx = psa_raw.find(marker)
    if idx == -1:
        raise ValueError("Could not find Psalm 151 chapter marker in PSA file")
    return psa_raw[:idx], psa_raw[idx:]


def main():
    print(f"Downloading Brenton Septuagint (USFM) from {USFM_ZIP_URL} ...")
    usfm_files = download_usfm_files()

    psalms_raw, psalm_151_raw = split_psalms(usfm_files["PSA"])
    usfm_files["PSA"] = psalms_raw
    usfm_files["PS151"] = psalm_151_raw
    book_codes = dict(BOOK_CODES)
    book_codes["Psalm 151"] = ["PS151"]

    orthodox_all = load_canon_list("orthodox")
    new_testament_books = set(load_canon_list("protestant")[-27:])
    orthodox_ot = [b for b in orthodox_all if b not in new_testament_books]

    missing = [b for b in orthodox_ot if b not in book_codes]
    if missing:
        raise ValueError(f"No USFM mapping for orthodox OT book(s): {missing}")

    out_dir = RAW_DATA_DIR / "septuagint"
    out_dir.mkdir(parents=True, exist_ok=True)

    for book in orthodox_ot:
        codes = book_codes[book]
        parts = []
        for code in codes:
            if code not in usfm_files:
                raise ValueError(f"USFM file for code {code!r} not found in archive")
            parts.append(strip_usfm(usfm_files[code]))
        book_text = "\n\n".join(parts)
        out_path = out_dir / f"{book}.txt"
        out_path.write_text(book_text, encoding="utf-8")

    print(f"Wrote {len(orthodox_ot)} book files to {out_dir}")


if __name__ == "__main__":
    main()
