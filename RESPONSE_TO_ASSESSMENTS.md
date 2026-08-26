# R16.2 external-relevance implementation crosswalk

Paper R16.2 implements the public framing and external-relevance requirements while preserving the validated R15.1 scientific evidence. R16.1 remains the exact predecessor at commit `7d2654525609c2e8eda6580d2572f6db0699fadd`; review files remain evidence and advice rather than independent scientific authority.

| R16.2 requirement | Public implementation |
|---|---|
| Explain why environmental stress can affect both service production and observation | Adds a concise introduction paragraph separating demand, supply, prioritization, endpoint coverage, and observation-layer change. |
| Connect to environmental-stress and first-responder research | Adds a related-literature paragraph framing stable administrative outcomes as a prerequisite that complements substantive estimates. |
| Strengthen publication relevance without criticism | Uses supportive language centered on construct validity, interpretation, reproducibility, and low-cost diagnostics. |
| Make downstream uses concrete | Adds a four-row table for call volume, response time, priority split, and police activity or coverage. |
| State low-cost validation checks | Requires declared initiation rules, duplicate and cancellation treatment, response-clock definitions, endpoint coverage, priority transitions, and schema continuity. |
| Keep reported DV proportionate | Retains one short downstream paragraph in the main paper; detailed $1/0/U$ bounds remain in the supplement. |
| Extend the conclusion | Applies the validation logic to heat, smoke, pollution, outages, disasters, police-service demand, and responsiveness. |
| Preserve scientific results | Leaves every `r15*` source object and the reproduction snapshot unchanged and retains Scientific Results R15.1. |
| Keep the legacy archive separate | Builds the combined reviewer PDF from the main paper and empirical supplement only. |
| Enforce public/private separation | The verifier checks the public sources, documents, PDFs, manifest scope, and release ZIP inputs for private-only markers. |

## Version and evidence boundary

- Paper version: R16.2.
- Scientific-results version: R15.1.
- Predecessor: R16.1 commit `7d2654525609c2e8eda6580d2572f6db0699fadd`.
- All empirical CSV/JSON objects and the inherited reproduction snapshot remain unchanged.
- The main result remains descriptive: the 53.2-percentage-point largest change is larger than all 151 post-change ordinary-week references.
- The package does not identify a causal effect, physical dispatch or arrival, police performance, effective capacity, a unique mechanism, true domestic-violence incidence, or an Ida-specific DV effect.
