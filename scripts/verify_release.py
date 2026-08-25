from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SNAPSHOT = PACKAGE / "reproduction" / "repository_snapshot"
PILOT = SNAPSHOT / "pilot_911_dv"
CANDIDATE = (
    PILOT
    / "experiments"
    / "nola_2020-01-01_2024-12-31_beland_plus_wave4r"
    / "candidate"
)


def load_json(path: Path):
    return json.loads(windows_safe_path(path).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def windows_safe_path(path: Path) -> Path:
    if os.name == "nt" and not str(path).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(path))
    return path


def manifest_path(relative: str) -> Path:
    return windows_safe_path(PACKAGE.joinpath(*relative.split("/")))


def verify_manifest() -> None:
    manifest = PACKAGE / "PACKAGE_MANIFEST.sha256"
    require(manifest.is_file(), "PACKAGE_MANIFEST.sha256 is missing")
    entries = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        path = manifest_path(rel)
        require(path.is_file(), f"manifest file missing: {rel}")
        require(sha256(path) == expected, f"manifest hash mismatch: {rel}")
        entries += 1
    require(entries > 20, "manifest is unexpectedly small")


def verify_pdfs() -> None:
    expected = {
        "Beland_Current_Status_Main_2026-08-24_R12_2.pdf",
        "Beland_Current_Status_Appendix_2026-08-24_R12_2.pdf",
        "Beland_Current_Status_2026-08-24_R12_2.pdf",
    }
    actual = {path.name for path in (PACKAGE / "paper").glob("*.pdf")}
    require(actual == expected, f"unexpected PDF set: {sorted(actual)}")


def verify_m7b() -> None:
    obj = load_json(CANDIDATE / "m7b_same_estimator_reference_geometry" / "M7B_INDEPENDENT_REPLICATION.json")
    require(obj["status"] == "PASS", "M7B replication is not PASS")
    require(obj["reference"]["n"] == 217, "M7B reference count changed")
    require(obj["ida"]["parity_max_abs"] <= 1e-10, "M7B Ida parity exceeds tolerance")
    require(obj["ida"]["interval"][0] > obj["reference"]["interval_summary"]["upper_max"], "M7B Ida interval overlaps the reference envelope")
    expected_n = {
        "FULL_QUALIFIED_REFERENCE:all": 217,
        "STAGE_ERA_MATCHED_REFERENCE:all": 153,
        "SAME_SEASON_STAGE_REFERENCE:all": 86,
    }
    for key, n in expected_n.items():
        row = obj["ranks"][key]
        require(row["n"] == n, f"M7B rank-set size changed: {key}")
        require(row["definitely_ge"] == 0 and row["possibly_ge"] == 0, f"M7B rank changed: {key}")


def verify_m7d_e() -> None:
    obj = load_json(CANDIDATE / "m7d_e_within_disposition_dispatch_observability" / "M7D_E_INDEPENDENT_REPLICATION.json")
    require(obj["overall"] == "PASS", "M7D-E replication is not PASS")
    require(obj["independent_identity_max_abs_residual"] <= 1e-12, "M7D-E identity residual exceeds tolerance")
    require(obj["independent_parent_parity_max_abs_residual"] <= 1e-12, "M7D-E parent parity exceeds tolerance")
    require(obj["primary_tables_used_as_numeric_inputs"] is False, "M7D-E independence boundary changed")


def verify_m8p() -> None:
    exp = PILOT / "experiments" / "nola_2025-01-01_2026-08-11_m8p_public_observability_replay"
    validation = load_json(exp / "metadata" / "validation_report.json")
    require(validation["status"] == "PASS", "M8P validation is not PASS")
    require(len(validation["checks"]) == 20, "M8P check count changed")
    require(all(row["passed"] for row in validation["checks"]), "M8P has a failed check")
    results = load_json(exp / "data" / "processed" / "m8p_results.json")
    require(results["decision"] == "M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED", "M8P decision changed")
    require(results["identified_set_comparison"]["strict_contractions_proved"] == [], "M8P strict-contraction boundary changed")
    statuses = {row["m8d_structural_witness_status"] for row in results["module_crosswalk_semantic_firewall"].values()}
    require(statuses == {"CLOSED"}, "M8P structural witness status changed")


def verify_formal_supplements() -> None:
    formal = PILOT / "formal_verification_r11_1"
    phase_relative = Path(
        "experiments/nola_2020-01-01_2024-12-31_beland_plus_wave4r/"
        "candidate/m8d_r1_conditional_identification_frontier_repair/"
        "M8D_R1_PHASE_DIAGRAM.json"
    )
    with tempfile.TemporaryDirectory(prefix="beland_formal_") as temp:
        temp_pilot = Path(temp) / "pilot_911_dv"
        temp_formal = temp_pilot / "formal_verification_r11_1"
        shutil.copytree(formal, temp_formal)
        temp_phase = temp_pilot / phase_relative
        temp_phase.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(windows_safe_path(PILOT / phase_relative), temp_phase)
        for relative in ("certificates/verify_certificates.py", "enumeration/verify_witness_regimes.py"):
            subprocess.run([sys.executable, str(temp_formal / relative)], cwd=temp_formal, check=True)


def main() -> None:
    verify_manifest()
    verify_pdfs()
    verify_m7b()
    verify_m7d_e()
    verify_m8p()
    verify_formal_supplements()
    print("RELEASE_VERIFICATION_PASS")


if __name__ == "__main__":
    main()
