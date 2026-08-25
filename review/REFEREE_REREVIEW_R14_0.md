# Referee re-review of R14.0

## Verdict

**R14.0 successfully answers the substance of the second referee report.** The manuscript is now a much shorter, more transparent, and more credible measurement paper.

I would change the recommendation from **major revision** to:

> **Minor revision / conditional pass, with one material denominator correction required before circulation.**

The second report’s three central objections were the omitted July 2021 data-regime change, an inadequately comparable reference class, and excessive mathematical apparatus relative to the empirical finding.  R14 directly restructures the paper around those criticisms:

- the July 28 break is now the first result;
- the non-officer-initiated denominator is explicit;
- the stage-era ordinary-week comparison is primary;
- $M_{\max}$ replaces the LP as the headline statistic;
- Ida’s support failure is disclosed;
- excluded emergencies, secondary-statistic ranks, threshold sensitivity, and conditional bootstrap uncertainty are reported;
- the within-disposition result is treated as accounting;
- the DV section is reduced to an illustration.

The exact reviewed commit is `477005b419cc1280b7e510e3b7cc9c068911545e`. 

---

# 1. Response to the ten referee findings

| R13 referee finding | R14 status | Assessment |
|---|---|---|
| July 28 public-file regime break omitted | **Closed** | It is now the paper’s first empirical result, with daily, monthly, and period summaries. |
| Ida fails the reference eligibility rule | **Closed** | Per-bin counts and coverage are in the main text, and the failure is stated in the abstract. |
| Other emergencies and holidays excluded | **Substantially closed** | Laura, Zeta, the freeze, post-Ida, and Francine are shown as labeled full-count comparisons. |
| “All-call” denominator was wrong | **Closed for the Ida estimator** | The paper now states that the primary universe is non-officer-initiated records. |
| LP complexity dominated the paper | **Closed** | $M_{\max}$ is primary; the LP is explicitly supplementary robustness. |
| No sampling uncertainty | **Substantially closed** | R14 adds a 4,000-replicate conditional within-stratum bootstrap and cell-level interval file. |
| Composition theorem overstated | **Closed** | It is now an accounting implication, not a new identification theorem. |
| DV section contained no DV estimates | **Closed** | It is compressed to one measurement table and a short prospective illustration. |
| Thresholds and captions incomplete | **Closed in the main paper** | All three thresholds are reported; marginal cells are no longer called categorically abnormal. |
| Framing, naming, and inaccessible citations | **Mostly closed** | The main paper is written in ordinary academic language and no longer relies on the unpublished project presentation. |

This is very close to the shorter structure recommended in the referee report: regime change, Ida spike, officer-initiation comparison, and a concise measurement implication. 

---

# 2. What is now particularly strong

## 2.1 The paper begins with the correct empirical fact

The new abstract states that $J_{01}$—arrival present, dispatch absent—is absent from 419,840 non-officer-initiated records through July 27, 2021, first appears on July 28, and becomes persistent thereafter. It also makes the support failure, ordinary-week rank, officer-initiated resemblance, and non-identification boundary visible immediately. 

The daily evidence supports the language of an observable public-file discontinuity:

- July 27: $J_{01}\mid A=0$;
- July 28: $J_{01}\mid A=0.0677$;
- July 29: $0.1297$;
- July 30: $0.1163$;
- subsequent August values generally remain positive. 

The paper correctly says that this is a break in the **observable public file**, not proof of a CAD-system change, export-policy reform, or operational mechanism. That is the scientifically defensible interpretation.

## 2.2 The empirical estimand is finally transparent

The main paper now explicitly defines the primary denominator as **non-officer-initiated public records** and acknowledges that the prior phrases “all calls” and “all reported calls” were inaccurate. It also explains that bins index call creation and that the fields come from the eventual released record. 

That resolves two major interpretive hazards at once:

- the estimator does not cover the complete public file;
- a late $J_{01}$ value is not a contemporaneous claim that a physical arrival happened without dispatch.

## 2.3 The simple statistic now carries the finding

The primary statistic is now:

$$
M_{\max}(G)=\max_{t,j}|G_{tj}|.
$$

For Ida it equals $0.5072$, compared with a largest stage-era ordinary-week reference value of $0.3282$. The paper also reports a raw full-count maximum-cell contrast of $0.5320$. 

This is a major improvement. A reader no longer needs to understand the 333-million-support-triple optimization before learning the empirical fact.

The manuscript also reports every stored secondary-statistic rank rather than selectively presenting only favorable measures. Ida is:

