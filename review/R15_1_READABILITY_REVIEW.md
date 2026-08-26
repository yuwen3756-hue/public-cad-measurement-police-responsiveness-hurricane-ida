# R15.1 Readability Review

## Verdict

The scientific content is now substantially stronger than in earlier versions, but the main paper is still difficult to read because it presents the audit trail and the empirical story at the same level. A reader encounters four different comparison designs, support rules, post-hoc status, bootstrap dependence caveats, alternating-window sensitivities, eight legacy statistics, disposition accounting, institutional exclusions, contemporary denominator arithmetic, and DV bounds before the paper has settled on one memorable answer.

The core paper should be easy to summarize in four sentences:

1. The public field convention changes abruptly on 28 July 2021.
2. Ida produces a second, temporary change inside the new regime.
3. The Ida change is larger than every later ordinary-week comparison.
4. The public data do not identify physical response or the institutional mechanism.

Everything else should support one of those sentences or move to the empirical supplement.

## Why R15.1 is hard to follow

### 1. The abstract is a methods inventory

The abstract contains the object definition, July break, officer stream, Ida, two reference designs, common-support failure, conditional bootstrap, institutional exclusions, and causal boundaries. The reader has no hierarchy for these facts.

### 2. The introduction repeats the same distinction four times

The paper says that public fields are not operational events in the opening paragraph, the next paragraph, two equations, the July paragraph, the contribution list, and the result box. Repetition consumes attention without improving understanding.

### 3. The paper explains the estimator before showing the event

Readers meet the 10×3 matrix, three reference universes, the 0.90 gate, inherited stage membership, and a post-hoc universe before seeing the simple daily Ida path. The daily path should come first.

### 4. The main results section has too many branches

The results move from standardized rank to full-count rank, bootstrap rank, alternating references, the daily figure, post-Ida, Francine, support coverage, threshold sensitivity, eight secondary statistics, the LP, the timing placebo, Kitagawa accounting, and initiation streams. This reads like a response memo rather than a paper.

### 5. Technical labels obscure intuitive quantities

Terms such as `J01`, `M_max`, `stage-era`, `support-independent`, `common-support`, `U_direct`, `U_full`, `Q`, and `D` appear before the reader has a stable verbal picture. The main text should use “arrival only,” “both fields,” and “largest percentage-point change.” Formal labels belong in the supplement.

### 6. The paper treats robustness checks as co-equal findings

The full-count post-change comparison should be primary. The standardized comparison, alternating references, threshold variants, secondary statistics, LP score, and timing placebo should be summarized briefly and documented in the supplement.

### 7. The literature is now adequate but overly segmented

Four short subsections make the section feel like annotated notes. A single flowing section with a final contribution paragraph is easier to read.

### 8. The DV section remains too mathematical for its role

The main paper does not estimate a DV quantity. A short table stating what is directly observed, selected, or unavailable is more useful than a prevalence-bound equation.

## Recommended main-paper hierarchy

1. Introduction: one question and three findings.
2. Data: two fields, four plain-language configurations, one denominator.
3. July 28 break: raw audit plus long-run figure.
4. Ida: daily path first.
5. Comparison: one primary full-count statistic; standardized analysis as secondary.
6. Interpretation: officer-stream clue, disposition accounting, institutional evidence.
7. Implications: response-time and DV measurement in one table.
8. Limitations and conclusion.

## Material to move out of the main paper

- the eight-statistic table;
- the LP threshold margin and interval-width discussion;
- threshold counts of 9/8/9;
- alternating reference phases;
- detailed bootstrap construction;
- full common-support table;
- full institutional source-status table;
- formulas for DV classification bounds;
- all historical support-library and formal-verification material.

## Editorial rules for the rewrite

- Use “arrival-only configuration,” not `J01`, after the definition table.
- Report 0.532 as “53.2 percentage points.”
- Say “larger than all 151 reference windows,” not “rank 1/152 including Ida.”
- Introduce the daily Ida figure before the ranking design.
- State one primary design and label all others as secondary.
- Use no more than two equations in the main paper.
- Keep the abstract below 190 words.
- Keep the conclusion below 250 words.
- Every paragraph should answer one question.
