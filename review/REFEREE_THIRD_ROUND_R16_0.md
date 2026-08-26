# Referee Report — Third Round (Readability and Publishability)

**Manuscript:** *Public CAD Is Not Operational Ground Truth: What Hurricane Ida Reveals About Measuring Police Responsiveness*
**Version reviewed:** Paper R16.0 / Scientific Results R15.1, branch `review/r16.0`, commit `3b8fbac` (25 August 2026), repository `yuwen3756-hue/public-cad-measurement-police-responsiveness-hurricane-ida`.
**Brief for this round:** writing style, structure, ease of understanding, whether the paper works as a standalone document a supervisor can absorb quickly, and whether the empirical result is publishable.
**Materials examined:** main paper (11 pp.), empirical supplement (13 pp.), one-page status note, `RESPONSE_TO_ASSESSMENTS.md`, the readability review materials in `review/`, and all `source/r15_*` / `r15_1_*` evidence files. `scripts/verify_release.py` returns `RELEASE_VERIFICATION_PASS` on a fresh clone. `git diff` of `reproduction/` against R15.0 (`5e2af0f`) is empty; every headline number in the R16 text matches the packaged CSV/JSON objects I checked in the previous two rounds. No scientific content has changed, so this report is about presentation and publishability only.

**Recommendation:** **Accept with minor corrections.** The rewrite achieves what the readability review asked for. A supervisor can now read the main paper in one sitting, state its result in a sentence, and see exactly where its claims stop. There are four small textual defects (one of them a broken paragraph in the supplement) and a handful of sentence-level suggestions. None require re-analysis.

---

## 1. Does the paper now read as a standalone paper? Yes.

The key test for a document like this is whether a reader who opens page 1 with no prior context can reconstruct the argument without the supplement, the response memo, or the reviewer history. R16.0 passes that test. Specifically:

**Structure.** The sequence *question → data and four configurations → July break → daily Ida path → comparison statistic → interpretation → implications → limitations* is the right order and is the order in which a reader forms beliefs. The estimator now arrives after the reader has already seen the phenomenon in two figures, so the statistic reads as "putting a number on what you just saw" rather than as an abstraction to be trusted. That was the central structural problem of R13–R15 and it is fixed.

**Hierarchy.** There is now one primary result (53.2 pp, larger than all 151 post-change ordinary weeks), one clearly subordinate secondary result (standardized, 50.7 pp, incomplete support), and everything else is explicitly labelled as robustness and moved to the supplement. The reader is never asked to hold two co-equal headline numbers. The one-sentence version — "the public file changes on 28 July 2021; five weeks later Ida produces a second, temporary change larger than any ordinary week since; the file does not reveal why" — is stated in the abstract, in §1, in the status note, and again in the conclusion, in the same words. That repetition is the good kind.

**Language.** The internal notation (`J01`, `M_max`, `U_direct`, "support-independent universe", "stage-era") is gone from the main prose. "Arrival only", "dispatch only", "both fields", and "largest percentage-point change" are used consistently. Table 1 fixes the vocabulary once and the paper never departs from it. The one appearance of "stage-era" (§6.2) is immediately glossed. A criminologist, an economist, or a police data analyst can all read this without translation.

**Length and density.** Main paper 11 pages, abstract 182 words, two figures, five tables, one equation. This is the correct size for the result. The abstract still carries eleven numbers, but they are now the eleven a reader would want, in the order they will meet them in the text, and the abstract has a stated conclusion in its last sentence.

**Boundaries.** The paper's refusal to overclaim is now a strength rather than an obstacle. Each result section ends with one short paragraph saying what the result does not show, in plain terms. The "Safe interpretation" framing in Table 1 and the "What the public file supports / Additional evidence needed" framing in Table 5 turn the limitations into something usable.

**Standalone check.** I read the main PDF without the supplement and found no claim that depends on the supplement to be understood. The supplement is referenced for detail, never for meaning. That is the right relationship.

---

## 2. Required corrections (all textual)

### 2.1 Broken paragraph in the supplement (§Ida path, standardized design)

The paragraph introducing the standardized contrast reads:

> "…let $w^B_{tx}$ be the baseline weight over common support. Its contrast is
>
> For half-day bin $t$, state $j\in\{J_{01},J_{10},J_{11}\}$, and common stratum $x$, let $p^E_{tjx}$ … The standardized contrast is [equation]"

The first sentence ends in "Its contrast is" with no equation, and the entire definition is then repeated. This is a copy-paste remnant of the reorganization. Delete the first of the two paragraphs. (Supplement source line 131.)

### 2.2 "Continues toward its pre-event range" is not what Figure 2 shows

