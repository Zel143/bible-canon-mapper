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

### 2026-07-19 — Sourcing the Translation Lineage Graph

**What I found:**

`graph_builder.build_translation_lineage_graph()` shipped with eight placeholder edges, unsourced by design (flagged in its own docstring as needing verification before `notebooks/02_translation_lineage.ipynb` could be treated as more than a structural scaffold). Checking each edge against actual translation history found two that were wrong, not just unsourced, plus a major missing branch:

1. **Wrong: `Hebrew Masoretic Text -> Septuagint`.** The Septuagint (translated c. 250–132 BC [6]) predates the Masoretes (who codified and vocalized the Hebrew text c. 7th–10th century AD) by roughly a millennium — it cannot descend from their work. Worse, modern textual criticism (corroborated by Dead Sea Scroll manuscripts like 4QJer-b/d and 4QSam-a) shows the LXX's Hebrew Vorlage was in places a *different* Hebrew text-type from the one that became the Masoretic tradition, not an earlier draft of it [7]. Fixed by replacing both "Hebrew Masoretic Text" edges with a single "Hebrew Source Texts (Second Temple era, textually plural)" ancestor node that branches to both the Septuagint and (separately) the later-codified Masoretic Text, rather than putting one downstream of the other.

2. **Unsupported: `Luther's Bible (1534) -> King James Version (1611)`.** Found no documented textual dependency of the KJV on Luther's German Bible. The real, heavily-documented English-line ancestry the old graph omitted entirely: the 1604 translators' instructions named the Bishops' Bible (1568) as base text, with Tyndale's, Coverdale's, Matthew's, the Great Bible's ("Whitchurch's"), and the Geneva Bible's wording to be preferred wherever they fit the original languages better [8]. In practice Tyndale's wording is estimated at up to ~80% of the KJV New Testament [9] — a far stronger claim than anything connecting Luther's Bible to the KJV. Dropped the Luther edge; added the Tyndale -> Great Bible -> Bishops' Bible -> KJV chain plus Tyndale -> KJV and Geneva Bible -> KJV directly, per the translators' own stated instructions.

3. **Needed nuance, not removal: `Vulgate -> Luther's Bible`.** Luther's translation team's primary sources were Hebrew (Caspar Cruciger brought "the Hebrew and Chaldee") and Erasmus's Greek New Testament, 2nd edition, 1519 [10][11] — the Vulgate (via Johannes Bugenhagen) was a *consulted reference*, not a primary source text the way it was for Douay-Rheims. Kept the edge but annotated it `reference, not primary source` in the graph's edge metadata rather than deleting it, since Luther's team did have and use it.

4. **Needed nuance: Vulgate's own sourcing.** Jerome translated the protocanonical Old Testament directly from Hebrew (390–405 AD, his stated *hebraica veritas* principle), but for most of the deuterocanonical books he didn't retranslate — Wisdom, Sirach, Baruch, and 1–2 Maccabees were retained from the existing Old Latin (Vetus Latina, itself Septuagint-based); only Tobit and Judith got fresh translation work, from Aramaic [12]. The New Testament is a revision of the Old Latin Gospels against Greek manuscripts, not a fresh translation [13]. Split the old single `Vulgate` predecessor into Masoretic Text (protocanonical OT), Old Latin (most deuterocanonical books), and Greek NT (Gospels revision) — the Vulgate is genuinely a three-source text, not a two-hop chain.

5. **Confirmed as correctly sourced already:** `Vulgate -> Douay-Rheims` — the Council of Trent's 1546 decree named the Vulgate the Church's authentic Latin text [2], and Douay-Rheims is a translation of it, not of the Hebrew/Greek directly. `Hebrew (Ben Chayyim/Bomberg edition, 1524–25) -> King James Version` — this specific printed Hebrew edition is the one generally identified as the KJV Old Testament translators' source text [14].

**Source(s):**

See references [2], [6]–[14] below.

**Why it matters (technical):**

