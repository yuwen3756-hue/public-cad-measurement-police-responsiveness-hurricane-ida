# Referee re-review of R15.0

## Verdict

**R15.0 closes the three remaining architecture problems.** The exact published commit is `5e2af0f0e8a9d1aef24017c91ef1a7109073262a`. 

My recommendation moves to:

> **Pass for Professor Beland’s review; minor revision before wider working-paper circulation.**

There is no longer a need for another conceptual overhaul. The paper is now recognizably a clean academic manuscript rather than a cumulative technical report. The original referee’s three major concerns were the omitted July data-regime change, the comparability of the reference design, and the excessive mathematical apparatus relative to the finding.  R15 addresses all three directly and follows the shorter empirical structure recommended in that report. 

---

# Assessment of the three requested refinements

| Requested refinement | R15 assessment | Verdict |
|---|---|---|
| Overhaul the mathematical appendix | A new empirical and methods supplement now follows the current estimand; the former mathematical appendix is a separately labeled legacy archive and is excluded from the professor-facing combined PDF. | **Closed** |
| Rewrite the paper as a self-contained latest version | The main manuscript has been rewritten from a blank R15 source rather than patched from R14. Revision-history language is absent and machine-checked. | **Closed** |
| Expand the literature review | Four distinct subsections now position the paper against response-time research, administrative measurement, disaster/DV research, and partial identification. | **Substantially closed; one citation repair remains** |

---

# 1. The appendix overhaul is successful

This is the clearest structural improvement in R15.

The new **Online Empirical and Methods Supplement** begins by defining the evidence hierarchy and then follows the actual R15 paper:

1. annual public-source lineage;
2. the raw July audit;
3. state construction and estimator;
4. common-support coverage;
5. standardized and full-count bootstrap results;
6. threshold and secondary-statistic sensitivity;
7. excluded emergencies;
8. officer-initiation patterns;
9. disposition accounting;
10. current denominator audit;
11. institutional-source audit;
12. DV measurement implications;
13. reproduction and claim indexing.   

That is now the correct professor-facing appendix. It begins from the empirical claims, rather than beginning from the old identified-set and constrained-optimization program.

The previous extended mathematics is preserved as a **Legacy Mathematical and Formal-Verification Archive**. Its cover explicitly states that it is not appended to the professor-facing paper and is intended only for readers who need the longer proofs, constrained programs, identified-set constructions, and formal verification. 

The release verifier enforces the separation:

- main paper: 9–16 pages;
- empirical supplement: 12–18 pages;
- research-status note: one page;
- legacy archive: at least 25 pages;
- combined professor PDF: main paper plus empirical supplement only;
- legacy-archive title must not appear in the combined PDF. 

**This fully implements the appendix proposal.**

### One archival cleanup remains

The legacy archive still contains inherited sentences such as:

> “R14.0 retains the locked R12 system-level matrix…”

That is not a problem for the current paper because the archive is properly separated, but it would be cleaner to add a conspicuous statement that the body preserves historical version language, or replace the few stale R14 sentences with version-neutral wording. The archive should read as an intentional historical technical record, not an accidentally outdated R15 appendix.

---

# 2. The main paper is now self-contained

The new main source is a complete rewrite of 279 lines rather than an incremental edit to the 709-line R13 document. It contains no body-text references to R12, R13, R14, the referee, a previous version, or a “post-review” analysis. The verifier explicitly scans for those phrases. 

The paper now proceeds naturally:

- research problem;
- operational-versus-record observation map;
- contribution;
- related literature;
- official data and denominator;
- raw July audit;
- comparison design;
- standardized and full-count results;
- institutional evidence;
- current denominator discipline;
- concise DV implications;
- limitations and conclusion.   

Several especially important repairs are now complete.

## Denominator repair

The paper consistently defines the main population as **non-officer-initiated public CAD records** and analyzes officer-initiated records as a separate administrative stream. 

The 2025 inconsistency is fixed correctly:

| Year | Denominator | Dispatch completeness |
|---|---|---:|
| 2024 | Non-officer | 65.38% |
| 2025 | Non-officer | 66.03% |
| 2025 | Officer | 0.91% |
| 2025 | All rows | 41.80% |
| 2026 snapshot | Non-officer | 66.84% |
| 2026 snapshot | Officer | 0.93% |
| 2026 snapshot | All rows | 41.88% |

The paper now explains that the $41.8\%$ figure answers a different question because it pools two streams with radically different public-field conventions.  

## Raw July validation

The paper now audits the official July 2021 compressed CSV directly rather than relying solely on the aggregate tally. It verifies:

- zero non-officer $J_{01}$ records through July 27;
- 34 on July 28;
- 69 on July 29;
- full parseability of nonblank dispatch and arrival fields;
- simultaneous collapse of officer-stream dispatch-field presence. 

The raw audit script reads official cached monthly files and writes only aggregate counts, format classes, dates, and hashes. It does not persist row-level records, addresses, narratives, or identifiers. 

This materially strengthens the paper’s first result. The July discontinuity is no longer merely a feature of one downstream aggregate file.

