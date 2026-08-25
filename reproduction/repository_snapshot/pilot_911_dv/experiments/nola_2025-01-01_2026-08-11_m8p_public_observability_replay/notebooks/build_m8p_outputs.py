from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PROCESSED = EXP / "data" / "processed"
METADATA = EXP / "metadata"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def pct(value: float | None) -> str:
    return "not established" if value is None else f"{100 * value:.4f}% nonmissing"


def main() -> None:
    completeness = read_csv(PROCESSED / "field_completeness.csv")
    current_rates = {
        (row["year"], row["field"]): float(row["nonmissing_rate"])
        for row in completeness
    }

    locked_audit_path = (
        ROOT
        / "pilot_911_dv/experiments/nola_2020-01-01_2024-12-31_path_e8a_field_qualification/data/processed/schema_audit.json"
    )
    locked_audit = json.loads(locked_audit_path.read_text(encoding="utf-8"))
    locked_months = [row for row in locked_audit["monthly"] if row["year"] == 2021]
    locked_rows = sum(row["rows"] for row in locked_months)

    def locked_rate(key: str) -> float:
        return sum(row["rows"] * row["coverage"][key] for row in locked_months) / locked_rows

    locked_rates = {
        "InitialType": locked_rate("initialtype_present_rate"),
        "Priority": locked_rate("priority_present_rate"),
        "SelfInitiated": locked_rate("selfinitiated_present_rate"),
        "TimeCreate": locked_rate("timecreate_parseable_rate"),
        "TimeDispatch": locked_rate("timedispatch_present_rate"),
        "TimeArrive": locked_rate("timearrive_present_rate"),
        "TimeClosed": locked_rate("timeclosed_present_rate"),
    }

    raw_types = {
        "NOPD_Item": ("text", "text", "text"),
        "Type": ("text", "text", "text"),
        "TypeText": ("text", "text", "text"),
        "InitialType": ("text", "text", "text"),
        "InitialTypeText": ("text", "text", "text"),
        "Priority": ("text", "text", "text"),
        "InitialPriority": ("text", "text", "text"),
        "TimeCreate": ("calendar_date", "text", "text"),
        "TimeDispatch": ("calendar_date", "text", "text"),
        "TimeArrive": ("calendar_date", "text", "text"),
        "TimeClosed": ("calendar_date", "text", "text"),
        "Disposition": ("text", "text", "text"),
        "DispositionText": ("text", "text", "text"),
        "SelfInitiated": ("text", "text", "text"),
        "Beat": ("text", "text", "text"),
        "PoliceDistrict": ("number", "text", "text"),
    }
    machine = {
        "NOPD_Item": "nopd_item",
        "Type": "type_",
        "TypeText": "typetext",
        "InitialType": "initialtype",
        "InitialTypeText": "initialtypetext",
        "Priority": "priority",
        "InitialPriority": "initialpriority",
        "TimeCreate": "timecreate",
        "TimeDispatch": "timedispatch",
        "TimeArrive": "timearrive",
        "TimeClosed": "timeclosed",
        "Disposition": "disposition",
        "DispositionText": "dispositiontext",
        "SelfInitiated": "selfinitiated",
        "Beat": "beat",
        "PoliceDistrict": "policedistrict",
    }
    raw_semantics = {
        "NOPD_Item": "Public CAD item identifier.",
        "Type": "Final/current public incident signal code endpoint.",
        "TypeText": "Final/current public incident signal description endpoint.",
        "InitialType": "Initial public incident signal code endpoint.",
        "InitialTypeText": "Initial public incident signal description endpoint.",
        "Priority": "Final/current priority code endpoint; current dictionary defines roots 0-3 and suffix ordering.",
        "InitialPriority": "Initial priority code endpoint; current dictionary directs users to Priority semantics.",
        "TimeCreate": "Timestamp when the CAD record was created.",
        "TimeDispatch": "Timestamp entered when an officer was dispatched.",
        "TimeArrive": "Timestamp entered when an officer arrived.",
        "TimeClosed": "Timestamp when the CAD item was closed.",
        "Disposition": "Final/current public disposition code endpoint.",
        "DispositionText": "Final/current public disposition label endpoint.",
        "SelfInitiated": "Whether an officer generated the item in the field rather than responding to a 911 call.",
        "Beat": "Public beat endpoint.",
        "PoliceDistrict": "Public police-district endpoint.",
    }
    genealogy: list[dict] = []
    for label, types in raw_types.items():
        endpoint_kind = "single public row endpoint"
        if label.startswith("Time"):
            endpoint_kind = "single recorded stage timestamp; not stage-event history"
        elif label.startswith("Initial"):
            endpoint_kind = "initial endpoint; paired with final endpoint, not transition history"
        elif label in {"Priority", "Type", "TypeText", "Disposition", "DispositionText"}:
            endpoint_kind = "final/current endpoint; overwrite/history behavior not public"
        genealogy.append(
            {
                "variable_concept": label,
                "label": label,
                "machine_field": machine[label],
                "datatype_2021": types[0],
                "datatype_2025": types[1],
                "datatype_2026": types[2],
                "present_2021": True,
                "present_2025": True,
                "present_2026": True,
                "public_surface": "Data.NOLA annual Calls for Service",
                "row_level_vs_aggregate": "row-level public record",
                "endpoint_vs_event_history": endpoint_kind,
                "multiplicity": "one field value per public CAD row",
                "overwrite_history_behavior": "No public version/event history or overwrite rule located.",
                "missingness_2021": pct(locked_rates.get(label)),
                "missingness_2025": pct(current_rates.get(("2025", label))),
                "missingness_2026": pct(current_rates.get(("2026", label))),
                "semantic_continuity": (
                    "Present in all three regimes; 2025/2026 timestamp storage changed from calendar_date to text."
                    if label.startswith("Time")
                    else "Present with the same label in all three regimes."
                ),
                "semantics": raw_semantics[label],
                "authority_source": "Official Data.NOLA dataset metadata and attached NOPD CFS dictionary; locked 2021 official metadata.",
            }
        )

    model_rows = [
        ("First dispatch timestamp", "FirstUnitDispatchedTime", "datetime", "Single first-unit dispatch endpoint; aligns conceptually with TimeDispatch but construction is undocumented."),
        ("First arrival timestamp", "FirstUnitArrivedTime", "datetime", "Single first-unit arrival endpoint; aligns conceptually with TimeArrive but construction is undocumented."),
        ("Incident-to-dispatch duration", "Incident_To_Dispatch_Seconds", "integer", "Derived duration; dashboard construction and missing-data rules are undocumented."),
        ("Incident-to-en-route duration", "Incident_To_EnRoute_Seconds", "integer", "Aggregate query verified non-null values and a large blank group; not shown in current report visuals and no public definition located."),
        ("Incident-to-arrival duration", "Incident_to_Arrival", "integer", "Derived duration; visible response-time concept but construction and exclusions are undocumented."),
        ("Incident-to-close duration", "Incident_To_Close_Seconds", "integer", "Derived duration; construction and exclusions are undocumented."),
        ("Priority change flag", "Priority Change Flag", "text", "Derived initial-versus-final endpoint flag; not a timestamped transition history."),
        ("Signal change flag", "Signal Change Flag", "text", "Derived initial-versus-final signal flag; not a timestamped transition history."),
        ("Initial modifying circumstance", "Initial Modifying Circumanstance", "text", "Queryable aggregate category; construction from signal/priority data is undocumented."),
        ("Final modifying circumstance", "Final Modifying Circumstance", "text", "Queryable aggregate category; construction from signal/priority data is undocumented."),
        ("CAD record source", "CAD Record Source", "text", "Dashboard classifies counted rows as Not Officer Initiated; does not reconcile exactly to raw SelfInitiated counts."),
        ("CAD record source detail", "CAD Record Source Detail", "text", "Queryable values include 911, Alarm, Direct Line, EMS, MDT/Officer, PBX, Phone, and others; measure binding is not documented."),
        ("All dispositions", "All Dispositions", "text", "Queryable comma-delimited values include repeated and mixed codes; ordering, timestamps, event identity, and overwrite behavior are undocumented."),
    ]
    for concept, field, dtype, semantics in model_rows:
        genealogy.append(
            {
                "variable_concept": concept,
                "label": field,
                "machine_field": field,
                "datatype_2021": "absent from locked public schema/model",
                "datatype_2025": dtype,
                "datatype_2026": dtype,
                "present_2021": False,
                "present_2025": True,
                "present_2026": True,
                "public_surface": "Current public NOPD Response Times Power BI semantic model (model covers 2023-2026)",
                "row_level_vs_aggregate": "model column; aggregate API query verified; only selected fields appear in the visible row table",
                "endpoint_vs_event_history": "derived endpoint/model field; no qualified event history",
                "multiplicity": "one model value per modeled incident except All Dispositions, whose comma-delimited multiplicity is not qualified",
                "overwrite_history_behavior": "No public construction, version, overwrite, or event-order rule located.",
                "missingness_2021": "not applicable",
                "missingness_2025": "not published by year",
                "missingness_2026": "not published by year",
                "semantic_continuity": "Current dashboard-only enrichment; common 2021 semantic binding not established.",
                "semantics": semantics,
                "authority_source": "Official public NOPD Power BI conceptual schema and aggregate query endpoint.",
            }
        )

    genealogy.append(
        {
            "variable_concept": "CFS-to-EPR bridge identifier",
            "label": "Item_Number",
            "machine_field": "item_number",
            "datatype_2021": "text",
            "datatype_2025": "text",
            "datatype_2026": "dataset not catalog-listed as of retrieval",
            "present_2021": True,
            "present_2025": True,
            "present_2026": False,
            "public_surface": "Annual Electronic Police Report dataset",
            "row_level_vs_aggregate": "row-level EPR; one CFS item may have multiple EPR person/offense rows",
            "endpoint_vs_event_history": "bridge endpoint, not internal/public publication history",
            "multiplicity": "one-to-many from CAD item to EPR rows",
            "overwrite_history_behavior": "No public version history located.",
            "missingness_2021": "0 null item_number rows in locked aggregate probe",
            "missingness_2025": "metadata-only in this replay; not recomputed",
            "missingness_2026": "not applicable; no catalog-listed 2026 EPR dataset",
            "semantic_continuity": "Bridge exists in 2021 and 2025, but no same-year 2026 public EPR endpoint was located.",
            "semantics": "Public identifier permitting conservative CAD-EPR linkage after normalization.",
            "authority_source": "Official Data.NOLA EPR 2021/2025 metadata and official Socrata catalog query.",
        }
    )

    for concept, semantics in (
        ("calls holding / queue state", "No public row or aggregate queue-length, waiting-duration, or calls-holding time series located."),
        ("unit availability / effective capacity", "No public row or aggregate available-unit, unit-status, staffing-at-risk, or effective-capacity state located."),
        ("callback / realized APR route", "Current policy documents callbacks and alternative routes, but no public realized callback/route variable was located."),
        ("system uptime / fallback continuity", "No public CAD/dispatch uptime, outage, failover, manual-mode, or continuity-state variable was located."),
    ):
        genealogy.append(
            {
                "variable_concept": concept,
                "label": "none located",
                "machine_field": "none",
                "datatype_2021": "absent",
                "datatype_2025": "absent",
                "datatype_2026": "absent",
                "present_2021": False,
                "present_2025": False,
                "present_2026": False,
                "public_surface": "No official public data field located",
                "row_level_vs_aggregate": "neither",
                "endpoint_vs_event_history": "not observed",
                "multiplicity": "not observed",
                "overwrite_history_behavior": "not applicable",
                "missingness_2021": "structurally absent",
                "missingness_2025": "structurally absent",
                "missingness_2026": "structurally absent",
                "semantic_continuity": "Persistent public non-observability.",
                "semantics": semantics,
                "authority_source": "Official current Socrata schemas, NOPD dashboard model, dashboard directory, and current policies searched.",
            }
        )

    write_csv(METADATA / "schema_genealogy.csv", genealogy)

    reform_rows = [
        {
            "CURRENT_REFORM_OBJECT": "Initial/final priority response dashboard",
            "PUBLICLY_OBSERVABLE_NOW": "Yes: visible filters, row table, priority-change flag, and aggregate query API for 2023-2026.",
            "IDA_2021_OBSERVABLE": "InitialPriority and Priority already existed in the locked 2021 raw public schema.",
            "IDENTIFICATION_GAIN": "Presentation and reproducibility gain; no new timestamped priority-history primitive.",
            "REMAINING_GAP": "No transition timestamp, actor, reason, multiplicity, or overwrite history; dashboard/raw universes do not reconcile exactly.",
            "CAPABILITY_LAYER": "public research observability",
            "EVIDENCE_STATUS": "implemented public surface",
        },
        {
            "CURRENT_REFORM_OBJECT": "Sub-priority codes and supervisor priority modification",
            "PUBLICLY_OBSERVABLE_NOW": "Current policy defines suffix ordering and raw InitialPriority/Priority contain endpoints.",
            "IDA_2021_OBSERVABLE": "Initial/final endpoint fields existed; historical policy binding was less explicit in the locked public package.",
            "IDENTIFICATION_GAIN": "Richer current semantic documentation, not event-history identification.",
            "REMAINING_GAP": "No public reasons-over-air record, actor, transition time, or sequence.",
            "CAPABILITY_LAYER": "internal rule documented publicly",
            "EVIDENCE_STATUS": "policy semantics only for internal action",
        },
        {
            "CURRENT_REFORM_OBJECT": "Real-time supervisory CAD access to calls holding, priority changes, and officer availability",
            "PUBLICLY_OBSERVABLE_NOW": "No public calls-holding or officer-availability data located.",
            "IDA_2021_OBSERVABLE": "No.",
            "IDENTIFICATION_GAIN": "None for public research observability.",
            "REMAINING_GAP": "Hourly queue, available-unit, unit-status, staffing, and effective-capacity witnesses.",
            "CAPABILITY_LAYER": "internal supervisory capability",
            "EVIDENCE_STATUS": "publicly documented reform commitment; not public data",
        },
        {
            "CURRENT_REFORM_OBJECT": "Alternative Police Response and fallback routing",
            "PUBLICLY_OBSERVABLE_NOW": "Policy defines telephone, online, civilian field, district fallback, and excluded call families; Code 0 is public.",
            "IDA_2021_OBSERVABLE": "Public endpoints did not identify realized route or fallback state.",
            "IDENTIFICATION_GAIN": "Semantic route menu only.",
            "REMAINING_GAP": "No public realized APR assignment, transfer, callback, duty-coverage, or failure-state variable.",
            "CAPABILITY_LAYER": "internal workflow documented publicly",
            "EVIDENCE_STATUS": "policy semantics only",
        },
        {
            "CURRENT_REFORM_OBJECT": "GOA and DV callbacks",
            "PUBLICLY_OBSERVABLE_NOW": "Policy requires certain callbacks, including DV-unit handling, but callback completion is not public.",
            "IDA_2021_OBSERVABLE": "Final disposition could be observed; callback execution could not.",
            "IDENTIFICATION_GAIN": "None for realized callback/continuity identification.",
            "REMAINING_GAP": "Callback attempt, completion, timing, outcome, and responsible unit in privacy-safe aggregate form.",
            "CAPABILITY_LAYER": "internal workflow documented publicly",
            "EVIDENCE_STATUS": "policy semantics only",
        },
        {
            "CURRENT_REFORM_OBJECT": "En-route stage in dashboard model",
            "PUBLICLY_OBSERVABLE_NOW": "Incident_To_EnRoute_Seconds is aggregate-queryable but absent from current visuals and undefined publicly.",
            "IDA_2021_OBSERVABLE": "No en-route field in the locked 2021 public schema.",
            "IDENTIFICATION_GAIN": "Candidate within-stage enrichment only; strict common-estimand contraction not proved.",
            "REMAINING_GAP": "Authoritative definition, start/end clocks, missingness rules, row-universe reconciliation, and event-history behavior.",
            "CAPABILITY_LAYER": "public research observability",
            "EVIDENCE_STATUS": "queryable but semantically unqualified",
        },
        {
            "CURRENT_REFORM_OBJECT": "All-dispositions model field",
            "PUBLICLY_OBSERVABLE_NOW": "Aggregate-queryable comma-delimited disposition combinations.",
            "IDA_2021_OBSERVABLE": "Locked public schema exposed a final disposition endpoint only.",
            "IDENTIFICATION_GAIN": "Candidate multiplicity enrichment; not a qualified ordered event history.",
            "REMAINING_GAP": "Construction, ordering, timestamps, repeat semantics, and overwrite rules.",
            "CAPABILITY_LAYER": "public research observability",
            "EVIDENCE_STATUS": "queryable but semantically unqualified",
        },
        {
            "CURRENT_REFORM_OBJECT": "CFS-to-EPR public bridge",
            "PUBLICLY_OBSERVABLE_NOW": "2025 EPR exposes item_number; no catalog-listed 2026 EPR was located on 2026-08-11.",
            "IDA_2021_OBSERVABLE": "Yes: 2021 CFS-to-EPR linkage by normalized item number.",
            "IDENTIFICATION_GAIN": "No stable cross-year gain; 2026 bridge currently incomplete.",
            "REMAINING_GAP": "Same-year 2026 EPR publication and documented publication/version timing.",
            "CAPABILITY_LAYER": "public research observability",
            "EVIDENCE_STATUS": "partial",
        },
    ]
    write_csv(PROCESSED / "reform_identification_crosswalk.csv", reform_rows)

    results = {
        "result_version": "beland_plus_m8p_v1",
        "decision": "M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED",
        "decision_basis": "The current public dashboard adds useful queryable derived/model fields, including candidate en-route and disposition-multiplicity signals, but the annual raw schema is essentially the locked 2021 schema and the new fields lack common semantic/history bindings. Queue, availability, priority history, and continuity remain outside the public measurement regime.",
        "comparison_universes": {
            "locked_2021": "Official Data.NOLA CFS 2021 endpoint 3pha-hum9 plus locked public CAD-EPR and M7D topology/decomposition artifacts.",
            "2025": "Official Data.NOLA CFS 2025 endpoint 4xwx-sfte and EPR 2025 endpoint agqi-9adb.",
            "2026": "Official Data.NOLA CFS 2026 endpoint es9j-6y5d; no catalog-listed EPR 2026 located as of 2026-08-11.",
            "dashboard_ecosystem": "Official NOPD dashboard directory and Response Times Power BI report/model; Calls for Service and Crime Trends link resolves to a third-party Community Crime Map and was not treated as official primary data.",
        },
        "module_crosswalk_semantic_firewall": {
            "B": {
                "public_semantic_enrichment": "PARTIAL_CONTEXT",
                "m8d_structural_witness_status": "CLOSED",
                "reason": "The 2025 public CFS-EPR item link supplies downstream public-record context. It is not the M8 internal/public dispatch bridge U_dispatch -> D_pub, and no public internal-event/public-export reconciliation is available.",
            },
            "Q": {
                "public_semantic_enrichment": "ENDPOINT_PROXY_ONLY",
                "m8d_structural_witness_status": "CLOSED",
                "reason": "Create/dispatch/arrival/close endpoints and response-time derivatives describe public record stages, but they do not construct a queue reachable set or expose calls holding, unit availability, or effective capacity.",
            },
            "P": {
                "public_semantic_enrichment": "ENDPOINT_ENRICHED",
                "m8d_structural_witness_status": "CLOSED",
                "reason": "Initial/final priority endpoints, suffix semantics, and a change flag are public; transition times, actors, reasons, multiplicity, and event history are not. No formal PARTIAL_OUTER priority-history set is proved.",
            },
            "C": {
                "public_semantic_enrichment": "SEMANTICS_QUALIFIED",
                "m8d_structural_witness_status": "CLOSED",
                "reason": "APR, callbacks, and fallback routes are documented as policy semantics, but no public realized route, callback, uptime, or failover state was located.",
            },
        },
        "m8d_realized_witness_regime": {
            "regime": "W_0",
            "tuple": ["CLOSED", "CLOSED", "CLOSED", "CLOSED"],
            "interpretation": "Current public semantic enrichment does not open any realized M8D B-Q-P-C structural witness module.",
        },
        "ida_observability_replay": {
            "L1_public_topology_detection": {
                "status": "PUBLICLY_IDENTIFIABLE",
                "change_from_2021": "No material primitive change; create/dispatch/arrival/close topology remains public.",
            },
            "L2_within_disposition_stage_localization": {
                "status": "PARTIALLY_IDENTIFIABLE",
                "change_from_2021": "Candidate improvement from queryable en-route duration and All Dispositions, but definitions, ordering, and history are unqualified.",
            },
            "L3_internal_public_bridge_separation": {
                "status": "PARTIALLY_IDENTIFIABLE",
                "change_from_2021": "Public surfaces can be compared, but internal state and publication transformations are not exposed; 2026 EPR is missing from the catalog.",
            },
            "L4_queue_availability_reconstruction": {
                "status": "NOT_PUBLICLY_IDENTIFIABLE",
                "change_from_2021": "No contraction: no queue, calls-holding, unit-status, or availability time series.",
            },
            "L5_priority_history_reconstruction": {
                "status": "PARTIALLY_IDENTIFIABLE",
                "change_from_2021": "Current documentation and dashboard flags clarify endpoint contrasts, but the 2021 schema already exposed both endpoints and no history was added.",
            },
            "L6_continuity_fallback_reconstruction": {
                "status": "NOT_PUBLICLY_IDENTIFIABLE",
                "change_from_2021": "Policy describes fallback routes, but realized routing, callback, uptime, and failover states remain unobserved.",
            },
            "L7_cross_module_propagation": {
                "status": "PARTIALLY_IDENTIFIABLE",
                "change_from_2021": "Public priority, stage, disposition, and 2025 EPR endpoints can be cross-tabulated, but Q and C states are absent and no full B-Q-P-C path is identified.",
            },
        },
        "identified_set_comparison": {
            "common_observable_endpoint_parameters": "Conditional on a maintained frozen common-semantic mapping, I_2026(theta | Y_Ida) = I_2021(theta | Y_Ida) after schema normalization when the dashboard field is a deterministic function of InitialPriority, Priority, stage timestamps, signal endpoints, disposition endpoint, or SelfInitiated.",
            "queue_availability_priority_history_continuity_parameters": "No strict containment proved; the same decisive latent state variables remain absent.",
            "dashboard_only_candidate_fields": "En-route seconds and All Dispositions are publicly queryable, but no authoritative common semantic map to the locked 2021 estimand was located. Treating their labels as a proof of common meaning would violate the semantic-binding rule.",
            "strict_contractions_proved": [],
        },
        "claim_firewall": [
            "No claim that current reforms prevent another Ida.",
            "No claim that current police performance is better.",
            "No claim that a 2026 system would respond better.",
            "No claim that Ida would have had a different outcome.",
            "No mechanism probabilities assigned.",
        ],
    }
    (PROCESSED / "m8p_results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