`graph_builder.build_translation_lineage_graph()` rewritten with these corrections — 14 nodes, edges carrying `date` and `note` attributes (approximate date, and either a citation number or `reference, not primary source` / `standardization, not translation` for edges that aren't simple source-language translations). `notebooks/02_translation_lineage.ipynb` re-run against it; no longer a placeholder scaffold.

**Why it matters (personal):**

The Septuagint/Masoretic error is the more interesting one to sit with: it's not that the graph had the wrong *direction* on a real relationship, it's that "the Hebrew Bible" isn't one static thing that Greek and Latin and German translators each took a copy of at different points — there were multiple Hebrew textual traditions circulating well into the Second Temple period, and picking which one to translate was itself a real choice with theological weight (Jerome's whole *hebraica veritas* argument is exactly about defending one such choice against pushback from people who trusted the Septuagint instead). That's the same shape as the 2 Maccabees canon-boundary question logged above, one level deeper: not just "which books count," but "which text of a book counts," and both turn out to be historically contingent decisions rather than settled facts I'd been assuming when I built the placeholder graph.

## References

[1] 2 Maccabees 12:38–46, New American Bible Revised Edition (NABRE), Catholic canon.
[2] Council of Trent, "Decree Concerning the Canonical Scriptures," Fourth Session, Apr. 8, 1546.
[3] M. Luther, "Preface to the Apocrypha," in *Biblia: das ist, die gantze Heilige Schrifft Deudsch*, Wittenberg, 1534.
[4] Council of Hippo, Canon 36 (393 A.D.), confirmed by the Third Council of Carthage (397 A.D.).
[5] 2 Kings 13:20–21, King James Version (KJV).
[6] Dating of the Septuagint's translation (Pentateuch c. 250 BC per the *Letter of Aristeas* tradition; remaining books completed by c. 132 BC per the prologue to Sirach) — see the Septuagint entry in standard biblical-studies reference works (e.g. *Britannica*, "Septuagint").
[7] E. Tov's classification of Dead Sea Scroll biblical manuscripts identifies a distinct "pre-Septuagint" Hebrew text-type (e.g. 4QJer-b, 4QJer-d, 4QSam-a) alongside proto-Masoretic manuscripts, confirming textual plurality in the Hebrew tradition the LXX translators drew from — summarized in scroll-classification literature following Tov's *Textual Criticism of the Hebrew Bible*.
[8] "Rules to Be Observed in the Translation of the Bible" (1604), the fifteen instructions issued to the King James translators, rule 1 (Bishops' Bible as base) and rule 14 (permitted alternate translations: Tyndale's, Matthew's, Coverdale's, Whitchurch's [Great Bible], Geneva).
[9] Widely-cited textual comparison of KJV New Testament wording against Tyndale's translation, commonly given as ~80–84% overlap in KJV translation-history scholarship; a secondary-source figure, not from a single primary document, and worth pinning to a specific peer-reviewed count if this graph is cited in the thesis itself.
[10] Historical accounts of the 1534 Luther Bible's collaborative translation team (Melanchthon, Cruciger, Bugenhagen, Jonas, Rörer et al.) and each member's role — see e.g. the Musée protestant's account of Luther as Bible translator.
[11] Erasmus, *Novum Instrumentum omne* (1516), 2nd ed. 1519 — the Greek New Testament edition Luther's translation team used as a primary NT source.
[12] Jerome's prefaces to his Vulgate translations (e.g. the preface to Judith, describing his method) and standard Vulgate reference histories, on which books he retranslated from Hebrew/Aramaic versus retained from the Vetus Latina.
[13] Standard Vulgate reference histories (e.g. *Britannica*, "Vulgate") on the Vulgate New Testament as a revision of Old Latin Gospel texts against Greek manuscripts rather than a fresh translation.
[14] The Second Rabbinic Bible (Bomberg, 1524–25, text established by Jacob ben Chayyim) as the Hebrew Old Testament edition generally identified with the King James translators' source text — see standard KJV textual-history references.
