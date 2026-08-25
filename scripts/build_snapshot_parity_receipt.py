"""Prove that the copied reproduction snapshot is byte-identical to R14."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
PREDECESSOR = PACKAGE.parent / "beland_plus_current_status_professor_2026-08-24_r14_0_v1"
RELATIVE = Path("reproduction/repository_snapshot")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    opened = path
    if os.name == "nt" and not str(path).startswith("\\\\?\\"):
        opened = Path("\\\\?\\" + str(path.resolve()))
    with opened.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for directory, _, names in os.walk(root):
        directory_path = Path(directory)
        for name in names:
            path = directory_path / name
            rows[path.relative_to(root).as_posix()] = sha256(path)
    return dict(sorted(rows.items()))


def tree_hash(rows: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in rows.items():
        digest.update(relative.encode("utf-8") + b"\0" + file_hash.encode("ascii") + b"\n")
    return digest.hexdigest()


def main() -> None:
    predecessor_rows = inventory(PREDECESSOR / RELATIVE)
    successor_rows = inventory(PACKAGE / RELATIVE)
    if predecessor_rows != successor_rows:
        missing = sorted(set(predecessor_rows) - set(successor_rows))
        extra = sorted(set(successor_rows) - set(predecessor_rows))
        changed = sorted(
            key for key in set(predecessor_rows) & set(successor_rows)
            if predecessor_rows[key] != successor_rows[key]
        )
        raise RuntimeError(
            f"snapshot parity failed: missing={missing[:3]} extra={extra[:3]} changed={changed[:3]}"
        )
    receipt = {
        "artifact_type": "R15_REPRODUCTION_SNAPSHOT_BYTE_PARITY_RECEIPT",
        "predecessor_package": PREDECESSOR.name,
        "successor_package": PACKAGE.name,
        "relative_root": RELATIVE.as_posix(),
        "file_count": len(successor_rows),
        "tree_sha256": tree_hash(successor_rows),
        "byte_identical": True,
        "line_ending_statement": "No text normalization was performed; equality is byte-for-byte for every snapshot file.",
        "gitattributes_policy": "Top-level .gitattributes uses * -text to prevent line-ending conversion.",
    }
    (PACKAGE / "REPRODUCTION_SNAPSHOT_PARITY.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"SNAPSHOT_PARITY_PASS files={len(successor_rows)}")


if __name__ == "__main__":
    main()
