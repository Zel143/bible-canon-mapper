# Mapping Canon Divergence: A Computational Comparison of Protestant, Catholic, and Orthodox Biblical Traditions

**Status: first full draft.** This synthesizes the completed pipeline (`src/`, `notebooks/01`–`04`) and the research log in `docs/historical_notes.md` into thesis form. It is not a finished submission — see the "Limitations and Open Items" section (5.4) for what still needs work before this goes to a committee.

## Abstract

Protestant, Catholic, and Orthodox Bibles disagree about which books belong in the Old Testament — 66, 73, and roughly 77–81 books respectively, depending on jurisdiction — and that disagreement is often discussed in exclusively historical or theological terms: council decisions, confessional statements, patristic testimony. This thesis treats the disagreement computationally instead, building a small open-source pipeline that (1) represents canon membership as a structured, queryable dataset rather than prose description, (2) traces which translations and source-language texts fed into which later Bibles, with each claim dated and cited, and (3) tests, using topic modeling, whether the deuterocanonical books that separate the Catholic and Orthodox canons from the Protestant one are thematically distinguishable from the protocanonical books all three traditions share. The topic model finds a real, non-trivial signal: deuterocanonical passages concentrate heavily in two topics — a narrative/political-history topic and a wisdom/moral-exhortation topic — that protocanonical passages are comparatively underrepresented in. That finding was then stress-tested against the most obvious alternative explanation — that deuterocanonical books simply cluster in underrepresented genres — by comparing protocanonical and deuterocanonical passages within matched genre categories; the effect survives for the genre (historical narrative) carrying most of the deuterocanonical text, growing rather than shrinking once genre is held constant, while genre does explain roughly half the effect within wisdom literature. A subsequent topic-count and random-seed sensitivity sweep — spanning topic counts from 4 to 28 and, separately, held-out perplexity and topic-coherence scoring — confirms this genre-confound result is not an artifact of the specific model configuration used: it holds across every random seed tested and at 9 of 11 candidate topic counts, failing only at the smallest count tested (too coarse to represent the distinction at all) and one other isolated value. The translation lineage graph, built from primary and secondary historical sources rather than assumption, corrects two claims that seemed intuitive but turn out to be unsupported or anachronistic once checked. The result is a small, reusable toolkit and dataset for canon comparison, plus a worked example of using standard NLP methods to make a historically contingent, doctrinally consequential fact — which books are Scripture — visible as data rather than only as doctrine.

## 1. Introduction

### 1.1 Research Question

How do textual, source, and historical differences across the Protestant, Catholic, and Orthodox biblical canons manifest quantifiably — in content overlap, translation lineage, and thematic emphasis?

**Sub-questions:**

1. Which books are unique to each canon, and how can this be represented and visualized as a set-overlap or graph structure?
2. Does topic modeling reveal a measurable difference in emphasis between the deuterocanonical books (Tobit, Judith, 1–2 Maccabees, Wisdom, Sirach, Baruch) and the protocanonical books all three traditions share?
3. Can a translation lineage — which source texts and prior translations fed into which later ones — be constructed and *sourced*, rather than asserted, to show where each tradition's canon and text ultimately trace back to?

### 1.2 Motivation

The proximate motivation was a specific question: what does the Bible say about the intercession of saints and prayer for the dead, versus what Catholic tradition holds? Chasing that question honestly led to 2 Maccabees 12:38–46, which explicitly commends prayer and sacrifice for the dead — a passage that is canonical Scripture for Catholics and Orthodox and has no scriptural status for Protestants, because 2 Maccabees is a deuterocanonical book: affirmed as canon at the Councils of Hippo (393) and Carthage (397), reaffirmed dogmatically by the Council of Trent (1546) in response to the Reformation, but moved to a non-canonical "Apocrypha" section in Luther's 1534 Bible [4][5][6]. A doctrinal disagreement that looked, on its face, like a dispute over interpreting a shared text turned out to be partly a downstream consequence of a *prior* disagreement about which texts count as Scripture at all.

That distinction — theological interpretation of shared Scripture versus disagreement rooted in different source texts — is not always obvious from the outside, and it is not always the case. As a contrast case, 2 Kings 13:20–21 (a dead man revived by contact with the bones of the prophet Elisha) involves the same broad pattern as 2 Maccabees — God acting through the remains of a deceased holy person — but is protocanonical, accepted without dispute in all three traditions [7]. The doctrinal split over relics and intercession is not a split over whether that pattern appears in universally accepted Scripture; it does. It is specifically about which later, contested books elaborate that pattern into practice. This pairing — one contested passage, one uncontested passage, on a related theme — became the seed case for the whole project: pick a passage, check its canon status across traditions, then check whether the *content* of contested and uncontested material is thematically distinguishable at scale, not just in this one pair.