- first on $M_{\max}$, $\sigma_1$, $\sigma_2$, $U_{\text{direct}}$, and $U_{\text{full}}$;
- eleventh on $\sigma_3$;
- one-hundredth on $Q$ in the stage-era set;
- fourth on $D$. 

The resulting interpretation—an unusually large field-state reconfiguration rather than uniform extremeness under every mathematical summary—is accurate.

## 2.4 The support limitation is handled honestly

R14 reports all ten event/reference counts and coverage rates. Record-weighted coverage is:

- event side: $86.1\%$;
- baseline side: $77.0\%$;

and Ida would fail the $0.90$ symmetric screen imposed on candidate reference windows. 

The machine-readable diagnostic independently records the same conclusion. 

This is now properly treated as a comparability qualification rather than hidden in a domain-audit artifact.

## 2.5 The excluded-episode comparisons add real context

The raw maximum-cell comparisons are now shown for:

- Laura: $0.084$;
- Zeta: $0.129$;
- February freeze: $0.113$;
- Ida: $0.532$;
- post-Ida week: $0.478$;
- Francine: $0.110$. 

The interpretation is good:

- the post-Ida week is large partly because Ida is its paired baseline and the public fields reverse;
- Francine is in the later field-production regime but does not resemble Ida;
- pre-July 2021 emergencies cannot generate a $J_{01}$ rise in a regime where $J_{01}$ is absent.

This directly answers the question of whether the Ida pattern is merely “what hurricanes look like.”

## 2.6 The uncertainty language is appropriately conditional

The new bootstrap resamples categorical state counts within fixed event/reference strata and fixed baseline weights. The resulting interval for $M_{\max}$ is approximately:

$$
[0.460,\ 0.566].
$$

The paper and manual correctly state that this does not capture:

- temporal dependence;
- uncertainty in the July 28 regime boundary;
- reference-class selection;
- event selection;
- or comparison-design uncertainty.  

The individual cell intervals are also retained in a machine-readable file, together with counts and support coverage. 

## 2.7 The within-disposition result is now proportionate

The paper retains the useful Kitagawa result:

- August 31 PM total: $-0.4950$;
- composition: $+0.0119$;
- within disposition: $-0.5069$;

and:

- September 1 AM total: $-0.4824$;
- composition: $+0.0123$;
- within disposition: $-0.4946$.

But it now calls this an accounting localization and explicitly preserves selection, semantic drift, unobserved composition, and recording pathways. 

The supplement likewise changes the former theorem into a restricted accounting remark and says that it is not a new identification theorem. 

## 2.8 The officer-initiated comparison is useful without being oversold

R14 reports that among arrival-observed officer-initiated records:

- Ida $J_{01}$ share: $98.9\%$;
- baseline $J_{01}$ share: $99.6\%$.

Officer-initiated records account for:

- $33.7\%$ of all public records during the five-day Ida window;
- $42.2\%$ in the paired baseline. 

The proposed pathway—some non-officer-originated records may have been entered in a form resembling self-initiated activity—is clearly labeled as a candidate requiring internal provenance and audit histories. 

That is exactly the right balance between presenting an insight and respecting non-identification.

---

# 3. Material correction still required: the 2025 denominator is inconsistent

This is the one issue I would correct before calling R14 fully closed.

The main paper’s primary longitudinal denominator is **non-officer-initiated records**. It reports non-officer dispatch-field completeness of $65.4\%$ in 2024. But the abstract and longer-regime section then report **41.8% in 2025** without explaining that this is an **all-record** figure.  

The packaged 2025 audit provides the required split:

| 2025 population | Rows | Dispatch present | Dispatch completeness |
|---|---:|---:|---:|
| Non-officer initiated, `SelfInitiated=N` | 207,050 | 136,712 | **66.03%** |
| Officer initiated, `SelfInitiated=Y` | 122,720 | 1,117 | **0.91%** |
| All records | 329,770 | 137,829 | **41.80%** |

The 2026 snapshot gives non-officer dispatch completeness of **66.84%**. 

Thus the comparable non-officer series is approximately:

$$
65.4\%\ \text{in 2024}
\quad\rightarrow\quad
66.0\%\ \text{in 2025}
\quad\rightarrow\quad
66.8\%\ \text{in the 2026 snapshot}.
$$

It does **not** continue declining from $65.4\%$ to $41.8\%$. The all-record rate falls to $41.8\%$ because approximately $37.2\%$ of 2025 records are officer initiated, and almost none of those have a dispatch field.

The all-record completeness file confirms that $41.8\%$ is computed over all 329,770 rows. 

## Required rewrite

The abstract should not say merely:

> “By 2025, dispatch-field completeness is only 41.8 percent.”

A correct formulation would be:

