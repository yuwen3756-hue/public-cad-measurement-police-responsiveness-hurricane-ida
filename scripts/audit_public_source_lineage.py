"""Create privacy-safe first-hand lineage and July-2021 raw-field audits.

The script reads the canonical official DataNOLA cache in ``source_data`` and
writes only aggregate counts, format classes, dates, and cryptographic hashes.
It never writes row-level records, addresses, narratives, or identifiers.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
PILOT = Path(__file__).resolve().parents[3]
SOURCE_OUT = PACKAGE / "source"
SOURCE_ROOT = PILOT / "source_data" / "socrata"
DATASETS = {
    2020: ("hp7u-i9hf", "nola_hp7u-i9hf"),
    2021: ("3pha-hum9", "nola_3pha-hum9"),
    2022: ("nci8-thrr", "nola_nci8-thrr"),
    2023: ("pc5d-tvaw", "nola_pc5d-tvaw"),
    2024: ("2zcj-b6ts", "nola_2zcj-b6ts"),
}
ISO_T = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?$")
ISO_SPACE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?$")
MISSING = {"", "null", "none", "nan", "nat"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_local(value: str | None) -> datetime | None:
    text = "" if value is None else str(value).strip()
    if text.lower() in MISSING:
        return None
    try:
        return datetime.fromisoformat(text.replace(" ", "T", 1))
    except ValueError:
        return None


def present(value: str | None) -> bool:
    return ("" if value is None else str(value).strip()).lower() not in MISSING


def format_class(value: str | None) -> str:
    text = "" if value is None else str(value).strip()
    if text.lower() in MISSING:
        return "missing_sentinel"
    if ISO_T.fullmatch(text):
        return "iso_T_fractional" if "." in text else "iso_T_seconds"
    if ISO_SPACE.fullmatch(text):
        return "iso_space_fractional" if "." in text else "iso_space_seconds"
    return "other_nonblank"


def monthly_paths(year: int, folder: str) -> list[Path]:
    root = SOURCE_ROOT / folder / str(year) / "cad_operational"
    paths = sorted(root.glob(f"cad_operational_{year}-??.csv.gz"))
    if len(paths) != 12:
        raise FileNotFoundError(f"Expected 12 monthly files for {year}, found {len(paths)}")
    return paths


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    SOURCE_OUT.mkdir(parents=True, exist_ok=True)
    annual_rows: list[dict] = []
    file_bindings: dict[str, list[dict]] = {}
    july_rows: dict[tuple[str, str], Counter] = defaultdict(Counter)
    july_formats: dict[str, Counter] = defaultdict(Counter)

    for year, (dataset_id, folder) in DATASETS.items():
        paths = monthly_paths(year, folder)
        row_count = 0
        min_created: datetime | None = None
        max_created: datetime | None = None
        bindings = []
        bundle = hashlib.sha256()
        for path in paths:
            file_hash = sha256(path)
            bundle.update(path.name.encode("utf-8") + b"\0" + file_hash.encode("ascii") + b"\n")
            bindings.append(
                {
                    "file": path.name,
                    "sha256": file_hash,
                    "bytes": path.stat().st_size,
                    "cache_mtime_utc": datetime.fromtimestamp(
                        path.stat().st_mtime
                    ).astimezone().isoformat(),
                }
            )
            with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                normalized = {name.lower(): name for name in (reader.fieldnames or [])}
                required = {"timecreate", "timedispatch", "timearrive", "selfinitiated"}
                if not required.issubset(normalized):
                    raise RuntimeError(f"Missing required columns in {path.name}: {sorted(required - set(normalized))}")
                for raw in reader:
                    row = {key: raw.get(name, "") for key, name in normalized.items()}
                    row_count += 1
                    created = parse_local(row.get("timecreate"))
                    if created is not None:
                        min_created = created if min_created is None else min(min_created, created)
                        max_created = created if max_created is None else max(max_created, created)
                    if year != 2021 or created is None or not (
                        datetime(2021, 7, 25) <= created < datetime(2021, 8, 1)
                    ):
                        continue
                    initiation = str(row.get("selfinitiated", "")).strip().upper()
                    stream_name = "non_officer" if initiation == "N" else "officer" if initiation == "Y" else "other"
                    key = (created.date().isoformat(), stream_name)
                    counts = july_rows[key]
                    counts["rows"] += 1
                    dispatch_present = present(row.get("timedispatch"))
                    arrival_present = present(row.get("timearrive"))
                    dispatch_parsed = parse_local(row.get("timedispatch"))
                    arrival_parsed = parse_local(row.get("timearrive"))
                    counts["dispatch_nonblank"] += int(dispatch_present)
                    counts["dispatch_parseable"] += int(dispatch_parsed is not None)
                    counts["arrival_nonblank"] += int(arrival_present)
                    counts["arrival_parseable"] += int(arrival_parsed is not None)
                    arrival_valid = (
                        arrival_parsed is not None and created is not None and arrival_parsed >= created
                    )
                    counts["arrival_valid_ge_create"] += int(arrival_valid)
                    state = f"J{int(dispatch_present)}{int(arrival_valid)}"
                    counts[state] += 1
                    for field in ("timecreate", "timedispatch", "timearrive"):
                        july_formats[field][format_class(row.get(field))] += 1
        annual_rows.append(
            {
                "year": year,
                "dataset_id": dataset_id,
                "official_url": f"https://data.nola.gov/d/{dataset_id}",
                "observed_min_timecreate": min_created.isoformat() if min_created else "",
                "observed_max_timecreate": max_created.isoformat() if max_created else "",
                "row_count": row_count,
                "monthly_file_count": len(paths),
                "annual_bundle_sha256": bundle.hexdigest(),
                "retrieval_date_recorded": "not recorded in monthly cache",
                "first_hand_verification_date": "2026-08-25",
                "parser_schema_version": "r15_public_lineage_v1",
            }
        )
        file_bindings[str(year)] = bindings

    daily_rows = []
    for (day, stream_name), counts in sorted(july_rows.items()):
        daily_rows.append(
            {
                "date": day,
                "initiation_stream": stream_name,
                **{name: counts[name] for name in (
                    "rows", "dispatch_nonblank", "dispatch_parseable",
                    "arrival_nonblank", "arrival_parseable", "arrival_valid_ge_create",
                    "J00", "J10", "J01", "J11",
                )},
            }
        )

    write_csv(SOURCE_OUT / "r15_annual_source_lineage.csv", annual_rows)
    write_csv(SOURCE_OUT / "r15_raw_july_25_31_audit.csv", daily_rows)
    result = {
        "artifact_type": "R15_PUBLIC_SOURCE_LINEAGE_AND_JULY_BREAK_AUDIT",
        "privacy_class": "aggregate-only; no row-level values persisted",
        "annual_sources": annual_rows,
        "monthly_file_bindings": file_bindings,
        "july_2021_source_file": file_bindings["2021"][6],
        "july_2021_format_classes": {
            field: dict(sorted(counts.items())) for field, counts in sorted(july_formats.items())
        },
        "arrival_validity_rule": "parseable timearrive greater than or equal to parseable timecreate",
        "dispatch_state_rule": "nonblank timedispatch, matching the frozen Wave-2 definition",
        "scientific_boundary": "field presence and parseability only; no physical dispatch or arrival inference",
    }
    (SOURCE_OUT / "r15_public_source_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("R15_PUBLIC_SOURCE_AUDIT_PASS")


if __name__ == "__main__":
    main()
