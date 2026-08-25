# R11.1 mathematical claim map

Statuses used here:

- `FORMALLY_VERIFIED`: Lean's kernel accepted the stated theorem.
- `TYPECHECKED_DEFINITION`: Lean represents the object, but no empirical or semantic truth follows.
- `EXHAUSTIVELY_ENUMERATED`: every member of a finite frozen domain was checked.
- `CERTIFICATE_VERIFIED`: an exact certificate was checked for the stated fixture.
- `TESTED_ONLY`: floating-point or artifact-level replication, not a kernel proof.
- `NOT_YET_VERIFIED_AS_STATED`: the paper statement needs an additional assumption or a narrower formulation.
- `SEMANTIC_REVIEW_REQUIRED`: institutional meaning or source binding lies outside Lean.

## 1. Measurement-admissibility layer

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Appendix `eq:observation_map`, `eq:performance_functional`, `eq:measure_identified_set` | `IdentifiedSets.IdentifiedSet` | `TYPECHECKED_DEFINITION` | Abstract state, recording, witness, and target types carry no institutional semantics. |
| Appendix `eq:witness_contraction` | `IdentifiedSets.witness_contraction` | `FORMALLY_VERIFIED` | Stronger witnesses must actually imply a subset of compatible worlds. |
| Appendix `eq:identified_diameter`--`eq:witness_sufficiency` | `IdentifiedSets.DiameterAtMost`, `Sufficient`, `diameter_at_most_mono` | `FORMALLY_VERIFIED` | The kernel uses the equivalent pairwise tolerance condition; the paper's supremum notation still requires its ordinary boundedness conventions. |
| Appendix `eq:inclusion_minimality` | `IdentifiedSets.InclusionMinimal`, `inclusion_minimal_of_deletion_tests` | `FORMALLY_VERIFIED` | Application to named institutional witnesses depends on the deletion premises. |
| Appendix `eq:witness_cost` | `IdentifiedSets.BundleCost`, `IsMinimumCost` | `TYPECHECKED_DEFINITION` | No agency cost or privacy-loss function is estimated. |
| Appendix `eq:stress_diagnostic` | Function composition represented abstractly | `TYPECHECKED_DEFINITION` | Its numerical value is covered by the frozen LP checks below. |

## 2. Public states, standardization, and stress statistic

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Main `eq:DA`; appendix `eq:Jrecord`--`eq:recordsimplex` | `PublicStates.*` | `FORMALLY_VERIFIED` | Boolean field-presence partition only. |
| Appendix `eq:marginalidentities` | Four-state algebra | `FORMALLY_VERIFIED` through the partition definitions | Does not identify physical dispatch or arrival. |
| Appendix `eq:rawshare`--`eq:standardcontrast` | `Standardization.standardizedShare`, `standardizedContrast` | `TYPECHECKED_DEFINITION` | Risk-set eligibility and reference weights require source review. |
| Appendix `eq:contrastsimplex` | `Standardization.standardized_simplex`, `standardized_contrast_sums_to_zero`, `omitted_state_determined` | `FORMALLY_VERIFIED` | Assumes common weights and within-stratum shares that sum to one. |
| Appendix `eq:contrastmarginals`, `eq:G` | Linear maps and matrix assembly | `TYPECHECKED_DEFINITION` | Dimensions and source-column bindings remain semantic checks. |
| Appendix `eq:support_entry`, `eq:envelope` | Frozen support construction | `SEMANTIC_REVIEW_REQUIRED` | The 864/610/632 chronology families and exposure inputs are external finite artifacts, not Lean primitives. |
| Appendix `eq:lp`, `eq:fullscore` | Constrained minimax program | `TYPECHECKED_DEFINITION` | The optimizer and data instance are computational objects. |
| Appendix `eq:idascore`, `eq:rankbounds`, `eq:addone`, `eq:threshold` | Frozen numerical outputs and arithmetic | `TESTED_ONLY` | No exact rational paper LP certificate exists. |

## 3. Within-disposition localization and bridge logic

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Appendix `eq:mr`--`eq:Hfactor` | `JointMass.h11`, `h01`, recovery theorems | `FORMALLY_VERIFIED` | Conditional share recovery requires positive recorded mass. |
| Main `eq:kitagawa`; appendix `eq:kitagawa_cell`, `eq:kitagawa01`, `eq:aggregatekitagawa` | `Kitagawa.*`, `JointMass.joint_mass_change_equals_kitagawa_terms` | `FORMALLY_VERIFIED` | Exact accounting identity, with no causal mediation interpretation. |
| Appendix `eq:signrestriction` and six focal sign witnesses | `CompositionOnly.*` | Algebra `FORMALLY_VERIFIED`; cell values `TESTED_ONLY` | The exclusion applies under the stated composition-only restriction. |
| Appendix order-sensitivity formulas | Same exact decomposition under alternative order | Algebra `FORMALLY_VERIFIED`; reported totals `TESTED_ONLY` | Order changes attribution, not the total contrast. |
| Main `eq:product`--`eq:hyperbola`; appendix `eq:nesting`, `eq:bridgeproduct`, `eq:productset` | `BridgeProduct.*` | `FORMALLY_VERIFIED` | Conditional on an admitted bridge and positive conditioning mass. |
| Appendix `eq:jointidentify`, `eq:frechet` | `Frechet.*` | `FORMALLY_VERIFIED` | Sharp for normalized nonnegative two-by-two tables with fixed marginals. |