> Among non-officer-initiated records, dispatch-field completeness falls from 90.1 percent before the July 2021 break to 65.4 percent in 2024 and remains approximately 66–67 percent in 2025–2026. Across the complete 2025 public file, completeness is 41.8 percent because officer-initiated records—37.2 percent of rows—almost never carry a dispatch field.

Section 4 should similarly distinguish:

1. the **within-denominator trend** for non-officer records; and
2. the **all-file mixture statistic**, which depends strongly on officer-initiation composition.

This correction strengthens rather than weakens the paper. It demonstrates exactly why denominator declaration is indispensable.

---

# 4. Remaining medium-priority scientific issues

## 4.1 Validate the July 28 break against the raw public source

The July 28 result is currently rebuilt from the processed aggregate tally. The R14 builder reads the aggregate `w2_period_tally.csv.gz` and locked M7B artifacts, not the underlying row-level 2021 source.  

That is sufficient to verify the result **within the package**, but because the regime break is now the paper’s central finding, an external version should independently establish that it is not a preprocessing artifact.

Add a narrowly scoped raw-source audit for July 25–31, 2021:

- count raw nonblank dispatch and arrival fields directly from the official 2021 file;
- show the raw string/timestamp validity rules;
- verify that July 27 has zero $J_{01}$ and July 28 has positive $J_{01}$;
- report any changes in field formatting or sentinel values;
- inspect Socrata metadata/version history if available;
- bind the exact source hash.

The paper is appropriately honest that the agency has not yet been contacted.  That satisfies the referee’s immediate disclosure request, but agency or OPCD confirmation would materially improve a journal version.

## 4.2 Clarify what the “full-count” comparison does and does not avoid

The raw stage-era comparison uses all records within each half-day, but its reference windows are still selected from the original `STAGE_ERA_MATCHED_REFERENCE` membership. In the builder, `raw_stage` is formed by retaining windows whose original `prespecified_universes` field contains the stage-era label. 

Therefore it avoids **within-window common-support selection**, but it does not fully avoid **window-level selection by the original support-eligibility design**.

The genuinely support-independent post-review comparison is the set requiring both event and baseline sides to occur after July 28 and excluding only frozen context episodes. That comparison yields rank $1/152$, including Ida. 

The abstract should preferably report:

> Ida is rank 1 among 153 prespecified stage-era ordinary-week references. In a post-review full-count comparison requiring both sides to occur after July 28, it is rank 1 among 151 nonexcluded reference windows.

That is clearer than saying that the 150-window stage-era full-count version simply “avoids common-support selection.”

## 4.3 Make the post-review promotion explicit

Both of the following were already present as frozen objects before R14:

- $M_{\max}$;
- the stage-era reference set.

But they became the headline statistic and principal reference universe **after the second referee review**. That is acceptable and scientifically sensible, but the manuscript should say so directly.

A useful sentence would be:

> The maximum-cell statistic and stage-era universe were prespecified and stored in the R12 artifacts, but R14 promotes them to the headline presentation after referee review because they are more transparent and better aligned with the observed data regime; the promotion is post-review rather than an ex ante primary designation.

Similarly, identify the July 28 analysis, bootstrap, full-count rank, and excluded-episode table as post-review diagnostics generated from already packaged data.

## 4.4 Extend uncertainty to the comparison distribution

The bootstrap currently provides conditional uncertainty for Ida’s standardized matrix and $M_{\max}$. It does not bootstrap the highest reference-window values or the raw full-count statistic.

Given the large gap, this is unlikely to overturn the rank. Still, a stronger uncertainty presentation would:

- bootstrap Ida and the top five stage-era references under the same procedure;
- report whether the intervals remain separated;
- or report a bootstrap distribution of Ida’s empirical rank.

For the full-count result, add an analogous categorical bootstrap based on the complete half-day state counts.

## 4.5 Show the officer-initiated pattern over a longer period

The officer comparison is currently reported for the five-day event and baseline windows. It would become more informative with a simple monthly series showing:

$$
\Pr(J_{01}=1\mid A=1,\ \text{officer initiated})
$$

from 2020 through 2024.

That would establish whether the approximately $99\%$ officer-initiated configuration is:

- a longstanding public-record convention;
- another feature that begins in July 2021;
- or a changing convention.

This distinction bears directly on the candidate “self-initiated form” pathway.

---

# 5. The online supplement needs a consistency pass

The ten-page main paper is now well organized. The thirty-page supplement still preserves several R13-era formulations that can conflict with the new hierarchy.

For example, the supplement still:

