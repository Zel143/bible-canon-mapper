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

### 2026-07-13 — Elisha's Bones (2 Kings 13:20–21) as a Contrast Case

**What I found:**

Verified 2 Kings 13:20–21: after Elisha's death, a dead man is hastily thrown into Elisha's tomb to escape a Moabite raiding party, and "when the man was let down, and touched the bones of Elisha, he revived, and stood up on his feet" [5]. Unlike the 2 Maccabees 12:38–46 case logged above, this passage is **protocanonical** — accepted as Scripture without dispute by Protestant, Catholic, and Orthodox traditions alike. There is no canon-formation controversy attached to it.

That makes it a useful contrast case rather than another instance of the same pattern. Both passages involve God acting through the remains of a deceased holy person, yet only the deuterocanonical one (2 Maccabees, tied to prayer for the dead / intercession) became a canon fault line, while this protocanonical episode (tied to relics) is uncontested Scripture across all three traditions. The doctrinal split over relics and intercession isn't a split over whether "God acting through remains after death" is biblical at all — it clearly is, in universally accepted text — it's specifically about which *later, contested* books codify practices (prayer for the dead, veneration) built on that pattern.

**Source(s):**

[5] 2 Kings 13:20–21

**Why it matters (technical):**

Good test case for `align_corpus.py`: since 2 Kings is present in all three canon lists, this passage should show up with all three "traditions" flags true in the overlap matrix, unlike the 2 Maccabees case which is catholic/orthodox-only. Pairing a contested and uncontested passage on a related theme is a useful validation pair once the pipeline is running on real data — it also suggests the eventual topic model should track *theme* presence separately from *canon* presence, since a theme can recur across both protocanonical and deuterocanonical material.

**Why it matters (personal):**

Sharpened the earlier reframing: it's not that the underlying theological ideas around death, intercession, or relics are absent from Protestant Scripture — this passage is right there in every Bible. The divide is narrower and more specific than "different theology" — it's about which later texts elaborating on a shared biblical pattern got bounded in or out as canon.

---

## References

[1] 2 Maccabees 12:38–46, New American Bible Revised Edition (NABRE), Catholic canon.
[2] Council of Trent, "Decree Concerning the Canonical Scriptures," Fourth Session, Apr. 8, 1546.
[3] M. Luther, "Preface to the Apocrypha," in *Biblia: das ist, die gantze Heilige Schrifft Deudsch*, Wittenberg, 1534.
[4] Council of Hippo, Canon 36 (393 A.D.), confirmed by the Third Council of Carthage (397 A.D.).
[5] 2 Kings 13:20–21, King James Version (KJV).
