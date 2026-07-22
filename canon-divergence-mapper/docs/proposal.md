# Thesis Proposal Draft

## Title
Mapping Canon Divergence: A Computational Comparison of Protestant, Catholic, and Orthodox Biblical Traditions

## Abstract (draft)
[Write 150–250 words summarizing the research question, method, and expected contribution once initial data exploration is done.]

## 1. Research Question
How do textual, source, and historical differences across biblical canons manifest quantifiably — in content overlap, translation lineage, and thematic emphasis?

## 2. Sub-Questions
1. Which books/passages are unique to each canon, and how can this be visualized as a set-overlap or graph structure?
2. **(Revised 2026-07-22 — see `docs/thesis.md`'s scope-change note.)** The project's text pipeline is now restricted to the Protestant Bible (KJV) as sole source, which removes the deuterocanonical books from the active corpus. Original question: does topic modeling reveal measurable differences in theological emphasis between deuterocanonical and protocanonical books? Current question: within the Protestant/KJV corpus, does topic modeling reveal measurable differences between Old and New Testament passages? The original comparison is preserved in git history and remains a candidate for reinstatement — see `docs/thesis.md` §6.
3. Can a translation lineage graph (Septuagint → Vulgate → Luther's Bible → KJV → modern) be constructed to show where canon decisions originated?

## 3. Background / Motivation

This project started with a question I couldn't answer cleanly: a friend asked me what the Bible actually says about saints, versus what Catholic tradition holds. Trying to answer honestly, I kept running into the same complication — the traditions aren't just interpreting the same text differently, they're working from different texts. Doctrines I'd assumed were purely theological disagreements (intercession of saints, prayers for the dead) turned out to be partly downstream of which books each tradition counts as Scripture in the first place — 2 Maccabees, for instance, is canonical for Catholics and Orthodox and excluded for Protestants, and it's a direct proof-text for prayer for the dead [1].

That sent me looking for the history: how the canon boundary actually got drawn, by whom, and when. As someone trying to know Christ personally — through Scripture and lived experience — and find a Christian community that lives that out, this isn't abstract to me. It bears directly on what counts as authoritative in the first place.

It also gave me a natural place to bring my training to bear. As a Computer Science student specializing in data science, I wanted to see whether questions that are usually settled by citing councils and creeds could instead be shown — set overlap, topic modeling, lineage graphs — using the same tools I'd use on any other corpus. This project treats the question computationally and historically rather than devotionally: not "which canon is right," but what the textual and historical record shows about how and why the traditions diverged, using the methods of my field to make that divergence visible and quantifiable.

See `docs/historical_notes.md` for the case study that prompted this (the saints/2 Maccabees question) and the full source list.

## 4. Related Work
- Digital humanities projects on biblical corpora (e.g., STEP Bible, Blue Letter Bible tools)
- Computational stylometry / authorship studies on biblical texts
- Prior canon-comparison scholarship (historical, non-computational) to cite as grounding

## 5. Data Sources
- KJV (active text source as of 2026-07-22 — see `docs/thesis.md` scope-change note); Douay-Rheims and Brenton's Septuagint were also fetched and used for an earlier version of the topic-modeling comparison, and remain in the repository but are not part of the active pipeline
- Historical records: Council of Trent, Council of Carthage/Hippo, Luther's preface to the Apocrypha (used for canon-list metadata and translation lineage, unaffected by the text-source scope change)

## 6. Methodology
- Corpus collection and cleaning (KJV only, as of 2026-07-22)
- Canon set-comparison (overlap graph via NetworkX) — still covers all three traditions, built from canon-list metadata rather than comparative text
- Topic modeling (LDA) — Old Testament vs. New Testament within the KJV corpus (revised scope; originally deuterocanonical vs. protocanonical, see `docs/thesis.md` §4.3–4.4)
- Translation lineage graph construction — still covers all three traditions
- Visualization (currently static matplotlib panels; interactive Plotly/D3 remains a planned upgrade, not yet built)

## 7. Expected Contribution
A reusable open-source toolkit + dataset for canon comparison, plus a historically grounded account of *why* divergence occurred — useful for both CS/DS methodology demonstration and interdisciplinary theology/digital-humanities audiences.

## 8. Timeline (draft — adjust to your program's requirements)
| Phase | Duration | Deliverable |
|---|---|---|
| Data collection & cleaning | 3–4 weeks | `data/raw`, `data/processed` populated |
| Canon overlap analysis | 2 weeks | Notebook 01 complete, overlap graph |
| Translation lineage research | 2–3 weeks | Notebook 02 complete |
| Topic modeling | 3 weeks | Notebook 03 complete |
| Visualization + writeup | 3 weeks | Final notebook, thesis draft |

## 9. Scope Guardrails
- Descriptive, not evaluative — document historical divergence without adjudicating theological correctness
- Keep computational contribution central (this is a CS/DS thesis, not a theology thesis)
