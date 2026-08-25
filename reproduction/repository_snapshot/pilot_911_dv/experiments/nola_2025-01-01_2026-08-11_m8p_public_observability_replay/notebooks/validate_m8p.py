from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.reader(handle)) - 1


def main() -> None:
    checks: list[dict] = []

    def check(name: str, passed: bool, evidence) -> None:
        checks.append({"name": name, "passed": bool(passed), "evidence": evidence})

    sources = {
        "2025": ROOT
        / "pilot_911_dv/source_data/socrata/nola_4xwx-sfte/2025/m8p_public_snapshot_2026-08-11/calls_for_service_2025.csv",
        "2026": ROOT
        / "pilot_911_dv/source_data/socrata/nola_es9j-6y5d/2026/m8p_public_snapshot_2026-08-11/calls_for_service_2026.csv",
    }
    expected = {
        "2025": (329770, "be8416343d253e2518a16ae007568a1561ee8b511dbdef3d5465956a198ae875"),
        "2026": (209829, "c151ca38199aa53921ad1fe048ee7108f6165e8700ae459070f4c014ce614e17"),
    }
    for year, path in sources.items():
        rows = csv_rows(path)
        digest = sha256(path)
        check(
            f"{year}_csv_frozen",
            (rows, digest) == expected[year],
            {"rows": rows, "sha256": digest},
        )

    manifest = json.loads((EXP / "metadata/source_manifest.json").read_text(encoding="utf-8"))
    dataset_ids = {row.get("dataset_id") for row in manifest["sources"]}
    check("required_cfs_dataset_ids", {"4xwx-sfte", "es9j-6y5d"} <= dataset_ids, sorted(x for x in dataset_ids if x))
    check(
        "manifest_hash_shapes",
        all(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) for row in manifest["sources"]),
        len(manifest["sources"]),
    )

    audit = json.loads((EXP / "data/processed/current_data_validity_audit.json").read_text(encoding="utf-8"))
    check("audit_row_counts", audit["years"]["2025"]["rows"] == 329770 and audit["years"]["2026"]["rows"] == 209829, {year: audit["years"][year]["rows"] for year in ("2025", "2026")})
    check("no_malformed_timestamps", all(not audit["years"][year]["malformed_timestamps"] for year in ("2025", "2026")), {year: audit["years"][year]["malformed_timestamps"] for year in ("2025", "2026")})

    dashboard = json.loads((EXP / "metadata/dashboard_machine_readability.json").read_text(encoding="utf-8"))
    check("dashboard_public_query_verified", dashboard["machine_readable_public_query_endpoint_verified"], dashboard["public_report_url"])
    check("dashboard_enroute_query_verified", dashboard["enroute_seconds_property_query_verified"], dashboard["enroute_probe_note"])
    check("dashboard_enroute_not_overclaimed", not dashboard["enroute_seconds_public_semantics_documented"] and not dashboard["enroute_seconds_property_in_current_report_visuals"], "queryable but undocumented and absent from visuals")
    check("dashboard_no_queue_capacity_fields", not dashboard["queue_availability_continuity_callback_properties"], dashboard["queue_availability_continuity_callback_properties"])

    results = json.loads((EXP / "data/processed/m8p_results.json").read_text(encoding="utf-8"))
    allowed_decisions = {
        "M8P_PUBLIC_OBSERVABILITY_MATERIALLY_IMPROVED",
        "M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED",
        "M8P_INTERNAL_CAPABILITY_IMPROVED_PUBLIC_BOUNDARY_REMAINS",
        "M8P_NO_MATERIAL_MEASUREMENT_REGIME_CHANGE",
        "M8P_BLOCKED_BY_CURRENT_SCHEMA_AMBIGUITY",
    }
    check("decision_enum", results["decision"] in allowed_decisions, results["decision"])
    check("strict_contraction_firewall", results["identified_set_comparison"]["strict_contractions_proved"] == [], results["identified_set_comparison"]["strict_contractions_proved"])
    module_firewall = results["module_crosswalk_semantic_firewall"]
    check(
        "module_semantic_statuses",
        {row["public_semantic_enrichment"] for row in module_firewall.values()}
        == {"PARTIAL_CONTEXT", "ENDPOINT_PROXY_ONLY", "ENDPOINT_ENRICHED", "SEMANTICS_QUALIFIED"},
        module_firewall,
    )
    check(
        "module_structural_statuses",
        {row["m8d_structural_witness_status"] for row in module_firewall.values()} == {"CLOSED"},
        module_firewall,
    )
    check(
        "m8d_realized_witness_regime",
        results["m8d_realized_witness_regime"]["regime"] == "W_0"
        and results["m8d_realized_witness_regime"]["tuple"] == ["CLOSED"] * 4,
        results["m8d_realized_witness_regime"],
    )
    check(
        "identified_set_common_semantic_condition",
        "Conditional on a maintained frozen common-semantic mapping" in results["identified_set_comparison"]["common_observable_endpoint_parameters"],
        results["identified_set_comparison"]["common_observable_endpoint_parameters"],
    )
    check("replay_statuses", {row["status"] for row in results["ida_observability_replay"].values()} <= {"PUBLICLY_IDENTIFIABLE", "PARTIALLY_IDENTIFIABLE", "NOT_PUBLICLY_IDENTIFIABLE", "UNKNOWN"}, results["ida_observability_replay"])

    with (EXP / "metadata/schema_genealogy.csv").open("r", encoding="utf-8", newline="") as handle:
        genealogy = list(csv.DictReader(handle))
    required_columns = {
        "label",
        "machine_field",
        "datatype_2021",
        "datatype_2025",
        "datatype_2026",
        "present_2021",
        "present_2025",
        "present_2026",
        "row_level_vs_aggregate",
        "endpoint_vs_event_history",
        "multiplicity",
        "overwrite_history_behavior",
        "missingness_2021",
        "missingness_2025",
        "missingness_2026",
        "semantic_continuity",
        "authority_source",
    }
    check("schema_genealogy_columns", required_columns <= set(genealogy[0]), sorted(genealogy[0]))
    check("schema_genealogy_scope", len(genealogy) >= 30, len(genealogy))

    markdown_files = [EXP / "README.md", EXP / "memo.md", EXP / "validation.md"]
    forbidden = {}
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        hits = [token for token in (r"\(", r"\)", r"\[", r"\]") if token in text]
        if hits:
            forbidden[str(path)] = hits
    check("obsidian_math_delimiters", not forbidden, forbidden)

    report = {
        "validation_version": "m8p_focused_validation_v1",
        "status": "PASS" if all(row["passed"] for row in checks) else "FAIL",
        "checks": checks,
    }
    (EXP / "metadata/validation_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps({"status": report["status"], "checks": len(checks), "failed": [row["name"] for row in checks if not row["passed"]]}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
