"""Build the R15 aggregate diagnostics from the packaged frozen artifacts.

The script reads only privacy-conscious aggregate files already contained in
the release. It does not read call narratives, addresses, or row-level data.
"""
from __future__ import annotations

import csv
import gzip
import json
import os
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
SNAPSHOT = ROOT / "reproduction" / "repository_snapshot" / "pilot_911_dv"
W2 = SNAPSHOT / "experiments" / "nola_2020-01-01_2024-12-31_beland_plus_wave2"
M7B = (
    SNAPSHOT
    / "experiments"
    / "nola_2020-01-01_2024-12-31_beland_plus_wave4r"
    / "candidate"
    / "m7b_same_estimator_reference_geometry"
)
M8P = (
    SNAPSHOT
    / "experiments"
    / "nola_2025-01-01_2026-08-11_m8p_public_observability_replay"
)
TALLY = W2 / "data" / "interim" / "w2_period_tally.csv.gz"

STATES = ("J00", "J10", "J01", "J11")
PRIMARY = ("J01", "J10", "J11")
PRIMARY_COLUMNS = (3, 2, 4)  # positions in [n, J00, J10, J01, J11]
HALF_HOURS = (("00-05", "06-11"), ("12-17", "18-23"))
IDA_START = date(2021, 8, 29)
CHANGE_DATE = date(2021, 7, 28)
BOOTSTRAP_REPLICATES = 4000
BOOTSTRAP_SEED = 1400


def long_name(path: Path) -> str:
    value = str(path.resolve())
    if os.name == "nt" and not value.startswith("\\\\?\\"):
        return "\\\\?\\" + value
    return value


def open_text(path: Path, mode: str = "r", newline: str | None = None):
    return open(long_name(path), mode, encoding="utf-8", newline=newline)


def read_json(path: Path):
    with open_text(path) as handle:
        return json.load(handle)