## 4. Queue, priority, continuity, and regularization

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Main `eq:queue`; appendix `eq:queuefull` | `QueueFlow.total_exits_identified`, exit-split results | `FORMALLY_VERIFIED` | Operational queue universe only. |
| Appendix two-path queue witness | `QueueFlow.bridge_does_not_identify_queue_state` | `FORMALLY_VERIFIED` | Explicit observational-equivalence witness. |
| Appendix `eq:queuebounds` | `QueueFlow.empty_stock_flow_set`, `total_exit_outer_bounds` | `FORMALLY_VERIFIED` | Outer containment and infeasibility; general sharpness is not claimed. |
| Main `eq:priority_bounds`; appendix `eq:priority_history_bound` | `PriorityHistory.endpoint_probability_le_history_probability` plus endpoint completions | `FORMALLY_VERIFIED` | Ordered-history semantics must be correctly bound. |
| Appendix continuity-state equations | Product-state representation | `TYPECHECKED_DEFINITION` | Policy routes do not establish realized states. |
| Appendix regularization equations | `Regularization.*` | `FORMALLY_VERIFIED` | A unique selector can coexist with a nonsingleton feasible set. |

## 5. DV classification and performance-measure bounds

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Main `eq:dv_bounds`; appendix `eq:dv_rule_bound_appendix` | `DVClassification.*` | `FORMALLY_VERIFIED` | Sharp over completions of the declared `1/0/U` administrative rule, not verified true-DV status. |
| Main `eq:response_bounds`; appendix `eq:response_mixture_appendix`, `eq:response_bound_appendix` | `SelectionBounds.*` | `FORMALLY_VERIFIED` | Pointwise CDF bounds conditional on the declared label and observed coverage. |
| Main `eq:follow_bounds`; appendix `eq:follow_bound_appendix` | `SelectionBounds.*` | `FORMALLY_VERIFIED` | Same binary-mixture theorem; lineage and completion semantics remain external. |
| Appendix response deletion test | `WitnessDeletion.clock_marginals_do_not_identify_duration_distribution` | `FORMALLY_VERIFIED` | Finite counterexample establishes that marginal clocks do not fix pairing. |
| Appendix priority deletion test | `PriorityHistory.stable_equal_endpoint_completion`, `offsetting_equal_endpoint_completion` | `FORMALLY_VERIFIED` | Equal endpoints admit both stable and offsetting histories. |
| Appendix follow-through deletion test | `WitnessDeletion.lineage_marginals_do_not_identify_eligible_completion` | `FORMALLY_VERIFIED` | Finite counterexample establishes that marginal eligibility/completion totals do not fix linked completion. |
| Main Table 6 and appendix target-specific witness bundles | `IdentifiedSets.InclusionMinimal` plus deletion witnesses | Formal logic `FORMALLY_VERIFIED`; application `SEMANTIC_REVIEW_REQUIRED` | Qualified classification, clocks, lineage, eligibility, and completion must match the stated targets. |

## 6. Prospective model frontier and inference

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Appendix `eq:taggedunion` | `SetPropagation.TaggedUnion`, membership theorem | `FORMALLY_VERIFIED` | Shared parameter typing is abstract; model-specific coordinate semantics remain tagged in the paper. |
| Appendix reachability, viability, and `eq:pathset` | `SetPropagation.NextReachable`, membership theorem | `TYPECHECKED_DEFINITION` | No latent path is estimated. |
| Appendix 54-regime equation | `WitnessRegimes.*` and frozen JSON enumerator | `FORMALLY_VERIFIED` and `EXHAUSTIVELY_ENUMERATED` | Counts availability states, not models or mechanisms. |
| Appendix propagated confidence region | `SetPropagation.PropagatedRegion`, `true_pair_belongs_to_propagated_region` | `FORMALLY_VERIFIED` | Statistical coverage still depends on the moment-region coverage premise. |
| Appendix minimum-action and state-space equations | Selectors and prospective laws | `TYPECHECKED_DEFINITION` | No calibrated stochastic model or historical pathway probability is supplied. |

## 7. Deterministic-transform replay theorem

| R11.1 source | Formal object | Status | Boundary |
|---|---|---|---|
| Appendix `eq:deterministic_no_gain` | `DeterministicTransform.deterministic_transform_is_redundant` | Within-regime claim `FORMALLY_VERIFIED` | Adding `g(Y_raw)` to the same `Y_raw` adds no restriction. |
| Same displayed 2026-to-2021 equality | `cross_regime_equality_of_equal_base` and `determinism_alone_does_not_imply_cross_regime_equality` | `NOT_YET_VERIFIED_AS_STATED` | Cross-regime equality needs equality of the underlying feasible-world restrictions or an equivalent explicit assumption. |

## 8. Computational and semantic boundary

| Item | Status |
|---|---|
| Exact-rational checker fixture | `CERTIFICATE_VERIFIED` |
| Exact-rational paper LP certificate | `NOT_YET_VERIFIED` |
| Ida score interval and reference separation | `TESTED_ONLY` |
| Frozen 54-regime JSON domain | `EXHAUSTIVELY_ENUMERATED` |
| Institutional/source interpretation of every formal variable | `SEMANTIC_REVIEW_REQUIRED` |

The main-paper equations are restatements or applications of these appendix families. No DV-specific empirical score, rank, anomaly, or performance change is formalized because R11.1 reports none.
