# Referee Report

**Manuscript:** *Public CAD Is Not Operational Ground Truth: Hurricane Ida and the Measurement of Police Responsiveness*
**Version reviewed:** Paper R13.0 / Results R12, public package commit `b867d242`
**Materials examined:** main text (23 pp.), appendix (30 pp.), LaTeX sources, and the full `reproduction/repository_snapshot` tree, including the locked M7B / M7D-E / M8P artifacts and the aggregate tally `w2_period_tally.csv.gz`. All new numbers in this report were computed from files inside the package; no outside data were used.

**Recommendation:** **Major revision.**

---

## Summary assessment

The paper's core empirical fact is real, reproducible, and worth publishing: on 31 August – 1 September 2021, the share of New Orleans public CAD records that carry an arrival timestamp but no dispatch timestamp rose by roughly 30–50 percentage points relative to the preceding week, and the change occurred within recorded dispositions rather than through a change in disposition mix. The paper's broader thesis — that public CAD fields are outputs of a record-production process and cannot be read mechanically as operational events — is correct and policy-relevant.

However, the manuscript as it stands has three problems serious enough to require rethinking rather than patching:

1. **A regime change in the public data-production process, five weeks before Ida, is entirely absent from the paper.** The record state the paper builds its result on ("arrival present, dispatch absent") does not exist anywhere in the public data before 28 July 2021. This changes the meaning of the main result and the legitimacy of the reference class.
2. **The reference-class design cannot support the claim "reference-extreme" in the sense readers will take it.** Ida fails the paper's own eligibility gate for reference windows; all other disasters and holidays are excluded from the reference set; and roughly 80 of the 217 reference windows sit in a data regime where the Ida pattern is structurally impossible.
3. **The ratio of apparatus to finding is very high.** A constrained minimax LP over 333 million support triples, a 54-regime witness enumeration, and a Lean 4 formalization are deployed to establish something that the simplest possible statistic — the maximum absolute cell contrast — already establishes with wider separation. The DV "application" contains no DV data and consists of textbook partial-identification bounds.

A shorter paper built around the data-regime change, the Ida spike, and the 2025 field-completeness numbers would be more convincing and more memorable than the present one. Detailed comments follow.

---

## Major comments

### 1. An undisclosed change in the public record-production process on 28 July 2021 (must address)

Using the package's own `w2_period_tally.csv.gz`, restricted to the non-officer-initiated records that form the paper's denominator:

| Period | P(arrival field present) | P(dispatch field present) | P(J01 \| arrival present) |
|---|---|---|---|
| Jan 2020 – 27 Jul 2021, every single day | 0.73–0.85 | 0.86–0.93 | **exactly 0.000** |
| Week of 25–31 Jul 2021 | 0.785 | 0.836 | 0.055 (**first non-zero day: 28 Jul 2021**) |
| 1–28 Aug 2021 | ≈0.78 | ≈0.78 | 0.09–0.11 |
| **Ida week, 29 Aug – 4 Sep 2021** | **0.663** | **0.649** | **0.246** |
| 5–12 Sep 2021 | 0.76–0.82 | 0.75–0.81 | 0.08–0.15 |
| 2024 (annual) | ≈0.74 | ≈0.65 | ≈0.22 |
| 2025 (paper §7) | 0.837 | 0.418 | ≈0.50 |

Implications:

- The state $J_{01}$ is *structurally impossible* in the public file from January 2020 through 27 July 2021. Dispatch-field completeness steps down from ≈0.90 to ≈0.78 in the week of 28 July 2021 and then drifts to 0.42 by 2025. This time series is stronger evidence for the paper's title than the Ida episode itself, and it does not appear in the manuscript.
- Roughly 80 of the 217 "full qualified" reference windows (January 2020 – July 2021) sit in a regime where the Ida pattern cannot occur by construction. Ranking Ida against them and reporting "above all 217" mixes two data-production regimes. The by-year medians of the reference score drift accordingly (2020: 0.051; 2021: 0.054; 2022: 0.066; 2023: 0.065; 2024: 0.066; maxima 0.095 → 0.213).
- The "stage-era matched" reference set (start ≥ 2021-07-01, R = 153) was evidently designed with this in mind, but the text never says what "stage era" means or why the cutoff is 1 July 2021. Readers cannot evaluate it.
- Ida's own paired baseline week (22–26 August 2021) has P(J01 | A) = 0.085, already three times the summer 2021 mean of 0.029. The baseline is drawn from a regime that had changed four weeks earlier and had not settled.

