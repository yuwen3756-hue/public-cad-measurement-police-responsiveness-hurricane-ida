# Response to the R15.0 reviews

This additive R15.1 package evaluates the two R15.0 reports together with the earlier review record. The published R15.0 package and its scientific-result objects remain unchanged. Reviewer recommendations are treated as evidence and editorial advice, not as scientific authority.

| Review item | R15.1 implementation |
|---|---|
| Explain the measurement for a new reader | The abstract and opening introduction now define the observable: presence and validity of released `TimeDispatch` and `TimeArrive` fields and changes in their four joint states. They state immediately that these are not response times or physical-event indicators. |
| Reduce abstract density | Retains the break date, Ida magnitude/rank, coverage caveat, qualified bootstrap statement, and interpretation boundary; moves denominator trends and daily officer percentages to the body. |
| Correct Miller-Segal placement | Separates the police-composition citation from pandemic-era studies and adds Leslie-Wilson and Miller-Segal-Spencer (2022). |
| State the literature contribution | Adds a synthesis paragraph identifying the regime-change finding, the within-regime Ida stress result, and the measurement-validity requirement. |
| Remove “topology” jargon | Replaces it with “joint field-presence distribution” or “field-presence configuration.” |
| Make ranks consistent | Uses rank $1/(R+1)$ including Ida throughout: standardized $1/154$, stage-era full-count $1/151$, and post-change full-count $1/152$. |
| Label the post-change universe | States that it was defined after the July break was identified and is a post-hoc comparison; the stage-era universe remains the prespecified comparison. |
| Show the Ida time path | Adds `source/r15_1_ida_time_path.csv` and a daily main-paper figure for dispatch presence, valid arrival, and $J_{01}$ among arrival-observed records from 22 August through 12 September. |
| Mention post-Ida and Francine | Adds their full-count values and explains that the post-Ida week uses Ida as its baseline, while Francine is a much smaller later-regime hurricane comparison. |
| Acknowledge omitted Cristobal context | Labels the 7 and 14 June 2020 windows, cites the official NHC report, states that Cristobal was not a prespecified exclusion, and leaves frozen rank membership unchanged. |
| Address adjacent-window dependence | Explains that one event week becomes the next baseline and adds two alternating non-overlap phases with ranks $1/77$ and $1/76$ including Ida. |
| Qualify the bootstrap | Calls it a conditional window-wise multinomial perturbation that does not model temporal dependence; it is not presented as formal time-series rank inference. |
| Narrow “record-production” and “all-record” | Uses “released-record discontinuity” and “unstandardized full-count statistic using all non-officer records.” |
| Strengthen the officer-stream interpretation | States that missing public dispatch fields cannot be read as officer absence for officer-generated items. It does not adopt the stronger claim that public data identify the exact record-production or export mechanism. |
| Complete dataset and policy citations | Adds separate official DataNOLA entries for 2020 and 2022-2024 and a direct citation to the NOPD policy page/manual. |
| State agency-contact status | States that no agency confirmation was available and no City, OPCD, or NOPD contact was conducted for this public-source revision. |
| Make the raw audit portable | Adds `--source-root PATH` and `BELAND_PUBLIC_SOURCE_ROOT`; renames `cache_mtime_utc` to `cache_mtime_with_offset`. |
| Enforce raw/aggregate parity | Adds `source/r15_1_raw_aggregate_parity.csv`; the verifier checks all 56 state cells across seven days and two initiation streams. |
| Windows clone guidance | Adds a fresh-clone / `core.autocrlf=false` instruction because the manifest is byte-exact and `.gitattributes` disables text normalization. |
| Clarify the legacy archive | Adds a prominent historical-version note and replaces stale body references to R14.0 with version-neutral wording. |

The optional call-type localization was not added. It would introduce a new empirical decomposition requiring an authoritative, period-appropriate code-label crosswalk and privacy-safe first-hand semantic review; it is outside a Paper R15.1 / Scientific Results R15 text-and-package repair.

Scientific boundaries are unchanged: the package does not identify causal effects, physical response, effective capacity, true domestic-violence incidence, or a generating mechanism.
