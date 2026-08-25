# BELAND-PLUS M7B reference calibration mega review

# BELAND-PLUS M7B

Status: `M7B_READY_FOR_EXTERNAL_STATISTICAL_REVIEW`. Start with `01_M7B_EXECUTIVE_BRIEF.md`; machine results are in `M7B_RESULTS.json`. No causal, mechanism, capacity, physical-response, coverage-generalization, or incidence claim is opened.

---

# M7B executive brief

The exact M5-primary Ida matrix reproduced within 4.13e-13. Reference counts are {'FULL_QUALIFIED_REFERENCE': 217, 'STAGE_ERA_MATCHED_REFERENCE': 153, 'SAME_SEASON_STAGE_REFERENCE': 86}. The primary interval rank is `{'R': 217, 'definitely_more_extreme': 0, 'possibly_more_extreme': 0, 'rank_lower': 1, 'rank_upper': 1, 'p_lower': 0.0045871559633027525, 'p_upper': 0.0045871559633027525}`. No reference interval overlaps the Ida interval, so Ida is rank 1 and the result is `M7B_READY_FOR_EXTERNAL_STATISTICAL_REVIEW`. These are descriptive empirical-reference patterns.

---

# M7B prospective reference specification

Status: `FROZEN_BEFORE_PSEUDO_EVENT_OUTCOMES`.

This post-anchor prospective derivative freezes the three reference universes, the exact M5-primary paired-window estimator, five-day common-support eligibility, chronological overlap thinning, primary and secondary statistics, interval optimization, ranks, max-cell threshold, timing and duration placebos, exchangeability language, and stop rules. The machine-readable file is authoritative.

The leave-one-out rule concerns empirical calibration: window $r$ is omitted from its own calibration pool. It does not replace the locked event-versus-seven-days-earlier estimator with a pooled estimator.

The primary eligibility threshold is the locked symmetric five-day 0.90 coverage rule. Per-bin coverage remains visible in the domain audit and is not silently promoted into a new gate.


---

# Authority and lock receipts

M6: `LOCKED_WITH_QUALIFIERS`. M7A: `MATH_LOCKED_WITH_QUALIFIERS`. M7A interval: `(0.25073448467090204, 0.25073449467090003)`. Frozen manifest, G hash, 333089280 candidate count, and candidate-tree hashes reconciled without rerunning predecessors.

---

# Reference window registry

Derived from the locked aggregate tally and frozen exclusions. Counts: `{'FULL_QUALIFIED_REFERENCE': 217, 'STAGE_ERA_MATCHED_REFERENCE': 153, 'SAME_SEASON_STAGE_REFERENCE': 86}`. Ida is excluded. Window selection is outcome-blind; the paired minus-seven-day period remains the exact estimator reference.

---

# Same-estimator parity

Maximum Ida G difference: `4.1261438710193943e-13`; maximum simplex/arrival/dispatch identity error: `1.1796119636642288e-16`; tolerance: `1e-10`. Status: `PASS`.

---

# Reference G geometry

Every admitted window has a 10 by 3 aggregate matrix for J01, J10, and J11. Amplitude and three singular values are in `M7B_REFERENCE_STATISTICS.csv`; cell matrices and domain audits remain separately traceable.

---

# Restricted-model score calibration

Primary statistic: interval-valued $U_{full}$. Locked Ida interval: `(0.25073448467090204, 0.25073449467090003)`. Full-reference fit tolerances: `{'R': 217, 'pi_0_25_lower': 0.0, 'pi_0_25_upper': 0.0, 'q50': [0.054351825181001276, 0.061777760199687115], 'q75': [0.06959255197179487, 0.07448786602155397], 'q90': [0.09093290334060797, 0.09246202518188801], 'q95': [0.10488723660275912, 0.10488724660275908]}`. `U_direct`, amplitude, normalized incompatibility, and enrichment gain are secondary.

---

# Interval rank inference

|design|R|rank_lower|rank_upper|p_lower|p_upper|
|---|---|---|---|---|---|
|FULL_QUALIFIED_REFERENCE__ALL_QUALIFIED|217|1|1|0.0045871559633027525|0.0045871559633027525|
|FULL_QUALIFIED_REFERENCE__NONOVERLAPPING_PRIMARY|217|1|1|0.0045871559633027525|0.0045871559633027525|
|STAGE_ERA_MATCHED_REFERENCE__ALL_QUALIFIED|153|1|1|0.006493506493506494|0.006493506493506494|
|STAGE_ERA_MATCHED_REFERENCE__NONOVERLAPPING_PRIMARY|153|1|1|0.006493506493506494|0.006493506493506494|
|SAME_SEASON_STAGE_REFERENCE__ALL_QUALIFIED|86|1|1|0.011494252873563218|0.011494252873563218|
|SAME_SEASON_STAGE_REFERENCE__NONOVERLAPPING_PRIMARY|86|1|1|0.011494252873563218|0.011494252873563218|

