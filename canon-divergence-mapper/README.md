# Canon Divergence Mapper

A computational comparison of Protestant, Catholic, and Orthodox biblical canons — tracing how textual history, translation lineage, and council decisions shaped three distinct scriptural traditions.

## Research Question

How do textual, source, and historical differences across biblical canons (66-book Protestant, 73-book Catholic, expanded Orthodox) manifest quantifiably — in content overlap, translation lineage, and thematic emphasis?

## Sub-Questions

1. Which books/passages are unique to each canon, and how can this be visualized as a set-overlap or graph structure?
2. **Revised 2026-07-22:** the text pipeline is now restricted to the Protestant Bible (KJV) only — see `docs/thesis.md`'s scope-change note. Within that corpus: does topic modeling reveal measurable differences between Old and New Testament passages? (Original question — deuterocanonical vs. protocanonical emphasis — is preserved in git history, not currently answerable from the active corpus.)
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

## Methodology

- Corpus cleaning (KJV only, as of the 2026-07-22 scope change)
- Set and graph visualization of canon overlap (NetworkX) — still covers all three traditions, from canon-list metadata
- Topic modeling (LDA) comparing Old Testament vs. New Testament passages within the KJV corpus (revised scope; originally deuterocanonical vs. protocanonical — see `docs/thesis.md`)
- Historical timeline mapping of council decisions and translation lineage — still covers all three traditions

## Data Sources

- **Active:** King James Version (Project Gutenberg #10) — the sole text source as of 2026-07-22.
- **Fetched, not currently active:** Douay-Rheims (Project Gutenberg #1581), Brenton's Septuagint (eBible.org) — used in an earlier version of the topic-modeling comparison; fetchers and raw data remain in the repo, recoverable via git history (`docs/thesis.md` Appendix).
- Historical records (canon-list metadata and translation lineage, unaffected by the text-source scope change): Council of Trent, Council of Carthage/Hippo, Luther's Bible preface.

## Scope Note

This project treats canon divergence **descriptively** — documenting what happened historically and why (Reformation-era debates over the Apocrypha, Jerome's *veritas hebraica* position, etc.) — rather than evaluatively judging which canon is "correct." This keeps it defensible as a Computer Science / Data Science thesis while respecting the theological weight of the subject.

**Scope change, 2026-07-22:** the project's text pipeline was deliberately narrowed to the Protestant Bible (KJV, 66 books) as sole source. Canon overlap (Sub-Question 1) and translation lineage (Sub-Question 3) are unaffected — both are built from canon-list metadata and historical sourcing, not comparative Bible text — but the topic-modeling comparison (Sub-Question 2) could no longer test deuterocanonical vs. protocanonical content, since those books fall outside the Protestant canon. See `docs/thesis.md`'s scope-change note and §4.3–4.4 for the full account, including what was preserved from the original analysis and what remains open.

## Status

✅ All four notebooks (`01`–`04`) run end-to-end.

- ✅ Canon lists structured (`data/metadata/canon_lists.json`) and loadable via `src/data_loader.load_canon_list`
- ✅ Canon overlap pipeline implemented and verified (`notebooks/01_canon_overlap.ipynb`)
- ✅ Translation lineage graph sourced, 14 nodes / 20 dated+cited edges (`notebooks/02_translation_lineage.ipynb`)
- ✅ KJV (Protestant, 66 books) fetched and parsed into `data/raw/kjv/` via `src/fetch_kjv.py` — the corpus's sole active source as of 2026-07-22
- ✅ Topic modeling (`notebooks/03_topic_modeling.ipynb`): Old Testament vs. New Testament passages, KJV corpus (revised scope)
- ✅ Combined visualization (`notebooks/04_visualization.ipynb`)
- ⏳ First full thesis draft in `docs/thesis.md`, revised for the current scope — see its §5.4/§6 for open items, including whether to reinstate the original cross-canon topic comparison

## Author's Note

This repo doubles as a personal research journal (see `docs/historical_notes.md`) documenting my own exploration of Scripture, history, and faith alongside the technical work.