This project also gave a natural place to bring quantitative training to bear on a question usually settled by citing councils and creeds. As a computer science / data science project, it treats the canon-divergence question the way one would treat any other corpus-comparison problem: set overlap, topic modeling, and lineage-graph construction, applied to a domain (biblical canon history) that is not usually approached with these tools.

### 1.3 Scope and Guardrails

This project is **descriptive, not evaluative**: it documents what happened historically and why (Reformation-era debates over the Apocrypha, Jerome's *hebraica veritas* position, conciliar decisions) without adjudicating which canon is theologically correct. This is both a methodological commitment and what makes the project viable as a computer science / data science thesis rather than a theology thesis: the computational contribution (a reusable canon-comparison pipeline, a sourced lineage graph, a topic-modeling result) is the deliverable, and the historical material is treated as data to be modeled, not doctrine to be settled.

## 2. Related Work

Digital humanities projects on biblical corpora (e.g., STEP Bible, Blue Letter Bible's tools) provide the closest prior art for structured, queryable biblical text, though typically oriented toward lookup and cross-referencing rather than comparative set/topic analysis across canon traditions. Computational stylometry and authorship studies on biblical texts (a substantial existing literature, not surveyed in detail here) establish that standard NLP methods are applicable to this text domain. Canon-comparison scholarship proper is extensive but almost entirely historical and non-computational — councils, patristic testimony, confessional documents — and is the primary source material this project draws its lineage-graph and case-study citations from (see References and `docs/historical_notes.md`).

**Open item:** this section needs specific citable digital-humanities and computational-stylometry papers, not just categories, before this thesis is submission-ready. Flagged rather than filled with placeholder citations, per the project's own standard of not asserting unsourced claims (see Section 5.4).

## 3. Data and Methodology

### 3.1 Canon Definitions

Canon membership for each tradition is stored as structured data (`data/metadata/canon_lists.json`), not prose: the Protestant list (39 Old Testament + 27 New Testament books) is the base; the Catholic list adds 7 deuterocanonical books (Tobit, Judith, 1–2 Maccabees, Wisdom, Sirach, Baruch) plus textual additions to Esther and Daniel not counted as separate books, for 73 total; the Orthodox list adds 4 more (1 Esdras, 3 Maccabees, Prayer of Manasseh, Psalm 151) under one commonly cited Greek/Rahlfs-based baseline, for 77 total. `src/data_loader.load_canon_list(tradition)` loads these programmatically. The Orthodox list is explicitly documented as one baseline among several — Slavonic, Georgian, and Ethiopian jurisdictions include additional books (2 Esdras/4 Ezra, 4 Maccabees, Jubilees, 1 Enoch) not represented here; cross-checking against a specific jurisdiction remains open (Section 5.4).

### 3.2 Source Texts

Three public-domain source translations were fetched and parsed into one plain-text file per book (`src/fetch_kjv.py`, `src/fetch_douay_rheims.py`, `src/fetch_septuagint.py`):

- **King James Version** (Project Gutenberg eBook #10) — Protestant, 66 books, Masoretic-Hebrew/Textus-Receptus-Greek based.
- **Douay-Rheims**, Challoner revision (Project Gutenberg eBook #1581) — full 73-book Catholic canon in one consistent, Vulgate-based translation.
- **Brenton's Septuagint** (eBible.org, USFM format) — the full 50-book Orthodox Old Testament (Brenton's translation has no New Testament) from one consistent Greek-based translation.

Each fetcher required nontrivial text-processing work beyond a bulk download: matching Gutenberg section headings to canonical book names, handling archaic spelling variants (e.g. "Josue" for Joshua, "Machabees" for Maccabees in Douay-Rheims), splitting Psalm 151 out of a merged Psalms file, reassembling Daniel and Baruch from USFM files that split out their deuterocanonical portions (Susanna, Bel and the Dragon, and the Epistle of Jeremy respectively) as separate books rather than folding them in as the Vulgate tradition does. A real encoding bug was found and fixed during this work: `Path.write_text` on Windows was doubling the already-present `\r\n` line endings in the downloaded Gutenberg text into `\r\r\n`, which silently truncated wrapped verses during later cleaning — caught by actually inspecting output rather than assuming a successful download meant correct output.

### 3.3 Canonical Source Selection per Tradition

Because all three source texts are now available, a shared book (e.g. Genesis) exists in up to three different translations. Rather than arbitrarily picking one, or blending them, `src/align_corpus.py` assigns each tradition the source closest to its own textual basis (`CANONICAL_SOURCES`):

| Tradition | Source | Rationale |
|---|---|---|
| Protestant | KJV | Masoretic-based, the only Protestant-specific source fetched |
| Catholic | Douay-Rheims | Vulgate-based, one consistent translation across the full 73-book canon |
| Orthodox | Septuagint (OT), KJV (NT) | The Septuagint is the Orthodox canon's actual textual basis (Greek, not Masoretic) for the Old Testament; Brenton's translation has no New Testament, so Orthodox NT books fall back to the KJV, whose Textus Receptus is closer to the Byzantine text Orthodox churches use liturgically than the Vulgate-derived Douay-Rheims New Testament |

This choice matters specifically for Section 4.3: comparing protocanonical and deuterocanonical *content* only makes sense if both come from the same translation, so that any topic difference reflects the underlying text rather than translator word choice. The Catholic corpus (Douay-Rheims throughout) is used for exactly this reason.

### 3.4 Corpus Cleaning

`src/build_processed_corpus.py` reads each tradition's canonical-source text via `align_corpus.load_book_text` and writes cleaned plain text to `data/processed/<tradition>/<book>.txt` (216 files: 66 Protestant + 73 Catholic + 77 Orthodox), plus `data/processed/corpus_manifest.json` recording the canon overlap matrix and per-book source/word/character counts. Cleaning removes non-scriptural editorial matter (book introductions, "Chapter N" headings, per-chapter summary blurbs present in the Gutenberg editions) and strips `chapter:verse` markers — including markers embedded mid-paragraph in chapters formatted without per-verse line breaks (e.g. Matthew's genealogy) — down to continuous prose. The Septuagint source, already reduced to plain prose during USFM-to-text conversion at fetch time, only needs whitespace normalization here.

### 3.5 Topic Modeling Methodology

Books in the Catholic corpus are labeled **protocanonical** (also in the Protestant list; 66 books) or **deuterocanonical** (Catholic-only; 7 books), then split into passages of 150 words each (final partial passage per book dropped if under 30 words), yielding 5,953 passages (5,267 protocanonical, 686 deuterocanonical) across all 73 books. Passages, not whole books or chapters, are the unit of analysis: a single topic label per book would be too coarse to say anything about emphasis *within* a book, and chapter-level chunking was not available because chapter markers are deliberately removed during corpus cleaning (Section 3.4). A fixed 150-word window is a pragmatic substitute for chapter-level chunking, not a claim that it is the ideal passage boundary.

Passages are vectorized as bag-of-words (`sklearn.feature_extraction.text.CountVectorizer`, English stopwords removed, `max_df=0.9`, `min_df=3`, vocabulary capped at 2,000 terms — 5,953 passages × 2,000 terms) and fit with Latent Dirichlet Allocation [15] (`sklearn.decomposition.LatentDirichletAllocation`, 12 topics, `random_state=42`, 20 iterations). Each passage is assigned its highest-probability (dominant) topic. LDA was chosen over an embedding-based method (e.g. BERTopic) specifically to avoid a multi-gigabyte dependency install (torch, sentence-transformers, UMAP, HDBSCAN) that was not justified for a first pass; the topic count (12) was a starting point, subsequently checked for stability and tuning sensitivity in Section 4.5.

### 3.6 Translation Lineage Methodology

`src/graph_builder.build_translation_lineage_graph()` constructs a directed acyclic graph of 14 texts and 20 lineage edges, each carrying an approximate date and a note — either a citation into the reference list below or a qualifier distinguishing the edge type (e.g. "standardization, not translation" for the Masoretes' codification of an existing Hebrew tradition; "reference, not primary source" for a text a translator consulted without translating from). Every edge was checked individually against historical sources rather than assumed; two edges present in an earlier, explicitly-flagged-as-placeholder version of this graph turned out to be wrong on inspection, not merely unsourced (Section 4.2, and the full research log in `docs/historical_notes.md`).

## 4. Results

### 4.1 Canon Overlap

The presence/absence matrix (`src/align_corpus.align_books`, run on the three canon lists) confirms: 0 books unique to the Protestant list, 0 unique to the Catholic list, and exactly 4 unique to the Orthodox list (1 Esdras, 3 Maccabees, Prayer of Manasseh, Psalm 151) — consistent with the Protestant and Catholic lists both being proper subsets of the Orthodox list under this dataset's baseline Orthodox definition (Section 3.1). The bipartite overlap graph (`notebooks/01_canon_overlap.ipynb`, `outputs/figures/canon_overlap_graph.png`) has 3 tradition nodes, 77 book nodes, and 216 edges. As a spot-check against the case studies motivating this project (Section 1.2): 2 Maccabees resolves to Catholic/Orthodox-only (`{'protestant': False, 'catholic': True, 'orthodox': True}`), and 2 Kings resolves to present in all three — matching the documented canon status of both passages exactly.

### 4.2 Translation Lineage

Two corrections were made against the graph's earlier placeholder edges, documented in full in `docs/historical_notes.md` ("Sourcing the Translation Lineage Graph," 2026-07-19):

1. **The Septuagint does not descend from the Masoretic Text.** The original placeholder graph had a `Hebrew Masoretic Text -> Septuagint` edge. This is anachronistic: the Septuagint was translated c. 250–132 BC [8], while the Masoretes codified and vocalized the Hebrew Masoretic Text roughly a millennium later (7th–10th century AD). Worse, Dead Sea Scroll evidence shows the Septuagint's Hebrew source text (Vorlage) differed in places from the Hebrew text-type that became the Masoretic tradition, rather than being an earlier draft of it [9]. The corrected graph gives both the Septuagint and the Masoretic Text a common ancestor — "Hebrew Source Texts (Second Temple era, textually plural)" — rather than deriving one from the other.

2. **No documented dependency of the King James Version on Luther's Bible.** The placeholder graph asserted a direct `Luther's Bible (1534) -> King James Version (1611)` edge. No such textual dependency is documented; what the placeholder graph omitted entirely is the real, heavily-documented English-Bible lineage. The 1604 rules governing the KJV translators named the Bishops' Bible (1568) as base text, with Tyndale's, Coverdale's, Matthew's, the Great Bible's, and the Geneva Bible's wording to be preferred wherever it fit the original languages better [10]; a computer-assisted sampling study estimates Tyndale's wording at ~84% of the KJV New Testament, and ~76% of the Old Testament portions he completed before his 1536 execution [11]. The corrected graph replaces the Luther edge with `Tyndale's Bible -> Great Bible -> Bishops' Bible -> King James Version`, plus direct edges from Tyndale's Bible and the Geneva Bible to the KJV per the translators' own stated instructions.

A third edge, `Vulgate -> Luther's Bible`, was kept but re-annotated rather than removed: Luther's translation team's primary sources were Hebrew (via team member Caspar Cruciger [12]) and Erasmus's Greek New Testament [13], with the Vulgate serving as a consulted reference (brought by team member Johannes Bugenhagen [12]) rather than a primary source text — a real distinction the earlier version of the graph did not make. The Vulgate's own upstream sourcing was similarly split into its three actual components rather than one generic "Vulgate" predecessor: the Masoretic Hebrew tradition for the protocanonical Old Testament (Jerome's *hebraica veritas* translations, 382–405 AD), the Old Latin (Vetus Latina) for most deuterocanonical books Jerome retained rather than retranslated (Wisdom, Sirach, Baruch, 1–2 Maccabees) [14], and Greek New Testament manuscripts for Jerome's revision of the Old Latin Gospels.

The resulting graph (`notebooks/02_translation_lineage.ipynb`, `outputs/figures/translation_lineage_graph.png`) is a valid directed acyclic graph — verified programmatically (`networkx.is_directed_acyclic_graph`) — of 14 texts and 20 dated, cited edges.

### 4.3 Topic Modeling: Protocanonical vs. Deuterocanonical

Fitting LDA on the 5,953-passage Catholic corpus produces 12 topics with clearly interpretable top-word lists — e.g. Topic 7 ("king, son, lord, israel, juda, house, jerusalem, years, david, solomon") reads as royal/dynastic narrative; Topic 3 ("shall, offer, altar, sacrifice, thereof, cubits, seven, day, lord, sin") reads as cultic/sacrificial law; Topic 11 ("thou, thy, thee, shalt, lord, hast, shall, god, art, wilt") reads as archaic second-person direct address (exhortation/covenant language).

Comparing topic distribution *within* each category (i.e. what fraction of each category's passages land in each topic, correcting for protocanonical passages outnumbering deuterocanonical roughly 8-to-1) shows two topics where deuterocanonical passages are substantially overrepresented relative to protocanonical ones:

| Topic | Top words | Deuterocanonical share | Protocanonical share |
|---|---|---|---|
| 0 | jews, came, great, men, city, went, people, king, jerusalem, day | 26.1% | 3.1% |
| 8 | god, hath, things, man, shall, lord, unto, good, let, heart | 40.2% | 16.0% |

Topic 0 reads as historical/political narrative centered on Jerusalem and named political actors — consistent with 1–2 Maccabees' subject matter (Hellenistic-era wars and Jewish political history). Topic 8 reads as general moral/wisdom exhortation — consistent with Wisdom and Sirach's genre. Conversely, protocanonical passages are overrepresented (relative to their already-larger base rate) in Topic 10 ("shall, lord, hath, saith, come, earth, people, land, man, god," 21.9% vs. 6.6%) and Topic 1 ("said, shall, jesus, man, saying, come, say, came, god, behold," 10.2% vs. 0.4%) — the latter almost certainly picking up Gospel narrative material (the word "jesus" is a strong marker), which has no deuterocanonical counterpart at all since the New Testament is identical across all three canons.

As a direct sanity check against the case-study pair from Section 1.2: 2 Maccabees' passages are dominated by Topic 0 (71 of 108 passages, 65.7%) with a secondary concentration in Topic 8 (21 passages, 19.4%). 2 Kings' passages are dominated by Topic 7 — the royal/dynastic narrative topic (76 of 156 passages, 48.7%) — with a secondary concentration in Topic 5 ("said, king, lord, hath, god, man, father, answered, let, thee," 39 passages, 25.0%), a topic reading as court/dialogue narrative. Both books are historical narrative in genre, and both get narrative-flavored dominant topics, but *different* narrative topics: 2 Kings clusters with royal/dynastic vocabulary, 2 Maccabees with a topic more focused on collective political actors ("jews," "people," "city") than named kings. This is a real, if modest, distinction — consistent with 2 Maccabees' actual content (a Hellenistic-era account of a people's political and religious resistance) differing in emphasis from 2 Kings' court-centered dynastic history, even though both are canonically "historical narrative" and both are protocanonical-adjacent in genre.

### 4.4 Testing the Genre Confound

Section 4.3's topic-distribution difference is consistent with a simpler explanation than "deuterocanonical content is thematically distinct": the seven deuterocanonical books happen to concentrate in genres (Hellenistic historical narrative for Tobit, Judith, and 1–2 Maccabees; wisdom literature for Wisdom and Sirach) that are comparatively underrepresented among the 39 protocanonical books, so a pure genre effect could produce the Section 4.3 result without any distinctively deuterocanonical content difference at all. This was tested directly by assigning each of the 46 Old Testament books (the 27 New Testament books are excluded — no deuterocanonical book has an NT counterpart) to one of four standard genre categories — Law, Historical Narrative, Wisdom/Poetic, Prophetic — and comparing protocanonical against deuterocanonical topic distributions *within* each genre that contains both (Law is excluded: none of the seven deuterocanonical books fall in it).

Distributions are compared with the Jensen-Shannon distance (JSD; symmetric, bounded [0, 1], 0 = identical distributions), against the Section 4.3 baseline of 0.567 computed without controlling for genre, plus a chi-square test of independence between topic and category restricted to each genre:

| Genre | Protocanonical books | Deuterocanonical books | Passages (proto / deutero) | Within-genre JSD | Baseline JSD | χ² test |
|---|---|---|---|---|---|---|
| Historical Narrative | 12 (Joshua–Esther) | 4 (Tobit, Judith, 1–2 Maccabees) | 1,372 / 374 | **0.636** | 0.567 | χ²=746.1, df=11, p=7×10⁻¹⁵³ |
| Wisdom/Poetic | 5 (Job–Song of Solomon) | 2 (Wisdom, Sirach) | 581 / 277 | **0.296** | 0.567 | χ²=79.8, df=9, p=1.8×10⁻¹³ |
| Prophetic | 17 (Isaiah–Malachi) | 1 (Baruch) | 1,146 / 35 | 0.476 | 0.567 | χ²=84.7, df=10, p=5.9×10⁻¹⁴ |

As a calibration check on what these JSD values mean in scale, the JSD *between* genres among protocanonical passages only (a case with no canon-status difference present at all, so any distance is a pure genre effect) ranges from 0.469 (Law vs. Historical Narrative) to 0.806 (Historical Narrative vs. Wisdom/Poetic).

Historical Narrative — the genre holding 4 of the 7 deuterocanonical books and 374 of the 686 deuterocanonical passages, the largest share by far — shows a within-genre JSD (0.636) *larger* than the unconditioned baseline (0.567), not smaller. Wisdom/Poetic shows a within-genre JSD (0.296) roughly half the baseline. Prophetic, resting on a single deuterocanonical book and 35 passages, falls in between (0.476) but is underpowered to draw a conclusion from. All three within-genre associations remain statistically significant at p ≪ 0.001. (`notebooks/03_topic_modeling.ipynb`, `outputs/figures/topic_distribution_by_genre.png`.)

### 4.5 Topic-Count Tuning and Stability

`N_TOPICS=12` (Section 3.5) was a starting point, not a tuned value. Three checks were run: two standard model-selection diagnostics (held-out perplexity and UMass topic coherence [16] across a wide range of candidate topic counts), and — more directly relevant to this thesis's actual claim — whether the Historical Narrative genre-confound result (Section 4.4) holds up under different topic counts and random initializations, or is an artifact of the specific `K=12, random_state=42` used throughout. UMass coherence was implemented directly from the document-term matrix (co-document frequency of each topic's top-10 words) rather than via an external library, for the same avoid-heavy-dependencies reasoning as the LDA-over-BERTopic choice in Section 3.5.

**K sweep**, widened to K ∈ {4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28} (fit on an 80% training split, held-out perplexity and coherence scored there, then the same trained model applied to the full dataset to recheck the Historical Narrative finding):

| K | Held-out perplexity | UMass coherence | Baseline JSD | Historical Narrative JSD | Historical Narrative ≥ baseline? |
|---|---|---|---|---|---|
| 4 | **721.1** (best) | **−1.417** (best) | 0.181 | 0.145 | **No** |
| 6 | 743.4 | −1.464 | 0.335 | 0.349 | Yes |
| 8 | 774.6 | −1.580 | 0.407 | 0.478 | Yes |
| 10 | 797.0 | −1.582 | 0.510 | 0.543 | Yes |
| 12 | 810.2 | −1.655 | 0.551 | 0.610 | Yes |
| 14 | 855.5 | −1.710 | 0.474 | 0.479 | Yes |
| 16 | 876.4 | −1.752 | 0.476 | 0.454 | No (narrowly) |
| 18 | 910.6 | −1.835 | 0.520 | 0.524 | Yes |
| 20 | 944.3 | −1.879 | 0.538 | 0.607 | Yes |
| 24 | 998.0 | −1.882 | 0.509 | 0.545 | Yes |
| 28 | 1070.8 | −1.908 | 0.519 | 0.545 | Yes |

Both held-out perplexity and UMass coherence increase/worsen monotonically across the entire tested range — by either metric alone, K=4 is the "best" fit, and fit quality degrades steadily as K grows all the way to 28. But K=4 is exactly where the Historical Narrative finding fails, and fails worst: at four topics the model is too coarse to represent the thematic distinction this analysis depends on, and both JSD values collapse to a fraction of their size at every other K tested. The finding holds at 9 of the 11 K values tested — everything from K=6 through K=28 except K=16, whose shortfall is narrow (0.454 vs. 0.476) rather than a reversal.

**Seed sweep** (K=12, full data, three different `random_state` values):

| `random_state` | Baseline JSD | Historical Narrative JSD | Historical Narrative ≥ baseline? |
|---|---|---|---|
| 0 | 0.502 | 0.636 | Yes |
| 42 | 0.567 | 0.636 | Yes |
| 99 | 0.506 | 0.546 | Yes |

At the topic count used throughout this thesis, the finding holds across every seed tested.

**Decision: keep `N_TOPICS=12`.** It is not perplexity- or coherence-optimal in the tested range — nothing tested is, except the substantively-failing K=4 — but it sits well inside the broad K=6–28 range (one isolated exception, K=16) where the genre-confound finding consistently replicates, it is where this notebook's topic-word interpretations (Section 4.3) were actually done, and it is robust to random seed. Optimizing K purely against perplexity or coherence here would mean discarding the one property those metrics don't measure and this analysis needs most: enough topic resolution to detect the effect being tested for. This is a known, general tension in topic-model selection — statistical fit metrics reward whatever compresses word co-occurrence patterns best, which is not the same target as "enough resolution for a specific downstream comparison" — not a problem specific to this corpus.

## 5. Discussion

### 5.1 What the Topic Result Does and Doesn't Show

The topic distribution difference (Section 4.3) is a genuine, non-trivial finding: deuterocanonical passages are not topically indistinguishable from protocanonical ones under this model. It also survives the genre-confound test (Section 4.4) — but not uniformly, and the way it survives is more informative than a simple pass/fail.

For Historical Narrative, which carries most of the deuterocanonical corpus (4 of 7 books, 374 of 686 passages), genre does *not* explain the effect away: the within-genre topic gap is larger than the unconditioned baseline, and the association between topic and canon status is overwhelming (p ≈ 7×10⁻¹⁵³). Deuterocanonical historical narrative (Tobit, Judith, 1–2 Maccabees) concentrates nearly half its passages in a single topic centered on collective political actors and Jerusalem ("jews," "people," "city," "jerusalem"), while protocanonical historical narrative (Joshua through Esther) spreads more evenly across several topics centered on named kings and royal succession. Both are "historical narrative" by genre, but they are not the same kind of historical narrative — this is the clearest evidence in the whole analysis that deuterocanonical *content*, not just deuterocanonical genre-membership, is driving the original result.

For Wisdom/Poetic, genre explains a real share of the effect: the within-genre gap roughly halves relative to baseline, and both protocanonical and deuterocanonical wisdom books share the same dominant topic (general moral exhortation) rather than diverging into different topics the way the two historical-narrative groups do. Wisdom and Sirach simply concentrate in that shared topic more heavily than Job, Psalms, Proverbs, Ecclesiastes, and Song of Solomon do — a difference of degree, consistent with Wisdom and Sirach being more narrowly wisdom-genre works than, say, Psalms (which includes lament, praise, and royal material well outside pure moral exhortation) or Song of Solomon (love poetry). The calibration check (cross-genre JSD among protocanonical passages alone, 0.47–0.81) puts this in context: canon status is not a negligible signal relative to genre even in Wisdom/Poetic, where genre explains the most.

The Prophetic result (Baruch alone) is inconclusive by design — a single deuterocanonical book and 35 passages cannot support a confident claim either way, and this thesis does not attempt to make one.

Net effect: the genre-confound hypothesis, stated as "the Section 4.3 result is just a genre artifact," is not supported. The more accurate statement is that genre and canon status both carry real signal, in different proportions depending on which genre — and for the genre holding most of the deuterocanonical text, canon status carries more, not less, once genre is controlled for.

### 5.2 The Translation Lineage Corrections, Read Together

The two corrected edges in Section 4.2 share a pattern worth naming directly: both were plausible-sounding claims that happened to be wrong once checked against sources, not merely unsourced guesses that turned out to be roughly right. The Septuagint-from-Masoretic-Text edge is wrong because it assumes "the Hebrew Bible" was a single fixed text that different traditions each took a copy of at different points in history, when in fact multiple Hebrew textual traditions coexisted well into the Second Temple period, and which one a given translator worked from was a real, consequential choice — the same choice Jerome explicitly defended in his *hebraica veritas* argument against contemporaries who trusted the Septuagint instead. The Luther-to-KJV edge is wrong because it substitutes the most *famous* prior Reformation translation for the actual documented one (the English Tyndale/Bishops'-Bible tradition), which is a natural error to make without checking primary sources. Both errors are the kind that intuition produces and citation-checking catches — which is the methodological point of doing the sourcing work at all (Section 3.6), not a criticism specific to this project's earlier draft.

### 5.3 Descriptive Framing, Revisited

Section 1.3 commits this project to descriptive rather than evaluative claims. The results in Section 4 hold to that: nothing here argues that the Protestant, Catholic, or Orthodox canon is theologically correct, or that deuterocanonical books are more or less inspired, authoritative, or valuable than protocanonical ones. What the topic-modeling result shows is that *content* differs measurably between the two categories — which is a precondition for, but does not settle, the theological question of *why* the traditions draw the canon boundary where they do. The translation lineage graph is similarly descriptive: it shows what fed into what, not which resulting text is more faithful to an original.

### 5.4 Limitations and Open Items

Being explicit about what is not yet done, rather than presenting a more finished picture than the pipeline actually supports:

- **The topic count (12) is not perplexity- or coherence-optimal.** Section 4.5's widened sweep (K ∈ {4, 6, ..., 28}) shows both metrics monotonically favoring K=4, the smallest value tested. K=12 was kept because switching to the metric-optimal K=4 would discard the genre-confound finding itself (K=4 is exactly where it fails), and because the more directly relevant check — whether the finding holds up — passes at K=12 across every random seed tested and 9 of 11 topic counts tested (Section 4.5). This is a real, general tension in topic-model selection (statistical fit vs. downstream task resolution), not something resolved by widening the grid further.
- **The K sweep has not been repeated with a proper external coherence library (e.g. gensim's `CoherenceModel`) as a cross-check on the self-implemented UMass coherence**, though the self-implementation was validated against a synthetic sanity check (co-occurring vs. non-co-occurring word pairs) before use.
- **LDA vs. embedding-based topic modeling.** Bag-of-words LDA was chosen for practical reasons (Section 3.5), not because it is expected to be the best-performing method. An embedding-based approach (e.g. BERTopic) might separate deuterocanonical wisdom literature from deuterocanonical narrative more cleanly than this single-pass LDA does, since it was not run.
- **The Prophetic genre-confound result (Section 4.4) is underpowered.** One deuterocanonical book (Baruch) and 35 passages is too small a sample to draw a conclusion from; would need a second deuterocanonical prophetic-genre book, and none exists in this canon list.
- **The Orthodox canon list is one baseline, not a jurisdictional standard.** Section 3.1 notes this; the 77-book list used throughout does not represent Slavonic, Georgian, or Ethiopian Orthodox canons, which include additional books not modeled here.
- **Related Work (Section 2) needs specific citations**, not category descriptions, before this is submission-ready.

## 6. Conclusion and Future Work

This project set out to test whether standard computational text-analysis methods — set comparison, graph construction, topic modeling — could make canon divergence across the Protestant, Catholic, and Orthodox biblical traditions visible as data, using the same tools applicable to any other corpus-comparison problem, without adjudicating which tradition's canon is theologically correct. The canon overlap analysis (Section 4.1) reproduces the documented canon differences exactly, including the specific case-study pair (2 Maccabees, 2 Kings) that motivated the project. The translation lineage graph (Section 4.2) demonstrates that even a small, deliberately scoped historical-lineage claim benefits materially from source-checking — two of eight original edges were substantively wrong, not merely unsourced. The topic-modeling result (Section 4.3) finds a real, interpretable thematic difference between deuterocanonical and protocanonical passages within a single consistent translation, and that difference holds up — for the genre carrying most of the deuterocanonical corpus, it strengthens — once tested directly against its most obvious alternative explanation, a pure genre confound (Section 4.4).

Immediate next steps, in rough priority order: (1) resources permitting, run a BERTopic comparison now that there is a genre-controlled, seed-and-K-stable result worth checking against a different modeling approach, and cross-check the self-implemented UMass coherence against an external library; (2) find a second deuterocanonical prophetic-genre text or otherwise strengthen the underpowered Prophetic/Baruch comparison in Section 4.4; (3) extend the corpus construction and topic-modeling pipeline to the Orthodox-only books (1 Esdras, 3 Maccabees, Prayer of Manasseh, Psalm 151), which was deliberately out of scope here because it would mix Septuagint- and KJV-sourced text and reintroduce the translation-artifact risk Section 3.3 was designed to avoid for the Catholic-corpus analysis.

## References

[1] `data/metadata/canon_lists.json`, `data/metadata/canon_lists.md` — this project's structured canon definitions.
[2] `src/align_corpus.py`, `src/graph_builder.py`, `src/build_processed_corpus.py` — this project's analysis pipeline.
[3] `docs/historical_notes.md` — this project's cited research journal; primary source for all historical claims cross-referenced by number below.
[4] Council of Hippo, Canon 36 (393 A.D.), confirmed by the Third Council of Carthage (397 A.D.).
[5] Council of Trent, "Decree Concerning the Canonical Scriptures," Fourth Session, Apr. 8, 1546.
[6] M. Luther, "Preface to the Apocrypha," in *Biblia: das ist, die gantze Heilige Schrifft Deudsch*, Wittenberg, 1534.
[7] 2 Kings 13:20–21, King James Version; 2 Maccabees 12:38–46, New American Bible Revised Edition.
[8] Dating of the Septuagint's translation (Pentateuch c. 250 BC per the *Letter of Aristeas* tradition; remaining books completed by c. 132 BC per the prologue to Sirach) — see the Septuagint entry in standard biblical-studies reference works.
[9] E. Tov's classification of Dead Sea Scroll biblical manuscripts identifies a distinct pre-Septuagint Hebrew text-type (e.g. 4QJer-b, 4QJer-d, 4QSam-a) alongside proto-Masoretic manuscripts, confirming textual plurality in the Hebrew tradition the Septuagint translators drew from — summarized in scroll-classification literature following Tov's *Textual Criticism of the Hebrew Bible*.
[10] "Rules to Be Observed in the Translation of the Bible" (1604), the fifteen instructions issued to the King James translators.
[11] J. Nielson and R. Skousen, "How Much of the King James Bible Is William Tyndale's? An Estimation Based on Sampling," *Reformation* 3 (1998): 49–74.
[12] Historical accounts of the 1534 Luther Bible's collaborative translation team (Melanchthon, Cruciger, Bugenhagen, Jonas, Rörer et al.) and each member's role.
[13] Erasmus, *Novum Instrumentum omne* (1516), 2nd ed. 1519 — the Greek New Testament edition Luther's translation team used as a primary New Testament source.
[14] Jerome's prefaces to his Vulgate translations (e.g. the preface to Judith) and standard Vulgate reference histories, on which books he retranslated from Hebrew/Aramaic versus retained from the Vetus Latina.
[15] D. M. Blei, A. Y. Ng, and M. I. Jordan, "Latent Dirichlet Allocation," *Journal of Machine Learning Research*, vol. 3, pp. 993–1022, 2003.
[16] D. Mimno, H. M. Wallach, E. Talley, M. Leenders, and A. McCallum, "Optimizing Semantic Coherence in Topic Models," in *Proceedings of the 2011 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2011, pp. 262–272.

## Appendix: Reproducibility

All results in Section 4 are reproducible from a clean checkout: `python src/fetch_kjv.py && python src/fetch_douay_rheims.py && python src/fetch_septuagint.py` populates `data/raw/`; `python src/build_processed_corpus.py` populates `data/processed/`; `jupyter nbconvert --to notebook --execute notebooks/0{1,2,3,4}_*.ipynb` regenerates every figure cited above. `data/raw/` and `data/processed/` are gitignored by design (fully regenerable, kept out of version control to keep the repository light) — see `context/PROJECT_MAP.md` for the full pipeline map (personal navigation notes, not part of this thesis).