§5 says the arrival-only share "falls to 16.4 percent on 2 September and continues toward its pre-event range over the following days." The packaged daily series (`r15_1_ida_time_path.csv`) shows a second, smaller spike: 20.1 percent on 9 September and **34.7 percent on 10 September**, with dispatch coverage falling to 58.2 percent that day, before the series returns to the 7–10 percent range on 11–12 September. This is visible in Figure 2 and a careful reader will notice that the text and the figure disagree. Replace with something like: "It falls to 16.4 percent on 2 September, returns to the pre-event range by 5 September, and shows one further one-day excursion to 34.7 percent on 10 September before settling." The secondary spike does not affect the comparison statistic (the 10 September date is outside the event window) but it should not be written out of the description.

### 2.3 The 29 August arrival-field dip should be mentioned once

Also in Figure 2: on landfall day (29 August) the *valid-arrival* share drops to 43.8 percent from a pre-event range of 74–84 percent, while dispatch coverage is still 72.9 percent. This is the other feature a reader will see in the figure, and it is the opposite pattern from 31 August – 1 September (arrival present, dispatch absent). One sentence in §5 noting that "the first day of the event is marked by missing arrival fields; the third and fourth days by missing dispatch fields" would make the figure fully described and is itself informative about how the record degraded.

### 2.4 "Three independent public configurations"

§6.1: "the change in the three independent public configurations: dispatch only, arrival only, and both fields present." The four configurations are not independent; three of them are *sufficient* because the four shares sum to one. Say "three of the four configurations (the fourth is determined by the other three)".

---

## 3. Suggested sentence-level improvements (optional)

1. **Table 1, "Safe interpretation" column.** Three of the four entries restate the row labels ("A dispatch field is available; a valid arrival field is not"). The column earns its space only in the "Arrival only" row and the footnote. Consider replacing the column with a single footnote, or retitling it "What it does *not* mean" and filling it accordingly, which is what the reader actually needs.

2. **§4, paragraph beginning "The simultaneous movement…"** is the best paragraph in the paper and could carry one more sentence. The phrase "the discrepancy lies somewhere between activity and released representation" is exactly right; the paper could add that for the officer stream specifically, an operational reading is not available (officers did not stop attending their own self-initiated events), so the change is in production of the record. The authors chose in R15/R16 to keep the hedge; I noted in round two that the evidence permits a stronger sentence. I do not insist, but the supervisor will likely ask the same question, and it is better answered in the text.

3. **§9 Limitations, "Reference windows overlap."** The supplement now contains the non-overlapping-window sensitivity I requested (Ida 1/77 and 1/76 in the two alternating phases; largest retained reference 0.310). This is the best answer to the overlap objection and the main paper does not mention it. Add one clause: "Reference windows overlap; using every second window removes adjacent overlap and leaves the ranking unchanged (supplement §Bootstrap)."

4. **Keywords.** "Partial identification" is still listed. In R16 the main paper uses that literature as a framing device (§2) but does not compute a bound. Either keep it (defensible) or replace it with "administrative data quality", which describes what the paper does.

5. **Title.** The new subtitle *What Hurricane Ida Reveals About Measuring Police Responsiveness* is better than the R15 subtitle. Minor: "Reveals About" slightly oversells; Ida is a stress test, not a revelation. "A Hurricane Ida Stress Test of Public Dispatch Data" would be more exact, but this is taste.

6. **§7.3 last paragraph.** "No public versioned changelog or internal-to-public reconciliation was available for this analysis, and no agency confirmation of the July change was obtained." This is honest and important. Consider stating the one concrete next step explicitly here (a public-records request to OPCD for CAD export configuration and change history covering July 2021), because a supervisor reading this will immediately ask "so what would resolve it?" and the answer is short.

7. **Supplement, Cristobal.** The 7 and 14 June 2020 windows are now labelled, with a citation to the NHC report, and correctly flagged as a post-hoc label that does not alter membership. Good. The sentence "Their large pre-break full-count movements occur through the available $J_{11}/J_{10}$ states, not through $J_{01}$" could also appear in the main paper §6.2 as a half-sentence, since it is the one piece of evidence that field reconfiguration under stress predates the July regime.

---

## 4. Consistency checks performed