## Source lineage

The supplement now binds each 2020–2024 analysis year to:

- official dataset ID;
- observed creation-date range;
- raw row count;
- twelve monthly source files;
- deterministic annual bundle digest;
- parser version;
- verification date;
- explicit disclosure that retrieval dates were not stored in the monthly cache.  

## Full-count and uncertainty analysis

The paper now distinguishes:

- the common-support standardized calculation;
- the full-count calculation using every non-officer record in each half-day;
- the inherited stage-era membership comparison;
- the genuinely post-change comparison requiring both event and baseline periods to begin after July 28. 

It also adds:

- Ida’s standardized bootstrap interval;
- the five strongest standardized-reference intervals;
- Ida’s full-count interval;
- the five strongest post-change full-count reference intervals;
- a conditional rank perturbation against all 151 post-change references.  

## Institutional evidence

The institutional section is properly bounded. It uses public documents to:

- define field labels and provider;
- document public warnings about accuracy and over-time comparison;
- provide Ida oversight context;
- establish that the Carbyne APEX cutover occurred in June 2022, too late to explain July 2021;
- establish that the Hexagon records-management system was not implemented before the contract was cancelled.

The official OPCD page dates the Carbyne cutover to June 24, 2022, and the OIG summary states that Hexagon was not yet implemented when its contract was cancelled. 

The paper correctly treats this as **negative evidence against two proposed explanations**, not identification of the remaining mechanism. 

---

# 3. The literature review is much better, but needs one final edit

The literature section now has the exact four-part architecture recommended:

1. response time and first-responder performance;
2. administrative records and measurement error;
3. disasters and domestic violence;
4. partial identification and uncertainty. 

For a roughly ten-page main paper, this is no longer unacceptably thin. It gives readers a disciplinary map without returning to the sprawling R12–R13 literature discussion.

The key contribution is also substantially clearer:

- existing response-time studies show why valid clocks matter;
- administrative-data studies show that recorded objects may differ from underlying events;
- disaster/DV studies motivate the substantive application;
- partial identification supplies the language for selected, bounded, and unavailable quantities.

## Citation-placement correction

The following sentence needs revision:

> “Pandemic-era studies similarly show that calls, reports, and underlying victimization need not move one-for-one $\citep{MillerSegal2019,BullingerCarrPackham2021,MillerSegalSpencer2024}$.”

`MillerSegal2019` is **not** a pandemic-era study. It is *Do Female Officers Improve Law Enforcement Quality? Effects on Crime Reporting and Domestic Violence*. The bibliography itself makes this clear. 

A better sequence is:

> Police composition can affect crime reporting and domestic-violence reporting $\citep{MillerSegal2019}$. Pandemic-era studies show that calls, reports, and underlying victimization need not move one-for-one $\citep{LeslieWilson2020,BullingerCarrPackham2021,MillerSegalSpencer2022,MillerSegalSpencer2024}$.

## Add one synthesis paragraph

The section would benefit from a final paragraph such as:

> Relative to these literatures, the paper contributes three findings. First, it documents a date-localized change in the joint presence of public CAD fields, rather than assuming a temporally stable administrative measurement regime. Second, it shows that Ida produces an additional extreme but temporary reconfiguration within the later regime. Third, it translates those facts into a measurement requirement: response-time and reported-DV analyses must validate the denominator, public endpoints, endpoint coverage, and stage lineage before interpreting released durations as operational performance.

That would make the novelty explicit rather than leaving readers to infer it across four subsections.

## Remove the remaining “topology” language

The literature section says:

> “The distinctive evidence here is topological…”

and the conclusion refers to “field-presence topology.”

The referee had already identified *topology* as unnecessary internal jargon. 

Use:

- “joint field-presence distribution”;
- “field-presence configuration”; or
- “joint dispatch–arrival field pattern.”

---

# Remaining substantive refinements

These are not grounds for another major revision, but they should be addressed in an R15.1 text-and-package repair.

## 1. Show the actual Ida time path

The main paper now contains:

- the raw July-break table;
- the monthly 2020–2024 regime figure;
- the reference-rank figure.

It does **not** contain a simple visual of the Ida two-day reconfiguration itself. The reader learns that $M_{\max}=0.5072$, but does not immediately see which field state moved, when it moved, and how quickly it recovered.

The source package already contains the required daily and half-day information. Add one compact figure or table showing, around August 22–September 12:

- dispatch-field share;
- arrival-field share;
- $J_{01}$ among arrival-observed records;
- Ida window;
- post-Ida recovery.

That would complete the empirical narrative recommended by the original referee: pre-Ida regime change, Ida spike, and recovery.

## 2. Mention Francine and the post-Ida week in the main paper

The empirical supplement reports:

- Francine: raw $M_{\max}=0.110$;
- post-Ida week: $0.478$;
- Ida: $0.532$. 

These comparisons should receive at least one sentence in the main results. Francine is especially valuable because it is a hurricane in the later public-data regime. The result that Francine is much smaller helps distinguish “generic later-regime hurricane” from the Ida-specific public-field reconfiguration.