def write_json(path: Path, value) -> None:
    with open_text(path, "w", newline="") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    fields = fields or list(rows[0])
    with open_text(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def schema_era(year: int) -> str:
    return "text" if year == 2023 else "numeric"


def load_tally():
    detail: dict[tuple[date, str, str, str], np.ndarray] = defaultdict(
        lambda: np.zeros(5, dtype=np.int64)
    )
    daily: dict[tuple[date, str], np.ndarray] = defaultdict(
        lambda: np.zeros(5, dtype=np.int64)
    )
    half_totals: dict[tuple[date, str, int], np.ndarray] = defaultdict(
        lambda: np.zeros(5, dtype=np.int64)
    )
    with gzip.open(long_name(TALLY), "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            day = date.fromisoformat(row["date"])
            si = row["si"]
            initialtype = row["initialtype"].strip().upper() or "UNKNOWN"
            hour = row["hour_bucket"]
            values = np.asarray(
                [int(row["n"]), *[int(row[state]) for state in STATES]],
                dtype=np.int64,
            )
            if int(values[0]) != int(values[1:].sum()):
                raise RuntimeError(f"State counts do not sum to n: {day} {si} {initialtype} {hour}")
            detail[(day, si, initialtype, hour)] += values
            daily[(day, si)] += values
            half = 0 if hour in HALF_HOURS[0] else 1
            half_totals[(day, si, half)] += values
    return dict(detail), dict(daily), dict(half_totals)


def metrics(values: np.ndarray) -> dict:
    n, j00, j10, j01, j11 = (int(x) for x in values)
    arrival_n = j01 + j11
    return {
        "n": n,
        "dispatch_share": (j10 + j11) / n if n else None,
        "arrival_share": arrival_n / n if n else None,
        "j01_share": j01 / n if n else None,
        "j01_given_arrival": j01 / arrival_n if arrival_n else None,
    }


def aggregate_daily(daily, si: str, start: date, end: date) -> np.ndarray:
    total = np.zeros(5, dtype=np.int64)
    day = start
    while day <= end:
        total += daily.get((day, si), np.zeros(5, dtype=np.int64))
        day += timedelta(days=1)
    return total


def weekly_rows(daily, si: str) -> list[dict]:
    grouped: dict[date, np.ndarray] = defaultdict(lambda: np.zeros(5, dtype=np.int64))
    for (day, row_si), values in daily.items():
        if row_si != si:
            continue
        sunday = day - timedelta(days=(day.weekday() + 1) % 7)
        grouped[sunday] += values
    rows = []
    for sunday in sorted(grouped):
        rows.append({"week_start": sunday.isoformat(), **metrics(grouped[sunday])})
    return rows


def monthly_rows(daily, si: str) -> list[dict]:
    grouped: dict[str, np.ndarray] = defaultdict(lambda: np.zeros(5, dtype=np.int64))
    for (day, row_si), values in daily.items():
        if row_si == si:
            grouped[f"{day.year:04d}-{day.month:02d}-01"] += values
    return [{"month": month, **metrics(grouped[month])} for month in sorted(grouped)]


def annual_rows(daily, si: str) -> list[dict]:
    grouped: dict[int, np.ndarray] = defaultdict(lambda: np.zeros(5, dtype=np.int64))
    for (day, row_si), values in daily.items():
        if row_si == si:
            grouped[day.year] += values
    return [{"year": year, "initiation_stream": si, **metrics(grouped[year])} for year in sorted(grouped)]


def half_side(detail, start: date, si: str, half: int) -> dict[str, np.ndarray]:
    allowed = set(HALF_HOURS[half])
    out: dict[str, np.ndarray] = defaultdict(lambda: np.zeros(5, dtype=np.int64))
    for (day, row_si, initialtype, hour), values in detail.items():
        if day == start and row_si == si and hour in allowed:
            key = f"{initialtype}|{hour}|{schema_era(day.year)}"
            out[key] += values
    return dict(out)


def standardized_window_inputs(detail, start: date):
    bins = []
    point = np.zeros((10, 3), dtype=float)
    for index in range(10):
        event_day = start + timedelta(days=index // 2)
        reference_day = event_day - timedelta(days=7)
        event = half_side(detail, event_day, "non_officer_self_initiated", index % 2)
        reference = half_side(detail, reference_day, "non_officer_self_initiated", index % 2)
        shared = sorted(set(event) & set(reference))
        reference_denominator = sum(int(reference[key][0]) for key in shared)
        if not shared or not reference_denominator:
            raise RuntimeError(f"No common support in B{index + 1}")
        weights = {key: int(reference[key][0]) / reference_denominator for key in shared}
        for coordinate, column in enumerate(PRIMARY_COLUMNS):
            point[index, coordinate] = sum(
                weights[key]
                * (event[key][column] / event[key][0] - reference[key][column] / reference[key][0])
                for key in shared
            )
        event_n = sum(int(values[0]) for values in event.values())
        reference_n = sum(int(values[0]) for values in reference.values())
        event_common = sum(int(event[key][0]) for key in shared)
        reference_common = sum(int(reference[key][0]) for key in shared)
        bins.append(
            {
                "bin": f"B{index + 1}",
                "event": event,
                "reference": reference,
                "shared": shared,
                "weights": weights,
                "event_n": event_n,
                "reference_n": reference_n,
                "event_coverage": event_common / event_n,
                "reference_coverage": reference_common / reference_n,
            }
        )
    return point, bins


def bootstrap_cells(point: np.ndarray, bins: list[dict]) -> tuple[list[dict], dict]:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    draws = np.zeros((BOOTSTRAP_REPLICATES, 10, 3), dtype=float)
    for bin_index, item in enumerate(bins):
        for key in item["shared"]:
            event = item["event"][key]
            reference = item["reference"][key]
            event_prob = event[1:] / event[0]
            reference_prob = reference[1:] / reference[0]
            event_draw = rng.multinomial(int(event[0]), event_prob, size=BOOTSTRAP_REPLICATES)
            reference_draw = rng.multinomial(
                int(reference[0]), reference_prob, size=BOOTSTRAP_REPLICATES
            )
            draws[:, bin_index, :] += item["weights"][key] * (
                event_draw[:, (2, 1, 3)] / event[0]
                - reference_draw[:, (2, 1, 3)] / reference[0]
            )
    rows = []
    for bin_index, item in enumerate(bins):
        for coordinate, name in enumerate(PRIMARY):
            values = draws[:, bin_index, coordinate]
            rows.append(
                {
                    "bin": f"B{bin_index + 1}",
                    "coordinate": name,
                    "point": point[bin_index, coordinate],
                    "bootstrap_p025": float(np.quantile(values, 0.025)),
                    "bootstrap_p975": float(np.quantile(values, 0.975)),
                    "event_n": item["event_n"],
                    "reference_n": item["reference_n"],
                    "event_coverage": item["event_coverage"],
                    "reference_coverage": item["reference_coverage"],
                }
            )
    maximum = np.max(np.abs(draws), axis=(1, 2))
    summary = {
        "replicates": BOOTSTRAP_REPLICATES,
        "seed": BOOTSTRAP_SEED,
        "interpretation": "within-stratum multinomial record bootstrap conditional on the aggregate tally",
        "point": float(np.max(np.abs(point))),
        "p025": float(np.quantile(maximum, 0.025)),
        "p975": float(np.quantile(maximum, 0.975)),
    }
    return rows, summary


def raw_half(half_totals, day: date, si: str, half: int) -> np.ndarray:
    return half_totals.get((day, si, half), np.zeros(5, dtype=np.int64))


def raw_window(half_totals, start: date) -> tuple[float | None, int, int]:
    maximum = 0.0
    event_total = 0
    reference_total = 0
    for index in range(10):
        event_day = start + timedelta(days=index // 2)
        reference_day = event_day - timedelta(days=7)
        event = raw_half(half_totals, event_day, "non_officer_self_initiated", index % 2)
        reference = raw_half(half_totals, reference_day, "non_officer_self_initiated", index % 2)
        event_total += int(event[0])
        reference_total += int(reference[0])
        if not event[0] or not reference[0]:
            return None, event_total, reference_total
        for column in PRIMARY_COLUMNS:
            difference = event[column] / event[0] - reference[column] / reference[0]
            maximum = max(maximum, abs(float(difference)))
    return maximum, event_total, reference_total


def raw_bootstrap_draws(half_totals, start: date, seed: int) -> np.ndarray:
    """Bootstrap the full-count maximum statistic for one five-day window."""
    rng = np.random.default_rng(seed)
    draws = np.zeros((BOOTSTRAP_REPLICATES, 10, 3), dtype=float)
    for index in range(10):
        event_day = start + timedelta(days=index // 2)
        reference_day = event_day - timedelta(days=7)
        event = raw_half(half_totals, event_day, "non_officer_self_initiated", index % 2)
        reference = raw_half(half_totals, reference_day, "non_officer_self_initiated", index % 2)
        if not event[0] or not reference[0]:
            raise RuntimeError(f"Empty raw half-day for {start.isoformat()} B{index + 1}")
        event_draw = rng.multinomial(
            int(event[0]), event[1:] / event[0], size=BOOTSTRAP_REPLICATES
        )
        reference_draw = rng.multinomial(
            int(reference[0]), reference[1:] / reference[0], size=BOOTSTRAP_REPLICATES
        )
        draws[:, index, :] = (
            event_draw[:, (2, 1, 3)] / event[0]
            - reference_draw[:, (2, 1, 3)] / reference[0]
        )
    return np.max(np.abs(draws), axis=(1, 2))


def read_csv_rows(path: Path) -> list[dict]:
    with open_text(path, newline="") as handle:
        return list(csv.DictReader(handle))


def rank(value: float, references: list[float]) -> int:
    return 1 + sum(candidate > value for candidate in references)


def main() -> None:
    detail, daily, half_totals = load_tally()
    non_officer = "non_officer_self_initiated"
    officer = "officer_initiated"

    write_csv(SOURCE / "r15_weekly_field_completeness.csv", weekly_rows(daily, non_officer))
    write_csv(SOURCE / "r15_monthly_field_completeness.csv", monthly_rows(daily, non_officer))
    write_csv(SOURCE / "r15_monthly_officer_field_completeness.csv", monthly_rows(daily, officer))
    write_csv(
        SOURCE / "r15_annual_initiation_field_completeness.csv",
        annual_rows(daily, non_officer) + annual_rows(daily, officer),
    )

    daily_rows = []
    for day in sorted({key[0] for key in daily}):
        if date(2021, 7, 1) <= day <= date(2021, 9, 15):
            daily_rows.append({"date": day.isoformat(), **metrics(daily[(day, non_officer)])})
    write_csv(SOURCE / "r15_daily_ida_field_completeness.csv", daily_rows)

    first_nonzero = min(
        day for (day, si), values in daily.items() if si == non_officer and values[3] > 0
    )
    prechange_j01 = sum(
        int(values[3])
        for (day, si), values in daily.items()
        if si == non_officer and day < CHANGE_DATE
    )

    periods = [
        ("pre_change", date(2020, 1, 1), date(2021, 7, 27)),
        ("transition_week", date(2021, 7, 25), date(2021, 7, 31)),
        ("august_pre_ida", date(2021, 8, 1), date(2021, 8, 28)),
        ("ida_week", date(2021, 8, 29), date(2021, 9, 4)),
        ("post_ida", date(2021, 9, 5), date(2021, 9, 12)),
        ("year_2024", date(2024, 1, 1), date(2024, 12, 31)),
    ]
    period_rows = []
    for label, start, end in periods:
        period_rows.append(
            {"period": label, "start": start.isoformat(), "end": end.isoformat(), **metrics(aggregate_daily(daily, non_officer, start, end))}
        )
    write_csv(SOURCE / "r15_period_summary.csv", period_rows)

    current_audit = read_json(
        M8P / "data" / "processed" / "current_data_validity_audit.json"
    )
    current_rows = []
    for year in ("2025", "2026"):
        annual = current_audit["years"][year]
        for initiation in ("N", "Y"):
            values = annual["stage_by_selfinitiated"][initiation]
            current_rows.append(
                {
                    "year": year,
                    "denominator": "non_officer" if initiation == "N" else "officer",
                    "rows": values["rows"],
                    "dispatch_present": values["dispatch_present"],
                    "dispatch_share": values["dispatch_present_rate"],
                    "arrival_present": values["arrival_present"],
                    "arrival_share": values["arrival_present_rate"],
                }
            )
        all_dispatch = sum(
            annual["stage_by_selfinitiated"][value]["dispatch_present"]
            for value in ("N", "Y")
        )
        current_rows.append(
            {
                "year": year,
                "denominator": "all_public_rows",
                "rows": annual["rows"],
                "dispatch_present": all_dispatch,
                "dispatch_share": all_dispatch / annual["rows"],
                "arrival_present": sum(
                    annual["stage_by_selfinitiated"][value]["arrival_present"]
                    for value in ("N", "Y")
                ),
                "arrival_share": sum(
                    annual["stage_by_selfinitiated"][value]["arrival_present"]
                    for value in ("N", "Y")
                ) / annual["rows"],
            }
        )
    write_csv(SOURCE / "r15_current_denominator_audit.csv", current_rows)

    registry = read_json(M7B / "M7B_REFERENCE_WINDOW_REGISTRY.json")
    excluded = set(registry["frozen_context_exclusions"])
    episode_labels = {
        "2020-08-23": "Hurricane Laura",
        "2020-10-25": "Hurricane Zeta",
        "2021-02-14": "February freeze",
        "2021-08-29": "Hurricane Ida",
        "2021-09-05": "Post-Ida week",
        "2024-09-08": "Hurricane Francine",
    }
    statistics = read_csv_rows(M7B / "M7B_REFERENCE_STATISTICS.csv")
    full_references = [
        row for row in statistics
        if "FULL_QUALIFIED_REFERENCE" in row["universes"]
        and row["window_start"] != IDA_START.isoformat()
    ]
    fully_prechange_reference_count = sum(
        date.fromisoformat(row["window_start"]) + timedelta(days=4) < CHANGE_DATE
        for row in full_references
    )
    pre_stage_cutoff_reference_count = sum(
        date.fromisoformat(row["window_start"]) < date(2021, 7, 1)
        for row in full_references
    )
    membership = {row["window_start"]: row["universes"] for row in statistics}
    raw_rows = []
    current = date(2020, 1, 5)
    while current <= date(2024, 12, 29):
        score, event_n, reference_n = raw_window(half_totals, current)
        start = current.isoformat()
        raw_rows.append(
            {
                "window_start": start,
                "raw_max_cell": "" if score is None else score,
                "event_n": event_n,
                "reference_n": reference_n,
                "frozen_context_excluded": start in excluded,
                "episode": episode_labels.get(start, ""),
                "prespecified_universes": membership.get(start, ""),
                "both_sides_after_change": current - timedelta(days=7) >= CHANGE_DATE,
            }
        )
        current += timedelta(days=7)
    write_csv(SOURCE / "r15_raw_window_scores.csv", raw_rows)

    ida_stat = next(row for row in statistics if row["window_start"] == IDA_START.isoformat())
    stage_rows = [row for row in statistics if "STAGE_ERA_MATCHED_REFERENCE" in row["universes"]]
    stage_rows.sort(key=lambda row: float(row["M_max_cell"]))
    write_csv(
        SOURCE / "r15_stage_era_reference_scores.csv",
        [
            {
                "rank": index + 1,
                "window_start": row["window_start"],
                "M_max_cell": row["M_max_cell"],
                "U_full_upper": row["U_full_upper"],
            }
            for index, row in enumerate(stage_rows)
        ],
    )

    metric_columns = [
        ("M_max_cell", "M_max_cell"),
        ("A", "A"),
        ("sigma_1", "sigma_1"),
        ("sigma_2", "sigma_2"),
        ("sigma_3", "sigma_3"),
        ("U_direct", "U_direct"),
        ("U_full", "U_full_upper"),
        ("Q", "Q_upper"),
        ("D", "D_upper"),
    ]
    universe_names = (
        "FULL_QUALIFIED_REFERENCE",
        "STAGE_ERA_MATCHED_REFERENCE",
        "SAME_SEASON_STAGE_REFERENCE",
    )
    secondary_rows = []
    for universe in universe_names:
        references = [row for row in statistics if universe in row["universes"]]
        for label, column in metric_columns:
            ida_value = float(ida_stat[column])
            values = [float(row[column]) for row in references]
            secondary_rows.append(
                {
                    "universe": universe,
                    "statistic": label,
                    "Ida_value": ida_value,
                    "max_reference": max(values),
                    "Ida_rank": rank(ida_value, values),
                    "denominator_including_Ida": len(values) + 1,
                }
            )
    write_csv(SOURCE / "r15_secondary_statistic_ranks.csv", secondary_rows)

    point, bins = standardized_window_inputs(detail, IDA_START)
    matrix_rows = read_csv_rows(M7B / "M7B_REFERENCE_G_MATRICES.csv")
    published = np.zeros((10, 3), dtype=float)
    for row in matrix_rows:
        if row["window_start"] == IDA_START.isoformat():
            index = int(row["bin"][1:]) - 1
            published[index] = [float(row[f"Delta_{name}"]) for name in PRIMARY]
    parity = float(np.max(np.abs(point - published)))
    if parity > 1e-12:
        raise RuntimeError(f"R15 Ida G parity failure: {parity}")
    bootstrap_rows, bootstrap_summary = bootstrap_cells(point, bins)
    write_csv(SOURCE / "r15_bootstrap_cells.csv", bootstrap_rows)
    standardized_bootstrap_rows = [
        {
            "estimator": "standardized_common_support",
            "window_start": IDA_START.isoformat(),
            "window_label": "Hurricane Ida",
            **{key: bootstrap_summary[key] for key in ("point", "p025", "p975")},
        }
    ]
    top_stage_rows = sorted(
        stage_rows, key=lambda row: float(row["M_max_cell"]), reverse=True
    )[:5]
    for offset, row in enumerate(top_stage_rows, start=1):
        window_start = date.fromisoformat(row["window_start"])
        window_point, window_bins = standardized_window_inputs(detail, window_start)
        _, window_summary = bootstrap_cells(window_point, window_bins)
        standardized_bootstrap_rows.append(
            {
                "estimator": "standardized_common_support",
                "window_start": row["window_start"],
                "window_label": f"top_stage_reference_{offset}",
                **{key: window_summary[key] for key in ("point", "p025", "p975")},
            }
        )

    thresholds = read_json(M7B / "M7B_MAX_CELL_REFERENCE_THRESHOLD.json")["results"]
    threshold_counts = {
        universe: {
            "threshold": values["c_0.95"],
            "exceeding_cells": int(np.sum(np.abs(point) > values["c_0.95"])),
        }
        for universe, values in thresholds.items()
    }
    intervals = read_csv_rows(M7B / "M7B_UNIFIED_SCORE_INTERVALS.csv")
    widths = [float(row["upper"]) - float(row["lower"]) for row in intervals if row["window_start"] != IDA_START.isoformat()]

    event_non = aggregate_daily(daily, non_officer, date(2021, 8, 29), date(2021, 9, 2))
    event_off = aggregate_daily(daily, officer, date(2021, 8, 29), date(2021, 9, 2))
    base_non = aggregate_daily(daily, non_officer, date(2021, 8, 22), date(2021, 8, 26))
    base_off = aggregate_daily(daily, officer, date(2021, 8, 22), date(2021, 8, 26))

    ida_raw = next(float(row["raw_max_cell"]) for row in raw_rows if row["window_start"] == IDA_START.isoformat())
    raw_stage = [
        float(row["raw_max_cell"])
        for row in raw_rows
        if "STAGE_ERA_MATCHED_REFERENCE" in row["prespecified_universes"] and row["raw_max_cell"] != ""
    ]
    raw_post_change_rows = [
        row
        for row in raw_rows
        if row["both_sides_after_change"] is True
        and row["frozen_context_excluded"] is False
        and row["window_start"] != IDA_START.isoformat()
        and row["raw_max_cell"] != ""
    ]
    raw_post_change = [float(row["raw_max_cell"]) for row in raw_post_change_rows]
    ida_raw_draws = raw_bootstrap_draws(half_totals, IDA_START, BOOTSTRAP_SEED + 100)
    reference_raw_draws = []
    for index, row in enumerate(raw_post_change_rows):
        reference_raw_draws.append(
            raw_bootstrap_draws(
                half_totals,
                date.fromisoformat(row["window_start"]),
                BOOTSTRAP_SEED + 101 + index,
            )
        )
    raw_rank_draws = 1 + np.sum(
        np.asarray(reference_raw_draws) > ida_raw_draws[None, :], axis=0
    )
    raw_bootstrap_rows = [
        {
            "estimator": "raw_full_count",
            "window_start": IDA_START.isoformat(),
            "window_label": "Hurricane Ida",
            "point": ida_raw,
            "p025": float(np.quantile(ida_raw_draws, 0.025)),
            "p975": float(np.quantile(ida_raw_draws, 0.975)),
        }
    ]
    for offset, row in enumerate(
        sorted(raw_post_change_rows, key=lambda item: float(item["raw_max_cell"]), reverse=True)[:5],
        start=1,
    ):
        source_index = raw_post_change_rows.index(row)
        values = reference_raw_draws[source_index]
        raw_bootstrap_rows.append(
            {
                "estimator": "raw_full_count",
                "window_start": row["window_start"],
                "window_label": f"top_post_change_reference_{offset}",
                "point": float(row["raw_max_cell"]),
                "p025": float(np.quantile(values, 0.025)),
                "p975": float(np.quantile(values, 0.975)),
            }
        )
    write_csv(
        SOURCE / "r15_bootstrap_window_maxima.csv",
        standardized_bootstrap_rows + raw_bootstrap_rows,
    )
    episodes = {
        row["episode"]: {
            "window_start": row["window_start"],
            "raw_max_cell": float(row["raw_max_cell"]),
            "event_n": row["event_n"],
            "reference_n": row["reference_n"],
        }
        for row in raw_rows
        if row["episode"] and row["raw_max_cell"] != ""
    }

    summary = {
        "artifact_type": "R15_AGGREGATE_REVIEW_DIAGNOSTICS",
        "source": "packaged w2_period_tally.csv.gz and locked M7B artifacts",
        "privacy_class": "aggregate-only; no narratives, addresses, identifiers, or row-level records",
        "change_date": {
            "first_nonzero_non_officer_J01_day": first_nonzero.isoformat(),
            "prechange_non_officer_J01_count": prechange_j01,
            "full_reference_windows_entirely_prechange": fully_prechange_reference_count,
            "full_reference_windows_starting_before_stage_cutoff": pre_stage_cutoff_reference_count,
            "interpretation": "empirical public-file regime break; institutional cause not identified",
        },
        "ida_common_support": {
            "event_coverage_min": min(item["event_coverage"] for item in bins),
            "event_coverage_max": max(item["event_coverage"] for item in bins),
            "reference_coverage_min": min(item["reference_coverage"] for item in bins),
            "reference_coverage_max": max(item["reference_coverage"] for item in bins),
            "event_record_weighted_coverage": sum(item["event_coverage"] * item["event_n"] for item in bins) / sum(item["event_n"] for item in bins),
            "reference_record_weighted_coverage": sum(item["reference_coverage"] * item["reference_n"] for item in bins) / sum(item["reference_n"] for item in bins),
            "event_record_count": sum(item["event_n"] for item in bins),
            "reference_record_count": sum(item["reference_n"] for item in bins),
            "would_pass_090_symmetric_gate": all(item["event_coverage"] >= 0.90 and item["reference_coverage"] >= 0.90 for item in bins),
        },
        "headline_statistics": {
            "standardized_M_max_cell": float(ida_stat["M_max_cell"]),
            "stage_era_rank": rank(float(ida_stat["M_max_cell"]), [float(row["M_max_cell"]) for row in stage_rows]),
            "stage_era_denominator_including_Ida": len(stage_rows) + 1,
            "unstandardized_M_raw": ida_raw,
            "unstandardized_stage_era_rank": rank(ida_raw, raw_stage),
            "unstandardized_stage_era_denominator_including_Ida": len(raw_stage) + 1,
            "unstandardized_post_change_rank": rank(ida_raw, raw_post_change),
            "unstandardized_post_change_denominator_including_Ida": len(raw_post_change) + 1,
        },
        "threshold_sensitivity": threshold_counts,
        "current_denominator_audit": current_rows,
        "sampling_diagnostic": bootstrap_summary,
        "sampling_window_comparisons": {
            "standardized_windows": len(standardized_bootstrap_rows),
            "raw_windows": len(raw_bootstrap_rows),
            "raw_post_change_reference_count": len(raw_post_change_rows),
            "raw_Ida_rank_bootstrap": {
                "p025": float(np.quantile(raw_rank_draws, 0.025)),
                "median": float(np.median(raw_rank_draws)),
                "p975": float(np.quantile(raw_rank_draws, 0.975)),
                "probability_rank_1": float(np.mean(raw_rank_draws == 1)),
            },
        },
        "officer_initiation": {
            "Ida_five_day_officer_share": int(event_off[0]) / (int(event_off[0]) + int(event_non[0])),
            "baseline_five_day_officer_share": int(base_off[0]) / (int(base_off[0]) + int(base_non[0])),
            "Ida_officer_J01_given_arrival": metrics(event_off)["j01_given_arrival"],
            "baseline_officer_J01_given_arrival": metrics(base_off)["j01_given_arrival"],
            "candidate_pathway": "some citizen-originated records may have been logged in a public form resembling officer-initiated records; internal initiation provenance and dispatch audit histories are required to test this",
        },
        "excluded_episodes_unstandardized": episodes,
        "optimization_intervals": {
            "reference_count": len(widths),
            "count_width_gt_0_01": sum(width > 0.01 for width in widths),
            "maximum_width": max(widths),
        },
        "parity": {"maximum_absolute_G_difference": parity, "status": "PASS"},
        "boundaries": {
            "causal_effect": False,
            "mechanism_identified": False,
            "physical_response_identified": False,
            "DV_incidence_identified": False,
        },
    }
    write_json(SOURCE / "r15_aggregate_diagnostics.json", summary)
    print("R15_EVIDENCE_BUILD_PASS")
    print(json.dumps(summary["headline_statistics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