- lists the full 217-window design first as the “locked reference results”;
- calls the full-set threshold $0.2094$ “the common threshold”;
- lists nine “abnormal” cells;
- uses the full-set rank language before the stage-era comparison;
- does not state the non-officer-initiated denominator at the first formal definition of the risk set.  

The main paper, by contrast, makes the stage-era design primary, reports eight cells under its threshold, and avoids binary abnormality language. 

This can be repaired without deleting the legacy mathematics. Add an explicit **R14 interpretation hierarchy** at the beginning of the supplement:

1. primary descriptive statistic: stage-era $M_{\max}$;
2. primary denominator: non-officer-initiated records;
3. support-qualified standardized analysis;
4. post-review raw full-count sensitivity;
5. full 217-window LP results retained only as historical robustness;
6. threshold counts are universe dependent: 9 / 8 / 9.

Also change the supplement’s notation so that the record-production process and recorded disposition do not both use $R$. The main paper already uses $R_t^{\mathrm{rec}}$; the supplement should follow it.

---

# 6. Source and citation repairs

## 6.1 Cite the full 2020–2024 data lineage

The central field-completeness series covers 2020–2024, but the main text cites only the 2021 public dataset when introducing it.  The bibliography contains 2021, 2025, and 2026 dataset entries, but not explicit 2020, 2022, 2023, and 2024 annual dataset bindings. 

Add a compact data-source table containing, for each year:

- official dataset ID;
- observed date range;
- row count;
- retrieval date;
- source SHA-256;
- parsing/schema version.

This is especially important now that the longitudinal break is the main contribution.

## 6.2 Cite the documented dispatch disruption

The officer-initiated candidate-pathway paragraph refers to disrupted dispatch operations, but the main text should attach the OIPM citation directly to that statement. The bibliography retains the OIPM report, so this is a simple citation placement repair.

---

# 7. Reproducibility and package notes

## Positive changes

The R14 builder is transparent and compact enough to review directly. It:

- verifies state-count identities;
- rebuilds the daily, weekly, and monthly series;
- calculates the raw and standardized ranks;
- reproduces the locked Ida matrix exactly;
- creates the conditional bootstrap;
- reports all secondary statistics and thresholds;
- emits one machine-readable diagnostic object.   

The PDF builder now checks unresolved references, citations, BibTeX warnings, and overfull boxes. 

The `.gitattributes` policy is also a useful attempt to preserve byte-exact package files across platforms. 

## Minor repairs

1. The reproduction manual says the analysis defines **five** mutually exclusive field-presence states. The paper and code define four: $J_{00},J_{10},J_{01},J_{11}$.  

2. The manual says pandas is used by the R14 builder, but the builder imports NumPy and standard-library modules, not pandas. Pandas is nevertheless added to `requirements.txt`.  

3. The release manifest includes the research package and scripts but does not appear to include repository-facing files such as `README.md` and `.gitattributes`, despite language that it binds every distributed file except itself. Either include those files or define them explicitly as repository controls outside the release payload.  

4. Several legacy artifact Git blob SHAs changed from R13 to R14 while the displayed numerical content remained identical, consistent with line-ending or packaging normalization. For example, the first records of `M7B_REFERENCE_STATISTICS.csv` are unchanged but the Git blob SHA differs across the two commits.   Add a short predecessor-parity receipt explaining byte-level normalization and confirming semantic equality of the frozen tables.

---

# Final recommendation

## For Professor Beland

**R14 is ready after the 2025 denominator correction.**

It now presents a memorable and defensible result:

> A new public-field configuration appears abruptly in late July 2021; Ida creates a further extreme but temporary reconfiguration within that changed regime; public fields therefore cannot automatically be interpreted as operational response clocks.

## For working-paper circulation

**Minor revision.**

Required before circulation:

1. correct the 2025 all-record versus non-officer denominator;
2. align the supplement with the R14 primary hierarchy;
3. cite and bind the full 2020–2024 data sources;
4. clarify the post-review promotion of $M_{\max}$ and the stage-era set.

## For journal submission

The next strongest additions would be:

1. a direct raw-source audit of July 27–29, 2021;
2. agency or OPCD inquiry concerning the July 2021 change;
3. bootstrap uncertainty for the top reference windows and raw statistic;
4. a longer officer-initiated field-state series.

These are now **targeted validation tasks**, not another conceptual overhaul.

## Overall editorial movement

- **R13:** major revision.
- **R14 as published:** minor revision because of one material denominator inconsistency.
- **R14 after that correction:** credible professor-facing paper and defensible external working paper.

I reviewed the source, generated evidence files, construction script, verification logic, and supplement at the published commit. I did not execute the complete package or conduct a page-by-page rendered-PDF inspection in this environment.