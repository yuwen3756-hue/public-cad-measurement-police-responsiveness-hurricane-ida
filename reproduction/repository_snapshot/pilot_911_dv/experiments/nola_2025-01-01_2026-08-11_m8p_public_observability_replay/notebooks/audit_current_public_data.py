from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PROCESSED = EXP / "data" / "processed"
METADATA = EXP / "metadata"

DATASETS = {
    2025: {
        "id": "4xwx-sfte",
        "dir": ROOT
        / "pilot_911_dv/source_data/socrata/nola_4xwx-sfte/2025/m8p_public_snapshot_2026-08-11",
    },
    2026: {
        "id": "es9j-6y5d",
        "dir": ROOT
        / "pilot_911_dv/source_data/socrata/nola_es9j-6y5d/2026/m8p_public_snapshot_2026-08-11",
    },
}

CURRENT_SOURCES = (
    ROOT
    / "pilot_911_dv/source_data/official_event_context/nopd_current_public_architecture/2026-08-11"
)
LOCKED_2021_METADATA = (
    ROOT
    / "pilot_911_dv/briefings/webai_context_packs/2026-07-15_path_e8_completion_webai_pack_v1/official_sources/data_nola_calls_for_service_2021_metadata.json"
)

TIMESTAMP_FIELDS = ("TimeCreate", "TimeDispatch", "TimeArrive", "TimeClosed")
RELEVANT_FIELDS = (
    "NOPD_Item",
    "Type",
    "TypeText",
    "Priority",
    "InitialType",
    "InitialTypeText",
    "InitialPriority",
    "TimeCreate",
    "TimeDispatch",
    "TimeArrive",
    "TimeClosed",
    "Disposition",
    "DispositionText",
    "SelfInitiated",
    "Beat",
    "PoliceDistrict",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def hash_text(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value.strip().casefold())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def parse_timestamp(value: str):
    if not value:
        return None, False
    try:
        return datetime.fromisoformat(value), False
    except ValueError:
        return None, True


def epoch_iso(value):
    if value is None:
        return None
    return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")


def file_retrieved_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )


