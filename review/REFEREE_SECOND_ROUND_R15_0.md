# Referee Report — Second Round

**Manuscript:** *Public CAD Is Not Operational Ground Truth: Regime Change, Hurricane Ida, and the Measurement of Police Responsiveness*
**Version reviewed:** Paper R15.0 / Results R15, commit `5e2af0f` (25 August 2026). Previous report covered R13.0 (`b867d242`); an intermediate R14.0 was reviewed separately and that review is preserved in `review/`.
**Materials examined:** main paper (12 pp.), empirical supplement (12 pp.), status note, `RESPONSE_TO_ASSESSMENTS.md`, all `source/r15_*` evidence files, and the reproduction snapshot. I re-derived the headline numbers from the packaged tally and checked that the locked M7B/M7D-E/M8P artifacts differ from R13 only in line endings (`git diff -w --ignore-cr-at-eol`: 0 insertions, 0 deletions) — no locked result was silently changed.

**Recommendation:** **Minor revision.** The paper is now a credible, readable measurement paper. What remains is a handful of consistency fixes, one labelling correction, and two places where the authors are more cautious than their own evidence permits.

---

## 1. Status of the first-round comments

| First-round comment | R15 status | Verified |
|---|---|---|
| 1. July 2021 regime change omitted | **Closed.** Now the first result; raw-file audit added (Table 1, Fig. 1); 419,840 pre-break records with zero $J_{01}$ confirmed. | Yes — matches my tally recomputation exactly. |
| 2. Ida fails its own eligibility gate | **Closed.** Coverage 0.861 / 0.770 stated in the abstract; full-count estimator added as the safeguard. | Yes. |
| 3. Other disasters excluded from reference | **Closed.** Laura 0.084, Zeta 0.129, freeze 0.113, post-Ida 0.478, Francine 0.110 reported as labelled episodes. | Yes — but see §2.3 below on an *unlabelled* emergency still inside the reference set. |
| 4. "All-call" denominator; officer stream | **Closed.** Non-officer denominator stated; officer stream shown separately (99% $J_{01}$ after break). | Yes. |
| 5. LP apparatus; unreported secondaries | **Closed.** $M_{\max}$ is headline; LP is robustness; all eight prespecified secondaries reported including the unfavourable ones ($Q$ 100/154, $\sigma_3$ 11/154). | Yes — ranks match `r15_secondary_statistic_ranks.csv`. |
| 6. No sampling uncertainty | **Closed.** Within-stratum multinomial bootstrap; cell intervals; 4,000-draw rank distribution. | Yes; limitations correctly stated. |
| 7. Composition "theorem" | **Closed.** Now one paragraph of accounting. | Yes. |
| 8. DV section without DV data | **Closed** (compressed to one page). | Yes. |
| 9. Captions / thresholds | **Closed.** 9/8/9 counts; interval widths disclosed. | Yes. |
| 10. Beland (2026) anchor; BELAND-PLUS naming | **Closed.** No citation to the unpublished presentation; "BELAND-PLUS" no longer appears in the main text (only in style-file colour names). | Yes. |

The restructuring follows the suggested outline closely, and the new raw-file audit adds something I had not asked for and which materially strengthens the paper: the officer-initiated stream loses its dispatch field on the *same day* (100% → 40.0% → 1.0% over 27–29 July). That coordinated shift is the single most important new fact in R15.

---

## 2. Remaining issues

### 2.1 Rank denominators are inconsistent across documents (must fix)

The full-count post-change comparison is reported three different ways:

- Main paper §5.1 and abstract: "rank 1 among **151** support-independent post-change references."
- Supplement claim index (Table 12): "0.5320; rank **1/151**."
- Supplement Table 12 next row and status note: "rank **1/152** including Ida."
- Main paper §5.1: "rank 1 among **150** comparable members of the stage-era set."

From `r15_raw_window_scores.csv`: 151 post-change references (both sides after 28 July, not context-excluded, excluding Ida) → rank 1/152 *including* Ida; 150 stage-era windows carry a full-count score (three stage-era members — 11, 18, 25 July and 1 August — have baselines before 28 July, and five post-change windows are not stage-era members). All three numbers are correct; they are simply used interchangeably. Adopt one convention ("rank 1 of $R+1$ including Ida", as in Table 3) and apply it everywhere.

### 2.2 The post-change universe is post hoc and should be labelled as such

§4 states that "the three reference universes, eligibility rules, and context exclusions were fixed before the reference-window outcomes were inspected." The "genuinely post-change" universe (both sides after 28 July) is not one of those three; it was constructed in response to the first-round review, after the July break was identified. That is the right design, but the text currently lets it inherit the prespecification language. One sentence: "This universe was defined after the July break was identified and is therefore a post-hoc comparison; the stage-era set is the prespecified one."

### 2.3 An unlabelled emergency sits inside the "ordinary-week" reference set

In `r15_raw_window_scores.csv`, the two largest full-count reference values overall are **2020-06-07 (0.333)** and **2020-06-14 (0.340)** — larger than any post-change reference (max 0.310). Tropical Storm Cristobal made Louisiana landfall on 7 June 2020, and the first week of June 2020 also had the protest curfews. Neither week is on the frozen exclusion list; both are ordinary members of the full-qualified set (their standardized $M_{\max}$ are 0.122 and 0.135, ranks well below the top).

