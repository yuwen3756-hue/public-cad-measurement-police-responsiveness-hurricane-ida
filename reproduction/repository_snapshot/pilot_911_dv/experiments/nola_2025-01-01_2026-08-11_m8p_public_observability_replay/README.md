# BELAND-PLUS M8P public observability replay

Decision: `M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED`.

The current public architecture adds a response-time dashboard with machine-queryable model fields, including candidate en-route and multi-disposition enrichments. The official 2025/2026 raw Calls for Service schema, however, is essentially the locked 2021 schema, and the dashboard-only fields lack authoritative construction, ordering, overwrite, and history definitions. Queue, unit availability, priority-event history, and continuity/fallback states remain outside the public measurement regime.

R1 semantic firewall: current public semantic enrichment is not an M8D structural witness. B is `PARTIAL_CONTEXT`, Q is `ENDPOINT_PROXY_ONLY`, P is `ENDPOINT_ENRICHED`, and C is `SEMANTICS_QUALIFIED` at the descriptive layer; all four realized structural witness statuses remain `CLOSED`, so the current M8D regime remains $W_0$.

Start with [memo.md](memo.md). Reproducible outputs are in:

- `metadata/source_manifest.json`: URLs, retrieval times, hashes, update dates, and provenance;
- `metadata/schema_genealogy.csv`: field-level genealogy and semantic qualifications;
- `metadata/dashboard_machine_readability.json`: public model, query, and coverage findings;
- `data/processed/current_data_validity_audit.json`: 2025/2026 aggregate validity audit;
- `data/processed/m8p_results.json`: module, replay-level, identified-set, and decision results;
- `data/processed/reform_identification_crosswalk.csv`: internal-capability versus public-observability crosswalk.

The full annual CSV snapshots remain in `pilot_911_dv/source_data/`; they are not duplicated here.