def audit_dataset(year: int, spec: dict):
    csv_path = spec["dir"] / f"calls_for_service_{year}.csv"
    missing = Counter()
    distinct = {field: set() for field in ("Priority", "InitialPriority", "SelfInitiated")}
    malformed = Counter()
    timestamp_min = {field: None for field in TIMESTAMP_FIELDS}
    timestamp_max = {field: None for field in TIMESTAMP_FIELDS}
    sequence = Counter()
    priority = Counter()
    priority_value_counts = {"InitialPriority": Counter(), "Priority": Counter()}
    item_seen = set()
    duplicate_items = 0
    final_type_counts = Counter()
    initial_type_counts = Counter()
    type_to_text_hashes = defaultdict(set)
    disposition_to_text_hashes = defaultdict(set)
    type_change_count = 0
    type_comparable = 0
    stage_by_selfinitiated = defaultdict(Counter)
    monthly = defaultdict(lambda: {"rows": 0, "missing": Counter(), "sequence": Counter()})
    rows = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        for row in reader:
            rows += 1
            for field in header:
                value = row.get(field, "")
                if value == "":
                    missing[field] += 1

            item = row.get("NOPD_Item", "")
            if item:
                if item in item_seen:
                    duplicate_items += 1
                else:
                    item_seen.add(item)

            parsed = {}
            for field in TIMESTAMP_FIELDS:
                parsed[field], failed = parse_timestamp(row.get(field, ""))
                if failed:
                    malformed[field] += 1
                value = parsed[field]
                if value is not None:
                    timestamp_min[field] = value if timestamp_min[field] is None else min(timestamp_min[field], value)
                    timestamp_max[field] = value if timestamp_max[field] is None else max(timestamp_max[field], value)

            create = parsed["TimeCreate"]
            dispatch = parsed["TimeDispatch"]
            arrive = parsed["TimeArrive"]
            closed = parsed["TimeClosed"]
            month_key = create.strftime("%Y-%m") if create else "UNKNOWN"
            m = monthly[month_key]
            m["rows"] += 1
            for field in RELEVANT_FIELDS:
                if row.get(field, "") == "":
                    m["missing"][field] += 1

            checks = {
                "dispatch_before_create": create and dispatch and dispatch < create,
                "arrive_before_create": create and arrive and arrive < create,
                "closed_before_create": create and closed and closed < create,
                "arrive_before_dispatch": dispatch and arrive and arrive < dispatch,
                "closed_before_dispatch": dispatch and closed and closed < dispatch,
                "closed_before_arrive": arrive and closed and closed < arrive,
                "arrival_without_dispatch": arrive and dispatch is None,
                "closed_without_arrival": closed and arrive is None,
            }
            for name, flag in checks.items():
                if flag:
                    sequence[name] += 1
                    m["sequence"][name] += 1

            p0 = row.get("InitialPriority", "").strip()
            p1 = row.get("Priority", "").strip()
            if p0:
                distinct["InitialPriority"].add(p0)
                priority_value_counts["InitialPriority"][p0] += 1
            if p1:
                distinct["Priority"].add(p1)
                priority_value_counts["Priority"][p1] += 1
            si = row.get("SelfInitiated", "").strip()
            if si:
                distinct["SelfInitiated"].add(si)
            stage_group = si or "MISSING"
            stage_by_selfinitiated[stage_group]["rows"] += 1
            if dispatch is not None:
                stage_by_selfinitiated[stage_group]["dispatch_present"] += 1
            if arrive is not None:
                stage_by_selfinitiated[stage_group]["arrival_present"] += 1
            if closed is not None:
                stage_by_selfinitiated[stage_group]["close_present"] += 1
            if p0 and p1:
                priority["both_present"] += 1
                if p0 != p1:
                    priority["exact_endpoint_disagreement"] += 1
                if p0[:1] != p1[:1]:
                    priority["numeric_endpoint_disagreement"] += 1
                elif p0 != p1:
                    priority["suffix_only_endpoint_disagreement"] += 1

            final_code = row.get("Type", "").strip()
            initial_code = row.get("InitialType", "").strip()
            if final_code:
                final_type_counts[final_code] += 1
                if row.get("TypeText", ""):
                    type_to_text_hashes[final_code].add(hash_text(row["TypeText"]))
            if initial_code:
                initial_type_counts[initial_code] += 1
            if final_code and initial_code:
                type_comparable += 1
                if final_code != initial_code:
                    type_change_count += 1

            disposition = row.get("Disposition", "").strip()
            if disposition and row.get("DispositionText", ""):
                disposition_to_text_hashes[disposition].add(hash_text(row["DispositionText"]))

    completeness = []
    for field in header:
        completeness.append(
            {
                "year": year,
                "field": field,
                "rows": rows,
                "nonmissing": rows - missing[field],
                "missing": missing[field],
                "nonmissing_rate": (rows - missing[field]) / rows,
            }
        )

    monthly_rows = []
    for month, values in sorted(monthly.items()):
        n = values["rows"]
        record = {"year": year, "month": month, "rows": n}
        for field in RELEVANT_FIELDS:
            record[f"{field}_nonmissing_rate"] = (n - values["missing"][field]) / n
        for name in (
            "dispatch_before_create",
            "arrive_before_create",
            "closed_before_create",
            "arrive_before_dispatch",
            "closed_before_dispatch",
            "closed_before_arrive",
            "arrival_without_dispatch",
            "closed_without_arrival",
        ):
            record[f"{name}_count"] = values["sequence"][name]
        monthly_rows.append(record)

    return {
        "year": year,
        "dataset_id": spec["id"],
        "csv_path": csv_path,
        "header": header,
        "rows": rows,
        "completeness": completeness,
        "monthly": monthly_rows,
        "malformed_timestamps": dict(malformed),
        "timestamp_min": {k: v.isoformat() if v else None for k, v in timestamp_min.items()},
        "timestamp_max": {k: v.isoformat() if v else None for k, v in timestamp_max.items()},
        "sequence_inconsistencies": dict(sequence),
        "duplicate_item_rows": duplicate_items,
        "unique_item_count": len(item_seen),
        "priority": dict(priority),
        "priority_values": {k: sorted(v) for k, v in distinct.items()},
        "priority_value_counts": {
            field: dict(sorted(counts.items())) for field, counts in priority_value_counts.items()
        },
        "priority_outside_documented_root_0_to_3": {
            field: {
                "rows": sum(
                    count for value, count in counts.items() if value[:1] not in {"0", "1", "2", "3"}
                ),
                "values": sorted(value for value in counts if value[:1] not in {"0", "1", "2", "3"}),
            }
            for field, counts in priority_value_counts.items()
        },
        "final_type_counts": final_type_counts,
        "initial_type_counts": initial_type_counts,
        "type_to_text_hashes": type_to_text_hashes,
        "disposition_to_text_hashes": disposition_to_text_hashes,
        "type_comparable": type_comparable,
        "type_change_count": type_change_count,
        "stage_by_selfinitiated": {
            group: {
                "rows": counts["rows"],
                "dispatch_present": counts["dispatch_present"],
                "dispatch_present_rate": counts["dispatch_present"] / counts["rows"],
                "arrival_present": counts["arrival_present"],
                "arrival_present_rate": counts["arrival_present"] / counts["rows"],
                "close_present": counts["close_present"],
                "close_present_rate": counts["close_present"] / counts["rows"],
            }
            for group, counts in sorted(stage_by_selfinitiated.items())
        },
    }


