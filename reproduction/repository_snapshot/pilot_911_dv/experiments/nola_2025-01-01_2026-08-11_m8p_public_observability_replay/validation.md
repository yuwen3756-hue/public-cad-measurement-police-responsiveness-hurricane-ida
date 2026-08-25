# Validation

Status: `PASS` - focused validation, 0 failures.

The validation scope is limited to this M8P experiment: source-manifest hashes, annual CSV row counts and parsing, machine-readable output schemas, decision/status vocabulary, absence of persisted incident examples, and Obsidian Markdown math delimiters. It does not validate police performance, internal capability, capacity, causal effects, or a behavioral counterfactual.

Verified:

- 2025 snapshot: 329,770 rows and SHA-256 `be8416343d253e2518a16ae007568a1561ee8b511dbdef3d5465956a198ae875`;
- 2026 snapshot: 209,829 rows and SHA-256 `c151ca38199aa53921ad1fe048ee7108f6165e8700ae459070f4c014ce614e17`;
- zero malformed nonblank stage timestamps in both annual snapshots;
- required source-manifest, genealogy, two-layer module-firewall, $W_0$, replay-level, decision, and claim-firewall structures;
- public aggregate queryability of the dashboard model and candidate en-route field;
- no dashboard fields named for queue, availability, unit status, callback, uptime, or fallback;
- no forbidden Obsidian math delimiters in the touched Markdown files.

Machine-readable evidence: `metadata/validation_report.json`.

R1 changed semantic classification and reporting only. It did not rerun or alter the annual snapshots, source manifest, schema genealogy, current-data validity audit, field-completeness table, monthly-quality table, L1-L7 replay results, or decision. Exact protected hashes are recorded in `M8P_R1_LOCK_RECEIPT.json`.

Project-memory note: the full memory-integrity checker returned `findings_present` for 29 pre-existing missing wiki-link targets in older notes. None references the new M8P milestone. A scoped check of the touched knowledge graph, index, and M8P milestone confirmed the target exists, both new links resolve, and no forbidden math delimiters were introduced. The older link debt is nonblocking and was not repaired in this scientific task.