The add-one fractions are empirical upper-tail fractions, not causal p-values.

---

# Epsilon 0.25 reference calibration

`epsilon=0.25` remains the prespecified M7A sensitivity boundary. Reference shares and q50/q75/q90/q95 are `REFERENCE_FIT_TOLERANCES`, not estimates of reporting error or causal bias. Primary: `{'R': 217, 'pi_0_25_lower': 0.0, 'pi_0_25_upper': 0.0, 'q50': [0.054351825181001276, 0.061777760199687115], 'q75': [0.06959255197179487, 0.07448786602155397], 'q90': [0.09093290334060797, 0.09246202518188801], 'q95': [0.10488723660275912, 0.10488724660275908]}`.

---

# Simultaneous abnormal cells

The nonoverlapping max statistic yields `{'FULL_QUALIFIED_REFERENCE': {'R': 217, 'c_0.95': 0.20939747635914793}, 'STAGE_ERA_MATCHED_REFERENCE': {'R': 153, 'c_0.95': 0.22469069558913304}, 'SAME_SEASON_STAGE_REFERENCE': {'R': 86, 'c_0.95': 0.20571914736674463}}`. Under the full-reference threshold, Ida has `9` empirically abnormal M5-primary cells. Exchangeability is not adopted, so this is an empirical simultaneous reference threshold.

---

# Structural timing placebos

Zero-padded shifts from minus four through plus four bins were frozen before outcomes. Ida alignment-advantage interval: `[-0.11373142857709367, -0.09753318737665745]`. This does not identify timing as causal.

---

# Duration-matched placebos

Three unlabeled contiguous three-bin patterns (B2-B4, B4-B6, B7-B9) preserve each aligned witness column's mass and have two transitions. Their exact feasible residuals are in `M7B_STRUCTURAL_PLACEBO_SCORES.csv`. Ida comparison: `{'best_placebo': 'UNLABELED_B4_B6', 'best_placebo_score': 0.45524170615825876, 'institutional_alignment_advantage_lower': 0.20450721148735873, 'institutional_alignment_advantage_upper': 0.20450722148735673}`. The aligned library fits better than these duration/mass alternatives, while the separate timing-shift result remains unfavorable.

---

# Estimator-consistent coverage

Coverage opened only after estimator parity and the new max-cell threshold. It is secondary.

|family|abnormal_cell_count|C_exists|C_forall|label|
|---|---|---|---|---|
|R1_S4_TWELVE_HOUR_SHIFTS|9|True|False|EXISTENTIAL_FULL_COVERAGE|
|R1_S4_REDEPLOYMENT_ANTI_LOOTING|9|False|False|NO_ADMISSIBLE_FULL_COVERAGE|
|R1_S4_CURFEW|9|False|False|NO_ADMISSIBLE_FULL_COVERAGE|

---

# Reference sensitivity

Required universe, dependence, leave-one-year-out, strict-support, emergency-adjacency, optimization-interval, and weight-normalization results are machine-readable in `M7B_SENSITIVITY_RESULTS.json`. Alternate timestamp sensitivity is not identified from the frozen timecreate aggregate tally and no substitute is inferred.

---

# Statistical interpretation

Interpretation case: `B`. The interval calibration status is `M7B_READY_FOR_EXTERNAL_STATISTICAL_REVIEW`. The defensible vocabulary is `EMPIRICAL_REFERENCE_RARITY` and `DESCRIPTIVE_REFERENCE_PATTERN`; exchangeability was not adopted.

---

# Identification boundaries

M7B does not estimate a causal effect, true demand or DV incidence, capacity, queue pressure, police performance, physical response, reporting failure, or mechanism. Public CAD topology is a reporting/administrative-observability measure. COVID-era behavior, mobility, holidays, evacuation, weather, seasonality, schema eras, and overlapping paired periods limit exchangeability.

---

# Next operational witness value of information

No acquisition starts automatically. The highest-value next evidence would be a separately authorized statistical review of interval refinement and exchangeability, followed only if justified by privacy-safe operational metadata that can discriminate observation failure from ordinary public-CAD variation.

---

# External statistical review prompt

Review the frozen reference universes, exact paired-window estimator, domain comparability, interval-valued ranks, epsilon reference tolerances, max-cell threshold, timing and duration placebos, and exchangeability register. Recompute from aggregate inputs and authority hashes; do not use result tables as numeric inputs and do not infer causality or incidence.