| Item | Main paper | Supplement / data | Status |
|---|---|---|---|
| Ida full-count statistic | 0.532 / 53.2 pp | 0.5320 (`r15_aggregate_diagnostics.json`) | Match |
| Post-change references | 151; largest 0.310 | 151; 0.3098 | Match |
| Standardized statistic | 0.507; 153 refs; largest 0.328 | 0.5072; rank 1/154; 0.3282 | Match |
| Coverage | 86.1 / 77.0 % | 0.861 / 0.770 | Match |
| Bootstrap interval | [0.475, 0.601] | [0.4754, 0.6015] | Match |
| Daily arrival-only shares | 13.2 / 22.9 / 43.4 / 49.3 / 16.4 | `r15_1_ida_time_path.csv` | Match |
| Daily dispatch shares | 47.3 / 40.9 | same file | Match |
| 27–29 July transition | 731/620/666; 0/34/69; 90.0/82.1/76.6; 479/575/504; 100/40.0/1.0 | `r15_raw_july_25_31_audit.csv` | Match |
| Annual dispatch shares | 65.4 / 66.0 / 66.8; all-row 42.7 / 41.8 / 41.9 | `r15_current_denominator_audit.csv` | Match |
| Rank denominators | "larger than all 151" used consistently | Claim index: 1/152 (post-change), 1/151 (stage-era) | Consistent; the round-two inconsistency is resolved |
| Post-hoc labelling of post-change set | Stated in §6.1 and §9 | Stated | Resolved |
| Citations | 27 keys | all present in `references_r16_0.bib` | OK |
| Page counts | main 11, supp 13, combined 24, note 1, archive 30 | as stated in README | OK |
| Locked artifacts | — | `git diff 5e2af0f HEAD -- reproduction/` empty | Unchanged |

---

## 5. Is the empirical result publishable?

**Yes, as a measurement paper, and the honest framing the authors have adopted is what makes it so.** My assessment by type of outlet:

**What the paper establishes and why it is worth publishing.** It documents, from official public bytes with a reproducible pipeline, (i) a dated discontinuity in a widely used public dataset that no prior user of the New Orleans CAD file appears to have reported, (ii) a stress-period reconfiguration of the released fields that is the largest in the post-break period by a factor of 1.7 on the simplest statistic, with sampling intervals that do not approach any reference, and (iii) the practical consequence that any response-time or DV-response study using this file across July 2021 — or pooling initiation streams in any year — is measuring a changing object. Point (iii) is the publishable contribution: it is a concrete, checkable warning to a real research community about a real dataset, with the check itself supplied.

**Where it is publishable as a standalone.**
- *Criminology and policing journals* (e.g., *Journal of Quantitative Criminology* as a research note, *Policing: A Journal of Policy and Practice*, *Crime Science*, *Police Practice and Research*). These outlets publish data-quality and measurement papers about CAD and RMS data, and the paper's target audience — people who compute response times from open data — reads them. This is the natural home. I would expect a favourable review at this length.
- *Data and official-statistics outlets* (*Data & Policy*, *Journal of Official Statistics*, *Journal of Economic and Social Measurement*). The reproducibility package and the interpretive checklist in the supplement are exactly what these venues value.
- *A general open-access outlet* (*PLOS ONE*, *Scientific Reports*) would accept it on the strength of the reproducibility alone, but the audience fit is weaker.

**Where it is not sufficient on its own.** A general economics field journal (*Journal of Public Economics*, *Journal of Urban Economics*, *JLE*) or a top criminology journal (*Criminology*) would want either the mechanism identified — an OPCD records request answering what changed on 28 July 2021 — or a substantive downstream result (the DV response-time analysis this project was built for) that the measurement work makes credible. Single-city, descriptive, no outcome, and a mechanism explicitly left open will not clear that bar as a standalone. The authors already know this; the paper's Table 5 and §8 are in effect the design document for that next paper.

**As a dissertation chapter.** This is a strong data/methods chapter. It demonstrates command of the source, reproducibility discipline that is well beyond the norm, and a correct instinct for the difference between what a record shows and what it means. A committee will accept it as a chapter in its own right and will read the DV chapter that follows with more confidence because of it. The one question a committee will put is the one in §3.2 above — why not say plainly that the officer-stream change is a record-production change — and the candidate should have that answer ready even if the text keeps the hedge.

**What would raise the ceiling most, in order of cost:**
1. One public-records request to OPCD (cheap; could resolve §7.3 entirely).
2. The call-type decomposition suggested in round two (a day's work from the packaged tally; turns "reconfiguration" into "ordinary citizen calls were released in the officer-initiated form").
3. A second city with an open CAD file to show the pattern is not idiosyncratic to New Orleans (moderate; converts a case study into a general finding about open CAD exports).

---

## 6. Summary for the supervisor

R16.0 is the version to read. It is 11 pages, has one result, states it in plain language, shows the phenomenon before the statistic, and draws its interpretive boundary explicitly. The numbers have not changed since R15 and all of them check against the packaged data. Four small text corrections are needed (a duplicated paragraph in the supplement; two places where the Ida-path description does not match its own figure; the word "independent"). After those, the paper is ready to be circulated and, in my judgement, publishable as a measurement paper in a criminology, policing, or data-policy journal. It becomes a stronger paper still if the July 2021 mechanism can be pinned down through a records request, and it is the right foundation for the reported-DV analysis that follows.
