# R16.2 changelog

Release date: 26 August 2026  
Paper version: R16.2  
Scientific-results version: R15.1  
Predecessor: R16.1 commit `7d2654525609c2e8eda6580d2572f6db0699fadd`

## Public-paper revision

- Adds an introduction bridge explaining that environmental stress can affect both police-service production and the administrative observation process.
- Adds a related-literature bridge positioning stable administrative outcomes as a prerequisite that complements substantive environmental-stress estimates.
- Renames the implications section around validation of police-service measures under environmental and system stress.
- Adds a four-row validation table for call volume, response time, priority split, and police activity or coverage.
- Makes denominator, initiation-stream, response-clock, endpoint-coverage, priority-definition, schema-continuity, and data-lineage checks explicit.
- Keeps reported DV as a short downstream application; the supplement retains the corresponding classification and missing-data bounds.
- Extends the conclusion to heat, smoke, pollution, outages, disasters, police-service demand, and responsiveness.

## Reviewer precision follow-up

- Rewrites the four-state definition table so every final-column entry completes the heading ``What the label does not establish.''
- Narrows the officer-stream inference to a changed mapping from officer-initiated activity to the released record, without locating the change in workflow, entry, retention, transformation, or export.
- Separates call-volume and response-time pathways, splits the Ida chronology into two stages, and moves the pre-break Cristobal discussion back to the supplement.
- Replaces publication-oriented table language with interpretive language, uses documented initiation streams, and clarifies the response-clock endpoints.
- Marks which validation checks are directly motivated by the New Orleans evidence and which are adjacent methodological extensions.
- Adds direct published sources on heat and law enforcement, heat-related 911 medical dispatch, and continuity of essential information systems; no seminar material is cited.

## Package revision

- Advances all current paper, supplement, status-note, bibliography, metadata, and legacy-archive filenames to R16.2.
- Updates the five-PDF build, release verifier, manifest builder, and ZIP builder.
- Adds verifier checks for the required environmental-stress language, forbidden critical language, frozen R15.1 hashes, page and abstract limits, legacy separation, and public/private separation.
- Updates the reviewer-facing documentation and version declarations.

## Frozen boundary

- Every `source/r15*` object remains byte-identical to R16.1.
- The complete `reproduction/repository_snapshot/` tree remains unchanged.
- No result, numerical claim, scientific-results label, causal boundary, physical-response boundary, performance boundary, capacity boundary, mechanism boundary, or reported-DV incidence boundary is promoted or changed.
