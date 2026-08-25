# BELAND-PLUS M8P: current-public-data Ida observability replay

## Decision

`M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED`

The post-Ida public measurement architecture is easier to use and modestly richer, but it does not close the operational identification frontier. The current NOPD response-time model adds machine-queryable derived fields, including `Incident_To_EnRoute_Seconds` and `All Dispositions`. Neither field is defined in a public dictionary, neither has a public event-order/overwrite contract, and neither is part of the official 2025/2026 Socrata Calls for Service schema. The core annual raw schema remains the same endpoint architecture available for Ida: initial and final signal/priority, create/dispatch/arrival/close timestamps, final disposition, and self-initiation.

Accordingly, current public data would permit a somewhat more complete descriptive reconstruction of an Ida-like administrative signature, especially for presentation, response-time slicing, candidate en-route timing, and disposition multiplicity. It would not publicly reconstruct calls holding, queue state, available units, effective capacity, timestamped priority transport, callback execution, CAD uptime, or fallback continuity. No common-semantic identified set is proved to contract strictly.

This is a measurement-regime comparison. It is not a counterfactual of police behavior, a performance comparison, a capacity estimate, or an estimate of what would happen if Ida occurred today.

## 1. Retrieval and freeze

All primary evidence is official City of New Orleans, Data.NOLA, NOPD, or the public NOPD Power BI report. The complete machine-readable manifest is [`metadata/source_manifest.json`](metadata/source_manifest.json).

