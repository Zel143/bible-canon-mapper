# Canon Divergence Mapper

A computational comparison of Protestant, Catholic, and Orthodox biblical canons — tracing how textual history, translation lineage, and council decisions shaped three distinct scriptural traditions.

## Research Question

How do textual, source, and historical differences across biblical canons (66-book Protestant, 73-book Catholic, expanded Orthodox) manifest quantifiably — in content overlap, translation lineage, and thematic emphasis?

## Sub-Questions

1. Which books/passages are unique to each canon, and how can this be visualized as a set-overlap or graph structure?
2. Does topic modeling reveal measurable differences in theological emphasis between deuterocanonical books (Tobit, Maccabees, Wisdom) and protocanonical ones?
3. Can we trace a translation lineage (Septuagint → Vulgate → Luther's German Bible → KJV → modern) showing where each tradition's canon decision originated?

## Project Structure

```
canon-divergence-mapper/
├── data/
│   ├── raw/            # original source texts
│   ├── processed/      # cleaned/aligned corpora
│   └── metadata/       # canon lists, council dates, source lineage
├── notebooks/           # analysis notebooks (run in order 01 → 04)
├── src/                 # reusable pipeline code
├── docs/                # proposal draft + historical research journal
└── outputs/             # generated figures and visualizations
```

## Methodology (planned)

- Corpus alignment across canons (Python, spaCy/NLTK)
- Set and graph visualization of canon overlap (NetworkX)
- Topic modeling (BERTopic/LDA) comparing deuterocanonical vs. protocanonical books
- Historical timeline mapping of council decisions and translation lineage

## Data Sources

- Public domain texts: KJV, Douay-Rheims, Orthodox Study Bible (excerpted), Septuagint, Vulgate
- STEP Bible / Bible Gateway API / CCAT for digitized text access
- Historical records: Council of Trent, Council of Carthage/Hippo, Luther's Bible preface

## Scope Note

This project treats canon divergence **descriptively** — documenting what happened historically and why (Reformation-era debates over the Apocrypha, Jerome's *veritas hebraica* position, etc.) — rather than evaluatively judging which canon is "correct." This keeps it defensible as a Computer Science / Data Science thesis while respecting the theological weight of the subject.

## Status

🚧 Data collection and corpus alignment phase.

- ✅ Canon lists structured (`data/metadata/canon_lists.json`) and loadable via `src/data_loader.load_canon_list`
- ✅ Canon overlap pipeline implemented and verified (`notebooks/01_canon_overlap.ipynb`)
- ✅ Translation lineage graph scaffolded (`notebooks/02_translation_lineage.ipynb`) — edges still need source verification
- ✅ KJV (Protestant, 66 books) fetched and parsed into `data/raw/kjv/` via `src/fetch_kjv.py`
- ⏳ Douay-Rheims and Brenton's Septuagint fetchers needed to cover Catholic/Orthodox-only books
- ⏳ Topic modeling (`notebooks/03_topic_modeling.ipynb`) and final visualization (`notebooks/04_visualization.ipynb`) blocked on the above

## Author's Note

This repo doubles as a personal research journal (see `docs/historical_notes.md`) documenting my own exploration of Scripture, history, and faith alongside the technical work.
