# Historical Notes & Personal Research Journal

A running log of historical findings, source citations, and personal reflections as this project develops. Kept separate from the academic notebooks so this can stay honest and personal while the technical work stays rigorous and citable.

## Format for entries

```
### [Date] — [Topic]

**What I found:**


**Source(s):**


**Why it matters (technical):**


**Why it matters (personal):**

```

## Entries

### 2026-07-13 — The Saints Question and 2 Maccabees

**What I found:**

A friend's question about what the Bible says about saints (intercession, prayers for the dead) versus Catholic tradition led me to 2 Maccabees 12:38–46, which explicitly commends prayer and sacrifice for the dead so they may be freed from sin [1]. This passage is a canonical proof-text for Catholics and Orthodox but carries no scriptural weight for Protestants, because 2 Maccabees is deuterocanonical — affirmed as canon at the Council of Hippo (393) and Third Council of Carthage (397) [4], reaffirmed dogmatically by the Council of Trent in response to the Reformation [2], but relocated to a non-canonical "Apocrypha" section by Luther in his 1534 Bible [3]. The doctrinal disagreement about saints/intercession is therefore partly a downstream effect of a prior disagreement about canon, not a standalone dispute over interpretation.

**Source(s):**

[1] 2 Maccabees 12:38–46
[2] Council of Trent, Fourth Session (1546)
[3] Luther's 1534 preface to the Apocrypha
[4] Council of Hippo (393) / Third Council of Carthage (397)

**Why it matters (technical):**

This gives the project a concrete first case study: pick a doctrinally contested passage, check whether it exists in each canon, then trace the canon-formation history around it. That's the analysis pipeline in miniature (`align_corpus.py` + `graph_builder.py`), run on one passage before scaling to the full corpus.

**Why it matters (personal):**

It reframed my own understanding — differences I'd filed under "theological interpretation" are sometimes actually "different source texts." That distinction matters for how I think about which tradition's claims rest on Scripture itself versus how Scripture was bounded in the first place.

---

## References

[1] 2 Maccabees 12:38–46, New American Bible Revised Edition (NABRE), Catholic canon.
[2] Council of Trent, "Decree Concerning the Canonical Scriptures," Fourth Session, Apr. 8, 1546.
[3] M. Luther, "Preface to the Apocrypha," in *Biblia: das ist, die gantze Heilige Schrifft Deudsch*, Wittenberg, 1534.
[4] Council of Hippo, Canon 36 (393 A.D.), confirmed by the Third Council of Carthage (397 A.D.).