| Source | Official ID / surface | Retrieval UTC | Data/model date | Frozen evidence |
|---|---|---:|---:|---|
| [Calls for Service 2025](https://data.nola.gov/d/4xwx-sfte) | `4xwx-sfte` | 2026-08-11 22:29 | rows updated 2026-01-01 09:01 | 329,770 rows; CSV SHA-256 `be8416343d253e2518a16ae007568a1561ee8b511dbdef3d5465956a198ae875` |
| 2025 Socrata metadata | `4xwx-sfte` API | 2026-08-11 22:28 | view modified 2025-01-22 | metadata SHA-256 `ed9f78a6cff25bbe05aa80c7687b6ad7ac20edaa7a5bba1c6c628cc8df2aa52a` |
| 2025 attached CFS dictionary | asset `5606e2f9-612c-4736-a98c-d08dff821d57` | 2026-08-11 22:29 | attached to 2025 view | SHA-256 `29fce9d3dce085ef39b35381dab56064ec4ae8e486013163a46d1bc91721ede6` |
| [Calls for Service 2026](https://data.nola.gov/d/es9j-6y5d) | `es9j-6y5d` | 2026-08-11 22:30 | rows updated 2026-08-11 08:00 | 209,829 rows; CSV SHA-256 `c151ca38199aa53921ad1fe048ee7108f6165e8700ae459070f4c014ce614e17` |
| 2026 Socrata metadata | `es9j-6y5d` API | 2026-08-11 22:29 | view modified 2026-01-02 | metadata SHA-256 `cfdc1a6d8bd2b4747c0ecaf482a67f8c666a37135afff9133285b52e62806938` |
| 2026 attached CFS dictionary | asset `2e6b9959-4bde-45fb-971d-e65b51bf48c7` | 2026-08-11 22:30 | attached to 2026 view | SHA-256 `29fce9d3dce085ef39b35381dab56064ec4ae8e486013163a46d1bc91721ede6` |
| [NOPD public-data/dashboard directory](https://nola.gov/browse-nopd-data-public-records/) | official HTML | 2026-08-11 22:34 | live page | SHA-256 `5b712632b93e5fdd3c62ca9377ced0a09ce2a190c536493428f6940da3370465` |
| [NOPD Calls for Service Response Times](https://app.powerbigov.us/view?r=eyJrIjoiYjUzMzBjYmItNDhhYi00MmZlLTgyMjgtMDFlM2Q2MDczNWVjIiwidCI6IjA4Y2JmNDg1LTFjYjctNGEwMi05YTIxLTBkZDliNDViOWZmNyJ9) | Power BI model `1300399`; resource key `b5330cbb-48ab-42fe-8228-01e3d60735ec` | 2026-08-11 22:34-22:56 | model refresh 2026-07-17 13:33 | model SHA-256 `adfc9ac5aa27a10b2996e07a51b48b4449500d0937ba2d4a7e80a4af1c2c514b`; conceptual schema and aggregate query responses separately hashed |
| [NOPD response policy 41.4.1](https://nola.gov/nola/media/NOPD/Policies/Chapter-41-4-1-Response-to-Police-Calls_1.pdf) | revised 2025 policy | 2026-08-11 22:34 | PDF created 2026-01-29 | SHA-256 `b9c63d7b32e7ef5bf9bcff258f78ab716e22e71334e032706da15b1d725f3186` |
| [NOPD APR policy 41.4.2](https://nola.gov/nola/media/NOPD/Policies/41-4-2-Alternative-Police-Response-Effective-9-15-2024.pdf) | revised 2024 policy | 2026-08-11 22:34 | revised 2024-09-15 | SHA-256 `687327bea8407df526902cf72749635e8a6ae94772748fad9715392a75c7177e` |
| [NOPD Sustainment Plan](https://nola.gov/nola/media/NOPD/Consent%20Decree/NOPD%20Audits/Sustainment-Plan-%28Ref-Doc-793-1%29-9-27-2024.pdf) | public reform document | 2026-08-11 22:34 | 2024-09-27 | SHA-256 `bc8b7ab7e5a717161cc76c3de8c276c66a9a9dc351da0221e6c40150963facd3`; used only as commitment/context, not as public data |
| [Electronic Police Report 2025](https://data.nola.gov/d/agqi-9adb) | `agqi-9adb` metadata/columns | 2026-08-11 22:39 | current annual view | metadata SHA-256 `32ab72d7a3f0fbeb0a5018b148f201bfad7ccfddb8e0c69675d8a9445766abf4` |

The official directory labels “Calls for Service and Crime Trends” as a management dashboard, but its link resolves to the third-party Community Crime Map. That interface was not treated as an official primary-data source, and no City/NOPD bulk data underlying it was verified. Dashboard existence is therefore not treated as downloadability.

The response-time dashboard is different: its public semantic model and `querydata` endpoint are machine-readable. Aggregate queries were reproduced and frozen. A direct bulk CSV/download endpoint was not verified.

The official Socrata catalog query returned EPR annual datasets through 2025 and the 2026 CFS dataset, but no catalog-listed EPR 2026 dataset as of retrieval. This is a current-publication finding, not proof that no later 2026 EPR will appear.

## 2. Frozen comparison universes

The comparison holds the locked Ida public topology and decomposition fixed:

- 2021 CFS endpoint `3pha-hum9`, including initial/final signal and priority endpoints, create/dispatch/arrival/close, final disposition, and self-initiation;
- the locked eight-state public administrative topology $K_{dac}$ from M7D-C;
- the locked within-disposition dispatch-field decomposition from M7D-E;
- the locked public CAD-EPR item bridge using 2021 EPR endpoint `6pqh-bfxa`;
- the M7D-A operational frontier, where all ten broad mechanism families remain feasible and Tier 1 witnesses are system uptime, calls holding, unit availability, and initial-to-qualified-endpoint priority transitions.

Nothing in M8P re-estimates the Ida signature, alters the M7D decomposition, assigns mechanism probabilities, or reinterprets arrival/closure as physical service or effective capacity.

## 3. Schema genealogy

The complete field-level genealogy is [`metadata/schema_genealogy.csv`](metadata/schema_genealogy.csv). Its main findings are:

1. **Raw annual schema continuity.** The same core 16 public fields are present in 2021, 2025, and 2026. The current Socrata dictionaries for 2025 and 2026 are byte-identical.
2. **Storage-type drift, not new measurement.** `TimeCreate`, `TimeDispatch`, `TimeArrive`, and `TimeClosed` were Socrata `calendar_date` fields in the locked 2021 metadata but are `text` in 2025/2026. `PoliceDistrict` changed from `number` to `text`. All current nonblank stage timestamps nevertheless parsed as ISO timestamps in the audit.
3. **Endpoint architecture persists.** Initial/final signal and priority remain paired endpoints. Public sources do not document transition timestamps, actors, reasons, version multiplicity, or overwrite history.
4. **Dashboard-only enrichments.** The public model adds derived stage durations, priority/signal change flags, modifying-circumstance categories, source detail, and `All Dispositions`. These are not in the Socrata dictionaries.
5. **Candidate en-route field.** `Incident_To_EnRoute_Seconds` is machine-queryable. The aggregate response contains non-null value groups and a 142,468-row blank group across the 848,799 modeled calls, but the field is absent from all current report visuals and no official public definition of its clocks or exclusions was located.
6. **Candidate disposition multiplicity.** `All Dispositions` is machine-queryable and contains single, repeated, and mixed comma-delimited codes. Public evidence does not establish whether order is chronological, whether repeats are distinct events, or whether the field is a current warehouse concatenation.
7. **Persistent structural absence.** No public field was located for calls holding, queue state, available units, unit status, effective capacity, callback execution, CAD uptime, failover, or manual-mode continuity.

The dashboard model covers 2023-2026, not Ida 2021. Its counted universe is not a transparent copy of the annual raw files. For 2025 it reports 233,319 “Not Officer Initiated” calls, while the raw file has 329,770 total rows and 207,050 `SelfInitiated=N` rows. For 2026 it reports 127,551 modeled calls at a July 17 refresh versus 209,829 raw rows and 130,346 `SelfInitiated=N` rows in the August 11 snapshot. The 2026 gap partly reflects refresh timing; the 2025 discrepancy remains unexplained publicly. This blocks a lossless public universe crosswalk.

## 4. M8 public-evidence module crosswalk

This crosswalk has two deliberately separate layers. **Public semantic enrichment** describes what the current public architecture makes easier to label, query, or compare. **M8D structural witness status** asks whether the public evidence supplies the realized retained state/history required to open a structural module. The first layer must not be promoted into the second.

| Module | Public semantic enrichment | M8D structural witness | Public evidence and remaining boundary |
|---|---|---|---|
| B - internal/public bridge | `PARTIAL_CONTEXT` | `CLOSED` | The 2025 CFS-EPR item link supplies downstream public-record context. It is not the M8 bridge $U_{dispatch}\to D_{pub}$, and no public internal-event/public-export transformation or reconciliation is available. |
| Q - queue and realized availability | `ENDPOINT_PROXY_ONLY` | `CLOSED` | Public stage endpoints and response-time derivatives describe realized public records. They do not construct a queue reachable set and expose no calls-holding, queue-stock, wait-state, available-unit, unit-status, staffing, or effective-capacity witness. |
| P - priority transport | `ENDPOINT_ENRICHED` | `CLOSED` | Initial/final priority, suffix semantics, modifiers, and a change flag enrich endpoint interpretation. No timestamped transition path, actor, reason, multiplicity, or event history is public, and no formal `PARTIAL_OUTER` set is proved. |
| C - continuity/fallback | `SEMANTICS_QUALIFIED` | `CLOSED` | Policies define possible APR, callback, and fallback routes. No realized route, callback completion, uptime, outage, failover, manual-mode, or continuity state is public. |

The realized M8D witness regime therefore remains $W_0=(CLOSED,CLOSED,CLOSED,CLOSED)$. Public enrichment does not open a B, Q, P, or C structural witness.

The current response policy defines suffixes as within-code ordering and states that pending calls are dispatched by priority/sub-priority rather than receipt time (41.4.1, p. 2). It also describes a return to the dispatch queue under the original item number (p. 5). Those facts clarify current semantics but do not expose a queue dataset. Likewise, the APR policy describes district handling when APR personnel are unavailable (41.4.2, p. 3) and callback rules (p. 5), but it does not publish realized callback or fallback states.

## 5. Ida observability replay

| Level | Result | Replay finding |
|---|---|---|
| L1 public-topology detection | `PUBLICLY_IDENTIFIABLE` | The locked create/dispatch/arrival/close topology remains directly reconstructible. This was already true in 2021. |
| L2 within-disposition/stage localization | `PARTIALLY_IDENTIFIABLE` | Current public data can still localize endpoint-stage patterns and adds candidate en-route and multi-disposition fields. Their construction, ordering, and history remain unqualified. |
| L3 internal/public bridge separation | `PARTIALLY_IDENTIFIABLE` | Public raw, dashboard, and 2025 EPR surfaces can be separated and compared, but the internal transformation and 2026 EPR bridge are missing. |
| L4 queue/availability reconstruction | `NOT_PUBLICLY_IDENTIFIABLE` | Response time and missing dispatch fields do not identify calls holding, queue length, available units, or effective capacity. |
| L5 priority-history reconstruction | `PARTIALLY_IDENTIFIABLE` | Current suffix documentation, modifiers, and dashboard flags make endpoint contrasts easier to interpret. The 2021 public schema already contained both endpoints, and no transition history is public. |
| L6 continuity/fallback reconstruction | `NOT_PUBLICLY_IDENTIFIABLE` | Policy documents route possibilities; realized callback, uptime, failure, and fallback states are not public. |
| L7 cross-module propagation | `PARTIALLY_IDENTIFIABLE` | Public stage, priority, disposition, and 2025 EPR endpoints can be cross-tabulated. A full B-Q-P-C propagation path cannot be reconstructed because Q state and C state are absent. |

The ambiguities that become smaller are therefore narrow: how current priority suffixes are supposed to order calls; whether an initial/final priority or signal endpoint differs; whether a modeled incident carries an en-route-duration value; and whether the model holds multiple disposition codes. The larger latent ambiguities do not become smaller: why priority changed, when it changed, how many operational transitions occurred, how long the call waited before a resource was available, whether a unit was effectively available, whether a callback/fallback occurred, and whether system continuity failed.

## 6. Identified-set comparison

Let $Y_{21}$ be the locked 2021 public endpoint topology and let $Y_{26}^{raw}$ be the same normalized fields in the current annual schema. Let $D_{26}^{derived}=g(Y_{26}^{raw})$ denote dashboard fields that are deterministic endpoint transformations, such as response durations and initial-versus-final change flags.

Conditional on a maintained, frozen common-semantic mapping between the shared endpoints, for any common parameter $\theta$ whose public restrictions depend only on those endpoints,

$$
\mathcal I_{2026}(\theta \mid Y_{Ida}, Y_{26}^{raw}, D_{26}^{derived})
=
\mathcal I_{2021}(\theta \mid Y_{Ida}, Y_{21}),
$$

after datatype and label normalization, because adding $g(Y)$ does not add information beyond $Y$. Without that maintained semantic mapping, equality is not asserted.

For queue, effective availability, priority-event history, callback/fallback, or system-continuity parameters, no public field adds the missing state variable. Strict containment is therefore not proved:

$$
\mathcal I_{2026}(\theta \mid Y_{Ida})
\subsetneq
\mathcal I_{2021}(\theta \mid Y_{Ida})
$$

is **not established** for any of those mechanism-relevant $\theta$.

The model-only fields `Incident_To_EnRoute_Seconds` and `All Dispositions` are genuine public query surfaces, but they do not yet prove strict contraction for a common Ida estimand. A strict comparison requires an authoritative semantic map specifying clocks, ordering, multiplicity, missingness, and overwrite/history behavior. The field names and observed aggregate values alone do not supply that map.

**Strict contractions proved: none.** No mechanism probabilities are assigned.

## 7. Current-data validity audit

The audit uses only annual 2025/2026 public data and performs no event-window, shock, DV-outcome, or anomaly fishing. Full results are in [`data/processed/current_data_validity_audit.json`](data/processed/current_data_validity_audit.json), [`data/processed/field_completeness.csv`](data/processed/field_completeness.csv), and [`data/processed/monthly_quality.csv`](data/processed/monthly_quality.csv).

| Check | 2025 | 2026 through retrieval | Interpretation |
|---|---:|---:|---|
| Rows / unique item IDs | 329,770 / 329,770 | 209,829 / 209,829 | No duplicate public item rows in either snapshot. |
| Malformed nonblank stage timestamps | 0 | 0 | Text-typed timestamps were parseable. |
| `TimeDispatch` nonmissing | 41.7955% | 41.8755% | Overall dispatch-field missingness remains large and structurally tied to initiation/status conventions. |
| `TimeArrive` nonmissing | 83.7199% | 84.1447% | Arrival is incomplete; it is not a capacity measure. |
| Non-self-initiated dispatch nonmissing | 66.0285% | 66.8444% | Restricting initiation changes the denominator but does not make dispatch complete. |
| Non-self-initiated arrival nonmissing | 74.1715% | 74.5899% | The dashboard’s apparent non-officer-initiated universe still requires explicit missingness treatment. |
| Arrival present while dispatch absent | 152,701 | 97,573 | Sequence-field noncooccurrence persists; it is not proof of an operational sequence violation. |
| Arrival before dispatch | 1,049 | 676 | Small but nonzero recorded chronology inconsistencies. |
| Closed before create | 292 | 62 | Small but nonzero chronology inconsistencies. |
| Initial/final priority complete | 100% / 100% | 100% / 100% | Endpoints are available, not histories. |
| Exact initial/final priority disagreement | 127,769 (38.7449%) | 77,850 (37.1016%) | Includes numeric and suffix changes; endpoint disagreement is not transition history. |
| Numeric-root priority disagreement | 76,904 (23.3205%) | 50,693 (24.1592%) | Root-code endpoint contrast only. |
| Values outside documented root 0-3 | 7 initial; 5 final | 2 initial; 0 final | Very rare schema/value anomalies remain. |
| Initial/final signal-code disagreement | 86,054 (26.0952%) | 53,139 (25.3249%) | Signal endpoint contrast only. |

Year-to-year raw headers are identical. There are 209 common final signal codes; 208 retain the same privacy-safe code-to-description hash set across years. The 2025 share using a code also observed in 2026 is 99.9918%; the 2026 share using a code observed in 2025 is 99.8332%. This is high but not perfect semantic stability.

The locked 2021 annual audit had 75.4533% dispatch coverage and 86.9061% arrival coverage overall; August 2021 dispatch coverage was 46.5078%. These rates are descriptive properties of different annual populations and conventions, not direct performance comparisons. They show why public endpoint completeness must be audited rather than inferred from field presence.

Modern public CFS therefore still contains many arrival-present/dispatch-absent configurations. That persistence reinforces the paper's interpretation of the topology as administrative observability, not physical nonresponse.

The dashboard reports 112,894 priority-change calls among 233,319 modeled 2025 calls and 59,929 among 127,551 modeled 2026 calls at its July refresh. Those shares do not equal the raw annual endpoint-disagreement shares because the dashboard universe, refresh date, and transformation rules differ. Without a public reconciliation rule, the dashboard is not a drop-in replacement for the raw public universe.

## 8. Reform identification crosswalk

The full crosswalk is [`data/processed/reform_identification_crosswalk.csv`](data/processed/reform_identification_crosswalk.csv).

| CURRENT_REFORM_OBJECT | PUBLICLY_OBSERVABLE_NOW | IDA_2021_OBSERVABLE | IDENTIFICATION_GAIN | REMAINING_GAP |
|---|---|---|---|---|
| Initial/final priority dashboard | Yes: visible and aggregate-queryable. | Both raw endpoints already public. | Presentation/reproducibility, not history. | Transition time, actor, reason, multiplicity, raw/dashboard reconciliation. |
| Sub-priority and supervisor modification | Current policy and endpoints. | Endpoint fields existed. | Better current semantic documentation. | Reasons-over-air record and transition sequence. |
| Real-time supervisory CAD access | Not public as data. | Not public. | None for public research. | Calls holding, priority transitions, officer availability, effective capacity. |
| APR/fallback routing | Route menu documented in policy. | Realized route not public. | Semantic only. | Realized assignment, transfer, callback, and failure state. |
| GOA/DV callbacks | Required by policy, not observed. | Final disposition only. | None for realized continuity. | Attempt, completion, timing, outcome, responsible unit. |
| En-route stage | Queryable model field, undocumented. | Absent. | Candidate partial stage localization. | Common definition, clocks, missingness, universe, history. |
| All dispositions | Queryable model combinations. | Final endpoint only. | Candidate multiplicity enrichment. | Ordering, timestamps, repeats, construction. |
| CFS-EPR bridge | 2025 yes; 2026 not catalog-listed. | 2021 yes. | No stable current-year gain. | 2026 publication and version timing. |

The Sustainment Plan’s pages 24-26 describe reforms including restored modifiers, a public response-time dashboard, real-time supervisor access to calls holding and officer availability, and possible DV callbacks. The dashboard’s existence is verified as a current public surface. The other statements remain internal-capability commitments or policy context unless and until their realized states are published. They are not treated as current public data.

## 9. Decision rationale

`M8P_PUBLIC_OBSERVABILITY_MATERIALLY_IMPROVED` is too strong because the decisive M7D witnesses remain absent and no strict common-estimand contraction is proved.

`M8P_NO_MATERIAL_MEASUREMENT_REGIME_CHANGE` is too weak because the public response-time semantic model is a real additional measurement surface and contains candidate stage/multiplicity fields not present in the locked 2021 raw schema.

`M8P_INTERNAL_CAPABILITY_IMPROVED_PUBLIC_BOUNDARY_REMAINS` would require converting public commitments and workflow documents into a verified current internal-capability result. M8P does not do that.

The supported decision is therefore:

**`M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED`**

Scientific disposition after R1 semantic-firewall repair: `M8P_SCIENTIFIC_CORE_LOCKED`. The empirical data, hashes, current-data audit, L1-L7 replay results, decision, and finding that strict contractions proved are none remain unchanged.

## 10. Claim firewall

This memo does not say or imply that:

- current reforms prevent another Ida;
- current police performance is better;
- the 2026 system would respond better;
- Ida would have had a different outcome;
- public assignment or arrival proves physical service;
- recorded availability proves effective capacity;
- a priority endpoint disagreement proves a transport history;
- a policy commitment proves realized public data;
- any mechanism has a probability assigned by this replay.

The supported claim is narrower: current public data permit a somewhat richer and more convenient administrative reconstruction, but the mechanism-relevant identified sets are not proved to contract because queue, availability, priority history, and continuity/fallback remain outside the public architecture.