def decode_powerbi_rows(path: Path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    data = obj["results"][0]["result"]["data"]
    ds = data["dsr"]["DS"][0]
    dm1 = next((item["DM1"] for item in ds["PH"] if "DM1" in item), None)
    if dm1 is None:
        dm1 = next(
            value
            for item in ds["PH"]
            for key, value in item.items()
            if key.startswith("DM") and isinstance(value, list)
        )
    select = data["descriptor"]["Select"]
    dictionaries = ds.get("ValueDicts", {})
    # Power BI places dictionary bindings on the first DM1 row's schema
    # descriptors, not consistently on the top-level result descriptors.
    # Bind by the stable select name so categorical values decode to their
    # public labels rather than the integer dictionary offsets.
    dictionary_by_name = {
        item.get("N"): item.get("DN")
        for item in dm1[0].get("S", [])
        if item.get("N") and item.get("DN")
    }
    previous = [None] * len(select)
    rows = []
    for raw in dm1:
        cells = list(raw.get("C", []))
        repeat = int(raw.get("R", 0))
        values = []
        for i, descriptor in enumerate(select):
            if repeat & (1 << i):
                value = previous[i]
            else:
                value = cells.pop(0) if cells else None
            dict_name = descriptor.get("DN") or dictionary_by_name.get(
                descriptor.get("Value", descriptor["Name"])
            )
            if dict_name is not None and isinstance(value, int):
                value = dictionaries[dict_name][value]
            values.append(value)
        previous = values
        rows.append({descriptor["Name"]: value for descriptor, value in zip(select, values)})
    return rows


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def source_manifest(audits):
    sources = []
    for audit in audits:
        year = audit["year"]
        spec = DATASETS[year]
        metadata_path = spec["dir"] / "metadata.json"
        columns_path = spec["dir"] / "columns.json"
        dictionary_path = spec["dir"] / "NOPD_-_Data_dictionary_for_Calls_For_Service_Open_Data.xlsx"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
        for path, kind, url in (
            (audit["csv_path"], "official_csv_export", f"https://data.nola.gov/api/views/{spec['id']}/rows.csv?accessType=DOWNLOAD"),
            (metadata_path, "official_socrata_metadata", f"https://data.nola.gov/api/views/{spec['id']}"),
            (columns_path, "official_socrata_columns", f"https://data.nola.gov/api/views/{spec['id']}/columns.json"),
            (
                dictionary_path,
                "official_attached_xlsx_dictionary",
                f"https://data.nola.gov/api/views/{spec['id']}/files/{metadata['metadata']['attachments'][0]['assetId']}",
            ),
        ):
            sources.append(
                {
                    "kind": kind,
                    "title": metadata["name"],
                    "dataset_id": spec["id"],
                    "year": year,
                    "url": url,
                    "retrieved_at_utc": file_retrieved_iso(path),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                    "rows": audit["rows"] if kind == "official_csv_export" else None,
                    "created_at_utc": epoch_iso(metadata.get("createdAt")),
                    "data_updated_at_utc": epoch_iso(metadata.get("rowsUpdatedAt")),
                    "view_last_modified_at_utc": epoch_iso(metadata.get("viewLastModified")),
                }
            )

    other = {
        "browse_nopd_data_public_records.html": (
            "official_nopd_dashboard_directory",
            "https://nola.gov/browse-nopd-data-public-records/",
        ),
        "nopd_chapter_41_4_1_response_to_police_calls_revised_2025.pdf": (
            "official_nopd_priority_response_policy",
            "https://nola.gov/nola/media/NOPD/Policies/Chapter-41-4-1-Response-to-Police-Calls_1.pdf",
        ),
        "nopd_chapter_41_4_2_alternative_police_response_revised_2024.pdf": (
            "official_nopd_alternative_response_policy",
            "https://nola.gov/nola/media/NOPD/Policies/41-4-2-Alternative-Police-Response-Effective-9-15-2024.pdf",
        ),
        "nopd_sustainment_plan_2024.pdf": (
            "official_public_reform_commitment_not_public_data",
            "https://nola.gov/nola/media/NOPD/Consent%20Decree/NOPD%20Audits/Sustainment-Plan-%28Ref-Doc-793-1%29-9-27-2024.pdf",
        ),
        "nopd_response_times_powerbi_models_and_exploration.json": (
            "public_dashboard_model",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/b5330cbb-48ab-42fe-8228-01e3d60735ec/modelsAndExploration?preferReadOnlySession=true",
        ),
        "nopd_response_times_powerbi_conceptual_schema.json": (
            "public_dashboard_conceptual_schema_normalized",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/conceptualschema",
        ),
        "nopd_response_times_powerbi_year_counts.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_year_source_counts.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_year_priority_change_counts.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_enroute_aggregate.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_all_dispositions_aggregate.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_cad_source_detail_aggregate.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_initial_modifier_aggregate.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_final_modifier_aggregate.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "nopd_response_times_powerbi_signal_change_aggregate.json": (
            "public_dashboard_aggregate_query",
            "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true",
        ),
        "electronic_police_report_2025_metadata.json": (
            "official_epr_2025_metadata",
            "https://data.nola.gov/api/views/agqi-9adb",
        ),
        "electronic_police_report_2025_columns.json": (
            "official_epr_2025_columns",
            "https://data.nola.gov/api/views/agqi-9adb/columns.json",
        ),
        "socrata_catalog_search_epr_2026.json": (
            "official_socrata_catalog_query",
            "https://api.us.socrata.com/api/catalog/v1?q=Electronic%20Police%20Report%202026&search_context=data.nola.gov&limit=20",
        ),
    }
    for name, (kind, url) in other.items():
        path = CURRENT_SOURCES / name
        sources.append(
            {
                "kind": kind,
                "title": name,
                "url": url,
                "retrieved_at_utc": file_retrieved_iso(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return {
        "manifest_version": "m8p_source_manifest_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "primary_source_rule": "Official City of New Orleans, Data.NOLA, NOPD, and the public NOPD Power BI report only.",
        "sources": sources,
    }


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)
    audits = [audit_dataset(year, spec) for year, spec in DATASETS.items()]

    completeness = [row for audit in audits for row in audit["completeness"]]
    monthly = [row for audit in audits for row in audit["monthly"]]
    write_csv(PROCESSED / "field_completeness.csv", completeness)
    write_csv(PROCESSED / "monthly_quality.csv", monthly)

    a25, a26 = audits
    codes25 = set(a25["final_type_counts"])
    codes26 = set(a26["final_type_counts"])
    common_codes = sorted(codes25 & codes26)
    mapping_rows = []
    stable_count = 0
    for code in common_codes:
        h25 = sorted(a25["type_to_text_hashes"][code])
        h26 = sorted(a26["type_to_text_hashes"][code])
        stable = h25 == h26
        stable_count += int(stable)
        mapping_rows.append(
            {
                "type_code": code,
                "present_2025": True,
                "present_2026": True,
                "text_hashes_2025": "|".join(h25),
                "text_hashes_2026": "|".join(h26),
                "semantic_hash_set_stable": stable,
                "rows_2025": a25["final_type_counts"][code],
                "rows_2026": a26["final_type_counts"][code],
            }
        )
    for code in sorted(codes25 - codes26):
        mapping_rows.append(
            {
                "type_code": code,
                "present_2025": True,
                "present_2026": False,
                "text_hashes_2025": "|".join(sorted(a25["type_to_text_hashes"][code])),
                "text_hashes_2026": "",
                "semantic_hash_set_stable": False,
                "rows_2025": a25["final_type_counts"][code],
                "rows_2026": 0,
            }
        )
    for code in sorted(codes26 - codes25):
        mapping_rows.append(
            {
                "type_code": code,
                "present_2025": False,
                "present_2026": True,
                "text_hashes_2025": "",
                "text_hashes_2026": "|".join(sorted(a26["type_to_text_hashes"][code])),
                "semantic_hash_set_stable": False,
                "rows_2025": 0,
                "rows_2026": a26["final_type_counts"][code],
            }
        )
    write_csv(PROCESSED / "call_type_semantic_stability.csv", mapping_rows)

    public_year_counts = decode_powerbi_rows(
        CURRENT_SOURCES / "nopd_response_times_powerbi_year_counts.json"
    )
    public_source_counts = decode_powerbi_rows(
        CURRENT_SOURCES / "nopd_response_times_powerbi_year_source_counts.json"
    )
    public_priority_change_counts = decode_powerbi_rows(
        CURRENT_SOURCES / "nopd_response_times_powerbi_year_priority_change_counts.json"
    )
    public_model_only_probes = {
        name: decode_powerbi_rows(CURRENT_SOURCES / file_name)
        for name, file_name in {
            "all_dispositions": "nopd_response_times_powerbi_all_dispositions_aggregate.json",
            "cad_record_source_detail": "nopd_response_times_powerbi_cad_source_detail_aggregate.json",
            "initial_modifying_circumstance": "nopd_response_times_powerbi_initial_modifier_aggregate.json",
            "final_modifying_circumstance": "nopd_response_times_powerbi_final_modifier_aggregate.json",
            "signal_change_flag": "nopd_response_times_powerbi_signal_change_aggregate.json",
        }.items()
    }
    model = json.loads(
        (CURRENT_SOURCES / "nopd_response_times_powerbi_models_and_exploration.json").read_text(
            encoding="utf-8"
        )
    )
    conceptual = json.loads(
        (CURRENT_SOURCES / "nopd_response_times_powerbi_conceptual_schema.json").read_text(
            encoding="utf-8"
        )
    )
    enroute_probe = json.loads(
        (CURRENT_SOURCES / "nopd_response_times_powerbi_enroute_aggregate.json").read_text(
            encoding="utf-8"
        )
    )
    properties = [
        {"entity": entity["Name"], "property": prop["Name"], "kind": "measure" if "Measure" in prop else "column"}
        for schema in conceptual["schemas"]
        for entity in schema["schema"]["Entities"]
        for prop in entity.get("Properties", [])
    ]
    queue_terms = re.compile(r"queue|holding|available|availability|unit status|fallback|uptime|callback", re.I)
    dashboard_summary = {
        "report_title": "NOPD Calls for Service Response Times",
        "public_report_url": "https://app.powerbigov.us/view?r=eyJrIjoiYjUzMzBjYmItNDhhYi00MmZlLTgyMjgtMDFlM2Q2MDczNWVjIiwidCI6IjA4Y2JmNDg1LTFjYjctNGEwMi05YTIxLTBkZDliNDViOWZmNyJ9",
        "resource_key": "b5330cbb-48ab-42fe-8228-01e3d60735ec",
        "model_id": model["models"][0]["id"],
        "model_last_refresh": model["models"][0]["LastRefreshTime"],
        "machine_readable_public_model": True,
        "machine_readable_public_query_endpoint_verified": True,
        "enroute_seconds_property_query_verified": bool(
            enroute_probe.get("results")
            and not enroute_probe["results"][0].get("result", {}).get("error")
        ),
        "enroute_seconds_property_in_current_report_visuals": False,
        "enroute_seconds_public_semantics_documented": False,
        "enroute_probe_note": "Aggregate-only query returned value groups. The property is machine-queryable, but it is absent from current report visuals and no official public definition was located; it cannot support a strict identified-set contraction without a semantic binding.",
        "direct_download_or_csv_export_verified": False,
        "public_year_counts": public_year_counts,
        "public_cad_source_counts": public_source_counts,
        "public_priority_change_counts": public_priority_change_counts,
        "additional_model_only_field_probes": public_model_only_probes,
        "model_only_field_probe_interpretation": "All Dispositions, source-detail, modifier, and signal-change values are publicly queryable in aggregate. They are absent from the Socrata dictionaries and lack public definitions for construction, ordering, overwrite behavior, or continuity; they are candidate public enrichments, not qualified event histories.",
        "property_count": len(properties),
        "properties": properties,
        "queue_availability_continuity_callback_properties": [
            item for item in properties if queue_terms.search(item["property"])
        ],
        "coverage_note": "The public model covers 2023-2026 and classifies all counted rows as Not Officer Initiated. It does not include the 2021 Ida year.",
    }
    (METADATA / "dashboard_machine_readability.json").write_text(
        json.dumps(dashboard_summary, indent=2, sort_keys=True), encoding="utf-8"
    )

    audit_summary = {
        "audit_version": "m8p_current_data_validity_audit_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "Annual aggregate data-quality audit only; no shock or outcome search.",
        "years": {},
        "year_to_year": {
            "header_exact_match": a25["header"] == a26["header"],
            "common_final_type_codes": len(common_codes),
            "final_type_codes_2025": len(codes25),
            "final_type_codes_2026": len(codes26),
            "final_type_codes_only_2025": sorted(codes25 - codes26),
            "final_type_codes_only_2026": sorted(codes26 - codes25),
            "common_type_code_text_hash_sets_stable": stable_count,
            "common_type_code_text_hash_sets_changed": len(common_codes) - stable_count,
            "2025_row_share_with_type_code_observed_in_2026": sum(
                count for code, count in a25["final_type_counts"].items() if code in codes26
            )
            / a25["rows"],
            "2026_row_share_with_type_code_observed_in_2025": sum(
                count for code, count in a26["final_type_counts"].items() if code in codes25
            )
            / a26["rows"],
        },
    }
    for audit in audits:
        priority = audit["priority"]
        comparable = priority.get("both_present", 0)
        audit_summary["years"][str(audit["year"])] = {
            "dataset_id": audit["dataset_id"],
            "rows": audit["rows"],
            "unique_item_count": audit["unique_item_count"],
            "duplicate_item_rows": audit["duplicate_item_rows"],
            "timestamp_min": audit["timestamp_min"],
            "timestamp_max": audit["timestamp_max"],
            "malformed_timestamps": audit["malformed_timestamps"],
            "sequence_inconsistencies": audit["sequence_inconsistencies"],
            "priority_endpoint": {
                **priority,
                "exact_disagreement_rate_among_both_present": priority.get(
                    "exact_endpoint_disagreement", 0
                )
                / comparable,
                "numeric_disagreement_rate_among_both_present": priority.get(
                    "numeric_endpoint_disagreement", 0
                )
                / comparable,
            },
            "priority_values": audit["priority_values"],
            "priority_outside_documented_root_0_to_3": audit[
                "priority_outside_documented_root_0_to_3"
            ],
            "final_type_code_count": len(audit["final_type_counts"]),
            "initial_type_code_count": len(audit["initial_type_counts"]),
            "type_change_count": audit["type_change_count"],
            "type_change_rate_among_both_present": audit["type_change_count"]
            / audit["type_comparable"],
            "stage_by_selfinitiated": audit["stage_by_selfinitiated"],
        }
    (PROCESSED / "current_data_validity_audit.json").write_text(
        json.dumps(audit_summary, indent=2, sort_keys=True), encoding="utf-8"
    )

    locked = json.loads(LOCKED_2021_METADATA.read_text(encoding="utf-8-sig"))
    schemas = {}
    for label, obj in (
        ("2021_locked", locked),
        ("2025", json.loads((DATASETS[2025]["dir"] / "metadata.json").read_text(encoding="utf-8-sig"))),
        ("2026", json.loads((DATASETS[2026]["dir"] / "metadata.json").read_text(encoding="utf-8-sig"))),
    ):
        schemas[label] = {
            col["fieldName"]: {"label": col["name"], "datatype": col["dataTypeName"]}
            for col in obj["columns"]
            if not col["fieldName"].startswith(":@")
        }
    relevant_machine = [
        "nopd_item",
        "type_",
        "typetext",
        "priority",
        "initialtype",
        "initialtypetext",
        "initialpriority",
        "timecreate",
        "timedispatch",
        "timearrive",
        "timeclosed",
        "disposition",
        "dispositiontext",
        "selfinitiated",
        "beat",
        "policedistrict",
    ]
    schema_rows = []
    for machine in relevant_machine:
        row = {"machine_field": machine}
        for label in ("2021_locked", "2025", "2026"):
            col = schemas[label].get(machine)
            row[f"{label}_present"] = col is not None
            row[f"{label}_label"] = col["label"] if col else ""
            row[f"{label}_datatype"] = col["datatype"] if col else ""
        schema_rows.append(row)
    write_csv(METADATA / "raw_schema_comparison.csv", schema_rows)
    (METADATA / "source_manifest.json").write_text(
        json.dumps(source_manifest(audits), indent=2, sort_keys=True), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
