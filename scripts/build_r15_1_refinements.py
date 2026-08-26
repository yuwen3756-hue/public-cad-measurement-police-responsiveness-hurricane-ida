"""Build the R15.1 presentation and reproducibility refinements.

The script derives only aggregate displays and checks from the packaged R15
objects. It does not read row-level records or change the R15 scientific-result
inputs.
"""
from __future__ import annotations

import csv
import gzip
import json
import os
from collections import defaultdict
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE / "source"
TALLY = (
    PACKAGE
    / "reproduction"
    / "repository_snapshot"
    / "pilot_911_dv"
    / "experiments"
    / "nola_2020-01-01_2024-12-31_beland_plus_wave2"
    / "data"
    / "interim"
    / "w2_period_tally.csv.gz"
)
STATE_NAMES = ("J00", "J10", "J01", "J11")


def readable_path(path: Path) -> Path:
    """Return a Windows extended-length path when the package path exceeds MAX_PATH."""
    resolved = path.resolve()
    if os.name == "nt" and not str(resolved).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(resolved))
    return resolved


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError(f"Refusing to write empty artifact: {path.name}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_time_path() -> list[dict]:
    rows = read_csv(SOURCE / "r15_daily_ida_field_completeness.csv")
    selected = [
        row
        for row in rows
        if "2021-08-22" <= row["date"] <= "2021-09-12"
    ]
    if len(selected) != 22:
        raise RuntimeError(f"Expected 22 Ida-path days, found {len(selected)}")
    output = []
    for row in selected:
        day = row["date"]
        output.append(
            {
                "date": day,
                "records": row["n"],
                "dispatch_share": row["dispatch_share"],
                "arrival_share": row["arrival_share"],
                "j01_given_arrival": row["j01_given_arrival"],
                "period": (
                    "Ida_event_window"
                    if "2021-08-29" <= day < "2021-09-03"
                    else "post_Ida_recovery"
                    if day >= "2021-09-03"
                    else "pre_Ida_baseline"
                ),
            }
        )
    write_csv(SOURCE / "r15_1_ida_time_path.csv", output)
    return output


def build_nonoverlap_sensitivity() -> list[dict]:
    rows = read_csv(SOURCE / "r15_raw_window_scores.csv")
    ida = next(row for row in rows if row["window_start"] == "2021-08-29")
    ida_value = float(ida["raw_max_cell"])
    references = sorted(
        (
            row
            for row in rows
            if row["both_sides_after_change"] == "True"
            and row["frozen_context_excluded"] == "False"
            and row["window_start"] != "2021-08-29"
            and row["raw_max_cell"]
        ),
        key=lambda row: row["window_start"],
    )
    if len(references) != 151:
        raise RuntimeError(f"Expected 151 post-change references, found {len(references)}")
    output = []
    for phase in (0, 1):
        subset = references[phase::2]
        rank = 1 + sum(float(row["raw_max_cell"]) > ida_value for row in subset)
        output.append(
            {
                "alternating_phase": phase + 1,
                "selection_rule": f"chronological post-change references at indices {phase + 1}, {phase + 3}, ...",
                "reference_count": len(subset),
                "denominator_including_Ida": len(subset) + 1,
                "Ida_raw_max_cell": ida["raw_max_cell"],
                "largest_reference_raw_max_cell": max(float(row["raw_max_cell"]) for row in subset),
                "Ida_rank_including_Ida": rank,
                "first_reference_start": subset[0]["window_start"],
                "last_reference_start": subset[-1]["window_start"],
            }
        )
    write_csv(SOURCE / "r15_1_nonoverlap_sensitivity.csv", output)
    return output


def tally_july_states() -> dict[tuple[str, str], dict[str, int]]:
    totals: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {state: 0 for state in STATE_NAMES}
    )
    stream_map = {
        "non_officer_self_initiated": "non_officer",
        "officer_initiated": "officer",
    }
    with gzip.open(readable_path(TALLY), "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            day = row["date"]
            if not ("2021-07-25" <= day <= "2021-07-31"):
                continue
            if row["si"] not in stream_map:
                continue
            key = (day, stream_map[row["si"]])
            for state in STATE_NAMES:
                totals[key][state] += int(row[state])
    return dict(totals)


def build_raw_aggregate_parity() -> list[dict]:
    raw_rows = read_csv(SOURCE / "r15_raw_july_25_31_audit.csv")
    raw_rows = [row for row in raw_rows if row["initiation_stream"] in {"non_officer", "officer"}]
    if len(raw_rows) != 14:
        raise RuntimeError(f"Expected 14 raw-audit day-stream rows, found {len(raw_rows)}")
    aggregate = tally_july_states()
    output = []
    for row in raw_rows:
        key = (row["date"], row["initiation_stream"])
        if key not in aggregate:
            raise RuntimeError(f"Aggregate tally missing {key}")
        out = {"date": key[0], "initiation_stream": key[1]}
        matched = True
        for state in STATE_NAMES:
            raw_value = int(row[state])
            aggregate_value = aggregate[key][state]
            out[f"raw_{state}"] = raw_value
            out[f"aggregate_{state}"] = aggregate_value
            out[f"difference_{state}"] = raw_value - aggregate_value
            matched = matched and raw_value == aggregate_value
        out["parity_status"] = "MATCH" if matched else "MISMATCH"
        output.append(out)
    if any(row["parity_status"] != "MATCH" for row in output):
        raise RuntimeError("Raw-versus-aggregate July state parity failed")
    write_csv(SOURCE / "r15_1_raw_aggregate_parity.csv", output)
    return output


def main() -> None:
    time_path = build_time_path()
    nonoverlap = build_nonoverlap_sensitivity()
    parity = build_raw_aggregate_parity()
    diagnostic = {
        "artifact_type": "R15_1_TEXT_AND_REPRODUCIBILITY_REFINEMENTS",
        "paper_version": "R15.1",
        "scientific_results_version": "R15",
        "source_boundary": "derived only from packaged R15 aggregate objects",
        "ida_time_path_days": len(time_path),
        "alternating_nonoverlap_sensitivity": nonoverlap,
        "raw_aggregate_parity_rows": len(parity),
        "raw_aggregate_state_cells_checked": len(parity) * len(STATE_NAMES),
        "raw_aggregate_parity_status": "MATCH",
    }
    (SOURCE / "r15_1_refinement_diagnostics.json").write_text(
        json.dumps(diagnostic, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("R15_1_REFINEMENT_BUILD_PASS")


if __name__ == "__main__":
    main()