**Requested changes.** (a) Add a subsection to §3 with a monthly or weekly 2020–2024 time series of P(D), P(A), and P(J01 | A), marking 28 July 2021 and Ida. (b) Make the stage-era-matched set the primary reference class; demote the full set to a sensitivity check. (c) Reframe the abstract and introduction around the pair of facts (regime change + Ida shock). (d) State whether the authors have asked the City / OPCD what changed in late July 2021 (CAD upgrade, export script, redaction policy). Even a "no response" is informative.

### 2. Ida does not meet the paper's own eligibility rule for reference windows

`M7B_PROSPECTIVE_REFERENCE_SPEC.json` defines eligibility as "symmetric five-day ≥ 100 records and **≥ 0.90 common-support coverage on both sides**." `M7B_REFERENCE_DOMAIN_AUDIT.csv` gives Ida's per-bin coverage as 0.75–0.93 on the event side and **0.51–0.85 on the reference side**; record-weighted, roughly 0.85 and 0.77. Ida would be excluded from its own reference set. The M7B notes acknowledge this ("per-bin coverage remains visible … not silently promoted into a new gate"); the paper does not.

The consequence is a comparability problem: Ida's standardized contrasts are computed on common support covering half to three-quarters of its records, while every reference window is computed on ≥ 90% support. Bin B3 has 206 event records across 27 strata; B2 has 335 reference records across 31 strata. Contrasts of ±0.4–0.5 are being computed from a few hundred records.

**Requested changes.** Report Ida's per-bin coverage and record counts in the main text. Then either lower the reference gate until Ida satisfies it and re-rank (reporting how many windows enter), or add an unstandardized comparison as a robustness check. Note that comment 5 shows the unstandardized maximum-cell statistic already gives rank 1, so this is likely to help the authors.

### 3. The reference class excludes every other disaster and holiday, so "reference-extreme" means "more extreme than ordinary weeks"

`frozen_context_exclusions` removes the weeks of Hurricane Laura (Aug 2020), Zeta (Oct 2020), the February 2021 freeze, Francine (Sep 2024), the week after Ida, and every Mardi Gras, Fourth of July, Thanksgiving, and Christmas. The one sensitivity analysis on this dimension (`exclude_adjacent_emergencies`, R = 154) removes *more* windows, not fewer.

What the design therefore shows is that a hurricane week is more unusual than a quiet week — which is close to true a priori. The question a reader wants answered is whether the Ida signature is *generic to emergency operations* or *specific to Ida*. Either answer is valuable: if Francine shows the same $J_{01}$ jump, the "measurement instability under stress" thesis generalizes; if not, Ida's specificity is established. The current design discards that information.

Because of comment 1, Laura, Zeta, and the freeze cannot show the Ida pattern (they are in the $J_{01} \equiv 0$ regime), which is itself a demonstration that "same estimator" does not mean "same object" across regimes. Francine (Sep 2024; P(J01 | A) ≈ 0.55–0.61, similar to its neighbouring weeks) is the only same-regime hurricane in the data.

**Requested changes.** Plot the excluded disaster and holiday windows as labelled points on Figure 2 (they need not enter the rank), and report their scores in the text. At minimum report Francine and the post-Ida week.

### 4. "All-call" is inaccurate: officer-initiated records (~40%) are excluded, and 99% of them are $J_{01}$

Ida's event-side count (3,878) equals the sum of `si == non_officer_self_initiated` in the tally; the 1,967 officer-initiated records in the Ida window are not in the denominator. The text says only "the frozen public-created-call universe." This contradicts the abstract's and §3.2's repeated "all reported calls."

More importantly for interpretation: after July 2021, officer-initiated records are **98.9–99.6% in state $J_{01}$** (arrival present, dispatch absent). $J_{01}$ is therefore the *normal* public form of a record that was not routed through a dispatcher. The most direct reading of citizen calls migrating en masse into $J_{01}$ during Ida is that, while 911/dispatch was down (documented by OIPM), calls were being logged in the same manner as self-initiated activity. This is a concrete, testable candidate mechanism — and it sits exactly on the paper's operational-vs-record-production distinction — yet the paper only says the pathway "remains set-valued."

**Requested changes.** (a) State the denominator explicitly. (b) Report the officer-initiated $J_{01}$ norm and the shift in the officer-initiated share (33.7% in the Ida week vs. 42.2% in the baseline week). (c) Name "calls logged in self-initiated form during the dispatch outage" as a candidate pathway and say what internal data would test it.

### 5. The main statistic's complexity buys nothing; simpler statistics give the same rank with wider separation

From `M7B_REFERENCE_STATISTICS.csv`:

| Statistic | Ida | Max reference | 2nd | Ida rank |
|---|---|---|---|---|
| $U_{\text{full}}$ (paper's LP score) | 0.2507 | 0.2125 | 0.2035 | 1 / 218 |
| `M_max_cell` (max abs. cell contrast, no LP) | 0.5072 | 0.3282 | 0.3083 | 1 / 218 |
| `U_direct` | 0.4223 | 0.3282 | 0.3083 | 1 / 218 |
| `D_upper` (prespecified secondary) | 0.1716 | 0.2835 | 0.2535 | **4 / 218** |
| `Q_upper` (prespecified secondary) | 0.4944 | 0.9408 | 0.9136 | **147 / 218** |

The plainest statistic gives the same rank with a larger gap. The constrained minimax LP, 333 million support triples, branch-and-bound coverage certificate, HiGHS replication, and Lean formalization add nothing to the conclusion while making the paper hard to read and hard to referee. Three further points:

- **The timing placebo is unfavourable** (advantage interval [−0.114, −0.098]): the institutional support library (12-hour shifts, anti-looting redeployment, curfew) fits Ida *worse* than arbitrary translations of itself. The paper concedes "no precise alignment," but does not draw the consequence: the score is then just distance from a three-column step basis, and the institutional labels attached to it carry no content.
- The M7A exclusion threshold of 0.25 is cleared by **0.0007 (0.3%)**. The rank does not depend on the threshold, as the paper says, but the M7A decision "restricted-support class excluded" is on a knife-edge and should be described as such.
- `Q` and `D` are prespecified secondary statistics in the spec. Ida ranks 147/218 on `Q` and 4/218 on `D`. Neither is reported. Whatever their definitions, prespecified statistics on which the focal observation is *not* extreme must be reported.

**Requested changes.** Use `M_max_cell` (or a norm of $G$) as the headline statistic; move the LP score to a robustness appendix; compress the Lean material to one paragraph. Report the Ida rank on every prespecified secondary statistic.

### 6. No sampling uncertainty; "finite-population exactness" does not answer the question

Cell contrasts of ±0.4–0.5 are computed from 206–674 event records spread over 27–60 strata. Among the nine "abnormal" cells, B4 (−0.216) and B8 (−0.228) sit within stratum-level noise of the threshold 0.2094, and under the stage-era threshold (0.2247, in the package JSON) B4 is no longer abnormal. Appendix §8.1 says the numbers carry only floating-point error; that answers "given this file" but not "if this file were regenerated."

**Requested changes.** Provide record-level bootstrap intervals within strata (or a permutation of bin labels across reference windows) for each cell contrast and for `M_max_cell`; report effective record counts per cell; avoid binary "abnormal" language for marginal cells.

### 7. The "composition-only exclusion theorem" is an identity, and the six witnesses are not independent

Theorem 1 says: if $q^E = q^R$, then $\Delta H_{11}$ and $\Delta H_{01}$ have the same sign. Observing opposite signs is equivalent to "$q$ changed within this disposition" — which Table 4 already reports directly (−0.44 to −0.65). Dressing this as a theorem with "six independent sign witnesses" verified in Lean presents an arithmetic fact as an identification result. The six cells share bins and the arrival-observed denominator; they are not independent.

**Requested change.** Demote to a remark; present the within-disposition change in $q$ directly. Keep the Kitagawa decomposition; one sentence on it suffices.

### 8. The DV application contains no DV data and only textbook bounds

Equations (12)–(17) are Manski's missing-outcome bounds, pointwise mixture bounds, and definitional statements ("endpoints do not identify the path between them"). The "witness necessity" arguments reduce to "a duration needs two timestamps." None of this is wrong, but none of it needs a paper, and the text states that no DV quantity is estimated. A referee will ask what this section contributes; the current answer is "a list of data a future study would need," which is a research proposal.

**Requested change.** Either (a) compress to two pages as an illustration and merge Tables 6 and 7, or (b) actually run the declared labelling rule on the 2021 file: report $N_1$ and $N_U$ for DV-related `initialtype` codes, the endpoint coverage $\pi_E$, and the $J$-state distribution of DV-labelled records during Ida. Even a descriptive table would be more valuable than symbols.

### 9. Inaccurate captions and unreported thresholds

- Figure 2's caption says "the narrow score intervals do not overlap." Fifty of the 217 reference intervals have width > 0.01; the maximum is **0.070** (`optimization_intervals.maximum_width`). The figure plots only upper endpoints, which is conservative for the separation claim, but that should be stated and "narrow" removed or restricted to Ida.
- §5.3 uses only the full-set threshold (0.2094). The stage-era (0.2247) and same-season (0.2057) thresholds are in the package and should be reported with their effect on the nine-cell set.
- §7's 2025 numbers (dispatch completeness 41.8%, arrival 83.7% — nearly half of arrival-observed records lack a dispatch field) are the paper's second-strongest result and are treated as an aside. Together with comment 1 they should be a headline.

### 10. Framing, naming, and key citations

- The framework is named BELAND-PLUS and is said to "extend the police-workload perspective associated with Beland (2026)," whose bib entry is an *"unpublished conceptual presentation."* An inaccessible talk cannot anchor the contribution. State the workload framework in equations (1)–(2) on its own authority and cite Brent and Beland (2020), which is published. A neutral method name (e.g., "public-record field-presence stress test") is advisable; naming a method after one's supervisor invites questions in external review that the paper does not need.
- `\author{}` is empty; the paper is dated 24 August 2026 and cites several 2026 items (including a dashboard "refreshed July 17, 2026"). Confirm each is publicly accessible before submission.

---

## Minor comments

1. **Vocabulary.** *Topology* (the object is a 10×3 contrast matrix, not a topology), *witness* (auxiliary data), and *qualified / frozen / locked / authority / firewall / TESTED_ONLY* are internal project-management terms that have leaked into the prose. Economics and public-administration readers need plain language: auxiliary data, prespecified, validated.
2. §3.4's point that "each bin indexes when a record was created; field states are taken from the eventual released record" is central — it means the late $J_{01}$ cells may reflect back-filled arrival fields without back-filled dispatch fields. It belongs beside the main result in §5, not inside the bin definition.
3. Table 2 (bins) duplicates Appendix Table 1, and its "Role" column pre-announces results; move to the results section or drop.
4. Figure 3 (the heat map) shows 9 numbers in 14 cells; a table is clearer. If kept, include B1, B9, and B10 so the reader sees the non-exceeding contrast.
5. Figure 4: "Total" and "Within" bars nearly coincide and "Composition" is ≈ 0; one sentence replaces the figure.
6. §3.1 is admirably honest that the design is "post-anchor prospective." Add whether the M7A threshold (0.25) and support library were frozen before or after Ida's $G$ matrix was seen; a reader cannot currently tell.
7. Appendix §6.4–6.6 (Fréchet bounds, queue non-identification, regularization) and §7 (54 regimes, tagged unions, reachability) play no role in any stated result; move to online supplementary material.
8. Notation: $R$ denotes both the record process (eq. 2) and the disposition variable (Appendix §5, $R = r$). Use a different letter.
9. References: `Pandey2025` is a working paper; `BelandPlusM8P2026` is a self-referential project artifact and should not appear in the bibliography.
10. `README.md` and `START_HERE.md` are identical; keep one.

---

## A suggested restructuring

The strongest version of this paper is about 12–15 pages:

1. **Public CAD field completeness steps down on 28 July 2021 and drifts to 42% by 2025** — one time-series figure (comment 1).
2. **Five weeks into that regime, Ida pushes the dispatch-missing rate up another 30–50 points for two days, then it recovers within three** — daily series plus the maximum-cell rank against the stage-era reference set, with Francine as the same-regime hurricane comparison.
3. **The shift is within dispositions and matches the normal $J_{01}$ form of officer-initiated records** — name the "calls logged in self-initiated form during the outage" candidate mechanism and say what internal data would test it (comment 4).
4. **Measurement implications**: the supportable / bounded / selected / unavailable classification in one table; DV as a half-page illustration.
5. LP score, Lean, 54 regimes → online appendix.

This paper and the present one report the same fact; the shorter one would be believed and remembered.

---

## Verification notes for the authors

- Repository cloned at commit `b867d242`. Values in `M7B_RESULTS.json`, `M7B_SENSITIVITY_RESULTS.json`, `M7D_E_RESULTS.json`, and `m8p_results.json` match the text (Ida interval; 217/153/86; $c_{0.95}$ = 0.2094; the Kitagawa components; the 2025/2026 audit figures).
- All additional numbers in this report (the $J_{01}$ time series, officer-initiated shares, alternative-statistic ranks, interval widths, Ida coverage) were computed from `w2_period_tally.csv.gz`, `M7B_REFERENCE_STATISTICS.csv`, `M7B_REFERENCE_DOMAIN_AUDIT.csv`, and `M7B_REFERENCE_WINDOW_REGISTRY.json` inside the package.
- Not run: the Lean build, the LP replication scripts, and a page-by-page typographic check of the PDFs.