Two consequences. First, the exclusion list was incomplete, which should be acknowledged. Second — and this is favourable to the paper — a tropical storm in the *pre-$J_{01}$* regime still produced the largest full-count field reconfiguration in that regime, through $J_{11}$/$J_{10}$ movement rather than $J_{01}$. That is direct support for "stress reconfigures the public record even when the available states differ." Label these two windows in Table 8 (excluded episodes) or in a footnote, and note that they were not prespecified exclusions.

### 2.4 Serial dependence of reference windows is stronger than the limitations paragraph suggests

Each window's baseline is the preceding week, so window $k$'s event period is window $k+1$'s baseline. A single disturbed week therefore generates *two* large contrasts of opposite sign — the post-Ida week (0.478) is the clearest example, and 2020-06-07 / 06-14 is another. The effective number of independent references is well below 151, and the "rank 1 in 4,000 of 4,000 draws" statement is conditional on this dependence. A cheap sensitivity: rerank against every second window (non-overlapping baselines). The limitations paragraph says "does not capture temporal dependence"; it should say what that dependence is and report the non-overlapping rank.

### 2.5 The authors under-claim on the officer stream

§5.4 and the supplement say the joint change is "consistent with a new public-recording convention linked to initiation status" and that the file "does not reveal whether records were reclassified, different events were retained, or one timestamp was omitted in export." For the *officer-initiated* stream this hedging is stronger than the evidence requires. Officer-initiated items are, by the dictionary's own definition, generated by the officer in the field; a dispatch timestamp going from present on 479/479 records on 27 July to absent on 499/504 on 29 July, while arrival stays at 100%, cannot be an operational change — officers did not stop being present at their own self-initiated events. For that stream the paper can say plainly: the change is in record production or export. The non-officer stream then inherits the *same convention* on the same day. That is a legitimately stronger sentence than the paper currently allows itself, and it is the sentence the professor will want.

### 2.6 A call-type localization would sharpen the Ida result (suggested, not required)

The tally supports one more decomposition the paper does not report. Among non-officer records with an arrival field, pre-Ida $J_{01}$ (1–28 August) is concentrated in a few `initialtype` codes: 22A and 22B (≈50% $J_{01}$ within type; 28% of all $J_{01}$), with the high-volume citizen types near 10% (code 21) or below 5% (codes 107, 103). During B6–B7 (31 Aug – 1 Sep), $J_{01}$ spreads to the ordinary citizen types: code 21 rises to 40%, 107 to 41%, 62A/62B to 37–49%, 103 to 59%. In plain terms, during the outage *ordinary citizen calls* were recorded in the form that, in normal weeks, only a handful of call types (and the officer stream) take. A short table with decoded type labels would turn "reconfiguration" into something a police manager recognizes. The type codes need decoding from the official dictionary before publication; I have not done that.

### 2.7 Abstract density

The abstract carries thirteen numbers, two dataset counts, and three percentages to one decimal. Half of them belong in §5. An abstract for this paper needs: the break date, the Ida magnitude and rank, the coverage caveat, and the one-line conclusion.

### 2.8 Package note (minor)

`scripts/verify_release.py` fails on my clone with a manifest hash mismatch on a JSON file under `reproduction/…/webai_context_packs/`. Cause: my clone was created at `b867d242` (before `.gitattributes` existed) with `core.autocrlf=true`, so the file was checked out CRLF and the later `* -text` rule did not renormalize it. The LF-normalized hash matches the manifest. A fresh clone at R15 should pass; the reproduction manual might add one line telling Windows users to clone fresh or set `core.autocrlf=false`. I did not rerun the LP replication or the Lean build.

---

## 3. What the paper now establishes, in the authors' own terms

1. A discontinuity in the public CAD export on 28 July 2021, present in official source bytes, affecting both initiation streams on the same day — for the officer stream, unambiguously a record-production change.
2. Five weeks later, a two-day reconfiguration during Ida that is the largest in every same-regime comparison, by a wide margin, on the simplest statistic, with bootstrap intervals that do not approach any reference.
3. A comparable long-run series (non-officer dispatch completeness 90% in 2020 → 65–67% in 2024–26) that shows the July break was the beginning of a persistent drift, not a one-off.
4. Public institutional documents that exclude two named technology explanations without identifying the cause.

That is a complete, defensible measurement paper. The remaining evidence gap — what OPCD changed on 28 July 2021 — is stated honestly and is the right next request (a public-records request to OPCD for CAD export configuration or changelog history for July 2021 would be the natural step).

---

## Verification notes

- Locked artifacts: `git diff -w --ignore-cr-at-eol b867d242 HEAD -- reproduction/` shows zero content changes; R15 claims "no empirical result was recomputed" are consistent with that.
- Recomputed from `w2_period_tally.csv.gz`: pre-break $J_{01}$ count 0 of 419,840; Ida-week non-officer dispatch share 0.649; 2024 non-officer share 0.654; officer-stream 2022–24 dispatch share ≈1%. All match `r15_period_summary.csv` and `r15_annual_initiation_field_completeness.csv`.
- Secondary ranks, bootstrap endpoints, and excluded-episode values match the packaged CSVs and `r15_aggregate_diagnostics.json`.
- New citations (`OIPM2021`, `DataNOLA2021`, `OPCDCarbyne2022`, `NOLAOIGHexagon2024`) carry URLs and verification dates; the Carbyne page is noted as returning not-found on 25 August 2026, which should be preserved in the reference as an archived-snapshot pointer if one exists.