## 3. Narrow two phrases

The result box currently says:

> “The public evidence identifies a record-production discontinuity…”

The raw audit identifies a **released-record or public-file discontinuity**. It does not identify that the generating change necessarily occurred in record production rather than in some operational-to-record interaction.

Replace it with:

> “The public evidence documents a released-record discontinuity…”

Similarly, replace:

> “The all-record, full-count Ida statistic…”

with:

> “The unstandardized full-count statistic using all non-officer records…”

“All-record” can otherwise be misread as including officer-initiated rows.

## 4. Qualify the bootstrap-rank statement

The code resamples each post-change reference window separately and then compares the independently perturbed window statistics with Ida. Overlapping reference windows may share underlying half-days, but the bootstrap does not preserve that cross-window dependence.  

The paper already states that the bootstrap does not capture temporal dependence, which is good. The abstract should nevertheless use narrower wording:

> “In a conditional window-wise multinomial bootstrap that does not model temporal dependence, Ida ranks first in all 4,000 draws.”

This supports a robustness statement about categorical-count perturbations, not formal rank inference for a dependent time series.

## 5. Complete the dataset citations

The supplement lists official IDs for 2020, 2021, 2022, 2023, and 2024, and the IDs correspond to official Data.NOLA annual datasets. Official pages are available for the later annual files and carry explicit accuracy and over-time-comparison warnings. 

The bibliography, however, contains dedicated entries only for 2021, 2025, and 2026. Add either:

- separate `DataNOLA2020`, `DataNOLA2022`, `DataNOLA2023`, and `DataNOLA2024` entries; or
- one consolidated annual-source entry listing all five IDs.

Also place a direct citation after the sentence about NOPD manual chapters in the institutional section.

## 6. State the agency-contact status

The institutional section now carefully explains what public records do and do not establish, but it no longer states whether the City, OPCD, or NOPD has been contacted about the July 2021 transition.

Add one sentence:

> “No agency confirmation of the July 2021 change was available for this version.”

or report the inquiry and response status if contact has occurred.

## 7. Make the raw-source audit more portable

The raw audit script locates the source cache by walking three parent directories above the release package. That works in the project’s managed directory structure but not in an ordinary standalone clone. 

Add either:

```text
--source-root PATH
```

or an environment variable such as:

```text
BELAND_PUBLIC_SOURCE_ROOT
```

The manual currently says to run the package “inside the project,” so the limitation is disclosed.  Still, a configurable source root would make the raw audit genuinely portable.

Also rename `cache_mtime_utc`: the script writes a timezone-aware local timestamp, not necessarily UTC.

## 8. Add a raw-versus-aggregate parity check

The raw July audit and aggregate tally visibly agree, but the release verifier currently checks selected raw counts rather than a full equality of all July 25–31 state cells between:

- the official raw-file audit; and
- the aggregate pipeline.

A complete $14\times4$ state-count parity check would make the claim “not an aggregate-pipeline artifact” machine-enforced rather than only visually apparent.

---

# Reproducibility assessment

R15’s reproducibility architecture is materially stronger.

The verifier now checks:

- manifest scope, including README and `.gitattributes`;
- exact five-PDF inventory;
- main, supplement, legacy, status-note, and combined-PDF page relationships;
- absence of the legacy archive from the professor-facing PDF;
- forbidden revision-history language;
- denominator arithmetic;
- raw July counts and parseability;
- support, rank, threshold, and bootstrap invariants;
- byte-identical reproduction-snapshot receipt;
- inherited M7B, M7D-E, M8P, and formal checks.  

The package also records Paper R15.0 / Scientific Results R15 consistently. 

The legacy reproduction snapshot is reported as byte-identical to the R14 predecessor across 79 files. 

I reviewed the verifier and construction logic, but I did **not** independently execute `RELEASE_VERIFICATION_PASS`. GitHub shows the committed scripts and artifacts, not a public CI run. I also could not perform a page-by-page visual rendering of the binary PDFs in this environment. The build script itself rejects undefined references, undefined citations, BibTeX warnings, and overfull boxes, and the verifier checks PDF page composition and extracted text. 

---

# Final recommendation

## Professor Beland review

**PASS.**

R15 is now a coherent, current-version paper that Professor Beland can read without knowing anything about R12–R14.

## External working-paper circulation

**Minor revision.**

The highest-priority surgical fixes are:

1. correct the Miller–Segal literature sentence;
2. add a literature-contribution synthesis paragraph;
3. replace “record-production discontinuity” and “all-record” with narrower terms;
4. show the Ida time path in one compact visual;
5. mention Francine and the post-Ida comparison in the main text;
6. qualify the bootstrap rank as a conditional window-wise perturbation.

## Version recommendation

These repairs do not require new scientific results. They can be issued as:

> **Paper R15.1 / Scientific Results R15**

The conceptual and package overhaul is complete. What remains is academic polish, tighter statistical phrasing, and a few reproducibility refinements—not another redesign of the project.
