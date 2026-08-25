"""Exhaustively enumerate and independently check the frozen 54 regimes."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "witness_regimes.json"
PILOT_ROOT = ROOT.parent.parent


class RegimeError(ValueError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def legal(regime: dict[str, str], spec: dict[str, Any]) -> bool:
    order = spec["level_order"]
    rule = spec["dependency"]
    return order[regime[rule["left"]]] <= order[regime[rule["right"]]]


def regime_id(regime: dict[str, str], spec: dict[str, Any]) -> str:
    order = spec["level_order"]
    return "_".join(f"{module}{order[regime[module]]}" for module in spec["modules"])


def enumerate_legal(spec: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for values in itertools.product(spec["levels"], repeat=len(spec["modules"])):
        regime = dict(zip(spec["modules"], values, strict=True))
        if legal(regime, spec):
            rows.append(regime)
    return rows


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    rows = enumerate_legal(spec)
    ids = [regime_id(row, spec) for row in rows]
    if len(rows) != spec["expected_legal_regime_count"]:
        raise RegimeError(f"expected 54 legal regimes, observed {len(rows)}")
    if len(set(ids)) != len(ids):
        raise RegimeError("regime identifiers are not unique")
    if any(not legal(row, spec) for row in rows):
        raise RegimeError("enumeration contains an illegal regime")

    illegal_probe = {"B": "CLOSED", "Q": "CLOSED", "P": "QUALIFIED", "C": "CLOSED"}
    if legal(illegal_probe, spec):
        raise RegimeError("negative dependency check failed")

    source_meta = spec["frozen_source"]
    source_path = PILOT_ROOT / source_meta["path_from_pilot_root"]
    if sha256(source_path) != source_meta["sha256"]:
        raise RegimeError("frozen source hash mismatch")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    if source["legal_regime_count"] != len(rows):
        raise RegimeError("frozen source count mismatch")

    expected_by_id = {regime_id(row, spec): row for row in rows}
    observed_by_id = {row["regime_id"]: row for row in source["regimes"]}
    if set(expected_by_id) != set(observed_by_id):
        raise RegimeError("frozen source is incomplete or contains extra regimes")
    for identifier, expected in expected_by_id.items():
        observed = observed_by_id[identifier]
        if observed["regime"] != expected:
            raise RegimeError(f"state assignment mismatch for {identifier}")
        active = sum(value != "CLOSED" for value in expected.values())
        if active < 2:
            if observed["CROSS_MODULE_RELATION_STATUS"] != "NOT_APPLICABLE":
                raise RegimeError(f"single-module coupling mismatch for {identifier}")
        else:
            if observed["CROSS_MODULE_RELATION_STATUS"] != "UNCOUPLED":
                raise RegimeError(f"default coupling mismatch for {identifier}")
            statuses = {variant["status"] for variant in observed["coupling_variants"]}
            if statuses != {"UNCOUPLED", "PARTIAL_MAP", "QUALIFIED_MAP"}:
                raise RegimeError(f"coupling variants incomplete for {identifier}")
            qualified = next(
                variant for variant in observed["coupling_variants"]
                if variant["status"] == "QUALIFIED_MAP"
            )
            if qualified["propagation_identified"] is not True:
                raise RegimeError(f"qualified map semantics mismatch for {identifier}")

    multi_module = sum(
        sum(value != "CLOSED" for value in row.values()) >= 2 for row in rows
    )
    if multi_module != spec["expected_multi_module_regime_count"]:
        raise RegimeError("multi-module regime count mismatch")

    fingerprint = hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()
    print(json.dumps({
        "status": "EXHAUSTIVELY_ENUMERATED",
        "legal_regime_count": len(rows),
        "multi_module_regime_count": multi_module,
        "unique": True,
        "complete_against_frozen_source": True,
        "dependency_negative_check": "REJECTED_AS_REQUIRED",
        "regime_id_fingerprint_sha256": fingerprint,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
