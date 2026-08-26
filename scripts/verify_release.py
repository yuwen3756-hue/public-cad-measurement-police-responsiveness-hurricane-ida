from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parents[1]
SNAPSHOT = PACKAGE / "reproduction" / "repository_snapshot"
PILOT = SNAPSHOT / "pilot_911_dv"
CANDIDATE = (
    PILOT
    / "experiments"
    / "nola_2020-01-01_2024-12-31_beland_plus_wave4r"
    / "candidate"
)


def windows_safe_path(path: Path) -> Path:
    if os.name == "nt" and not str(path).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(path))
    return path


def load_json(path: Path):
    return json.loads(windows_safe_path(path).read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with windows_safe_path(path).open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def manifest_path(relative: str) -> Path:
    return windows_safe_path(PACKAGE.joinpath(*relative.split("/")))


def verify_manifest() -> None:
    manifest = PACKAGE / "PACKAGE_MANIFEST.sha256"
    require(manifest.is_file(), "PACKAGE_MANIFEST.sha256 is missing")
    entries = 0
    listed = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        path = manifest_path(relative)
        require(path.is_file(), f"manifest file missing: {relative}")
        require(sha256(path) == expected, f"manifest hash mismatch: {relative}")
        entries += 1
        listed.add(relative)
    require(entries > 25, "manifest is unexpectedly small")
    for required in ("README.md", ".gitattributes", "REPRODUCTION_SNAPSHOT_PARITY.json"):
        require(required in listed, f"manifest scope missing {required}")


def pdf_pages(path: Path) -> int:
    return len(PdfReader(path).pages)


def pdf_text(path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def verify_pdfs() -> None:
    paper = PACKAGE / "paper"
    names = {
        "Beland_Current_Status_Main_2026-08-25_R15_1.pdf",
        "Beland_Current_Status_Empirical_Supplement_2026-08-25_R15_1.pdf",
        "Beland_Current_Status_2026-08-25_R15_1.pdf",
        "Beland_Research_Status_Note_2026-08-25_R15_1.pdf",
        "Beland_Legacy_Technical_Archive_2026-08-25_R15_1.pdf",
    }
    actual = {path.name for path in paper.glob("*.pdf")}
    require(actual == names, f"unexpected PDF set: {sorted(actual)}")
    main = paper / "Beland_Current_Status_Main_2026-08-25_R15_1.pdf"
    supplement = paper / "Beland_Current_Status_Empirical_Supplement_2026-08-25_R15_1.pdf"
    combined = paper / "Beland_Current_Status_2026-08-25_R15_1.pdf"
    status = paper / "Beland_Research_Status_Note_2026-08-25_R15_1.pdf"
    legacy = paper / "Beland_Legacy_Technical_Archive_2026-08-25_R15_1.pdf"
    require(9 <= pdf_pages(main) <= 16, "main paper page count outside expected range")
    require(12 <= pdf_pages(supplement) <= 18, "empirical supplement is not 12--18 pages")
    require(pdf_pages(status) == 1, "research status note is not one page")
    require(pdf_pages(legacy) >= 25, "legacy archive is unexpectedly short")
    require(
        pdf_pages(combined) == pdf_pages(main) + pdf_pages(supplement),
        "combined professor PDF is not main plus empirical supplement",
    )
    combined_text = pdf_text(combined)
    require("Public CAD Is Not Operational Ground Truth" in combined_text, "combined PDF missing title")
    require("Online Empirical and Methods Supplement" in combined_text, "combined PDF missing supplement")
    require("Legacy Mathematical and Formal-Verification Archive" not in combined_text, "legacy archive was appended to professor PDF")


def verify_main_source() -> None:
    text = (PACKAGE / "source" / "main_paper_r15_1.tex").read_text(encoding="utf-8")
    forbidden = ("R12", "R13", "R14", "previous version", "referee", "post-review", "was inaccurate", "original estimator")
    lower = text.lower()
    require(not any(term.lower() in lower for term in forbidden), "main paper contains revision-history language")
    required = (
        "This paper measures a more limited object",
        "136,712 of 207,050",
        "1,117 of 122,720",
        "137,829 of 329,770",
        "65.4 percent in 2024, 66.0 percent in 2025, and 66.8 percent",
        "rank $1/152$ including Ida",
        "conditional window-wise multinomial bootstrap",
        "This post-change universe was defined after the July break was identified",
    )
    for phrase in required:
        require(phrase in text, f"main paper missing consistency phrase: {phrase}")
    requirements = (PACKAGE / "requirements.txt").read_text(encoding="utf-8").lower()
    require("pandas" not in requirements, "requirements incorrectly claim pandas")
    builder = (PACKAGE / "scripts" / "build_r15_evidence.py").read_text(encoding="utf-8")
    require('STATES = ("J00", "J10", "J01", "J11")' in builder, "builder does not declare exactly four states")
    for phrase in ("field-presence topology", "record-production discontinuity", "all-record, full-count"):
        require(phrase not in text, f"main paper retains superseded wording: {phrase}")


def verify_r15() -> None:
    obj = load_json(PACKAGE / "source" / "r15_aggregate_diagnostics.json")
    require(obj["artifact_type"] == "R15_AGGREGATE_REVIEW_DIAGNOSTICS", "diagnostic type changed")
    require(obj["change_date"]["first_nonzero_non_officer_J01_day"] == "2021-07-28", "break date changed")
    require(obj["change_date"]["prechange_non_officer_J01_count"] == 0, "pre-break J01 count changed")
    require(obj["change_date"]["full_reference_windows_entirely_prechange"] == 66, "pre-break reference count changed")
    require(obj["change_date"]["full_reference_windows_starting_before_stage_cutoff"] == 64, "pre-stage reference count changed")
    require(obj["ida_common_support"]["would_pass_090_symmetric_gate"] is False, "support-gate finding changed")
    require(abs(obj["headline_statistics"]["standardized_M_max_cell"] - 0.5071816170350076) <= 1e-12, "M_max changed")
    require(obj["headline_statistics"]["stage_era_rank"] == 1, "stage-era rank changed")
    require(obj["headline_statistics"]["unstandardized_post_change_rank"] == 1, "post-change rank changed")
    require(obj["headline_statistics"]["unstandardized_post_change_denominator_including_Ida"] == 152, "post-change denominator changed")
    require(obj["threshold_sensitivity"]["FULL_QUALIFIED_REFERENCE"]["exceeding_cells"] == 9, "full threshold count changed")
    require(obj["threshold_sensitivity"]["STAGE_ERA_MATCHED_REFERENCE"]["exceeding_cells"] == 8, "stage threshold count changed")
    require(obj["threshold_sensitivity"]["SAME_SEASON_STAGE_REFERENCE"]["exceeding_cells"] == 9, "same-season threshold count changed")
    require(obj["sampling_diagnostic"]["replicates"] == 4000, "resampling count changed")
    rank_boot = obj["sampling_window_comparisons"]["raw_Ida_rank_bootstrap"]
    require(rank_boot == {"median": 1.0, "p025": 1.0, "p975": 1.0, "probability_rank_1": 1.0}, "raw rank bootstrap changed")
    require(obj["sampling_window_comparisons"]["raw_post_change_reference_count"] == 151, "raw bootstrap universe changed")
    require(obj["parity"]["status"] == "PASS" and obj["parity"]["maximum_absolute_G_difference"] <= 1e-12, "G parity failed")
    require(obj["boundaries"] == {
        "DV_incidence_identified": False,
        "causal_effect": False,
        "mechanism_identified": False,
        "physical_response_identified": False,
    }, "interpretation boundary changed")
    current = {(str(row["year"]), row["denominator"]): row for row in obj["current_denominator_audit"]}
    require(current[("2025", "non_officer")]["rows"] == 207050, "2025 non-officer denominator changed")
    require(current[("2025", "non_officer")]["dispatch_present"] == 136712, "2025 non-officer numerator changed")
    require(current[("2025", "officer")]["dispatch_present"] == 1117, "2025 officer numerator changed")
    require(current[("2025", "all_public_rows")]["dispatch_present"] == 137829, "2025 all-row numerator changed")


def verify_source_audit() -> None:
    obj = load_json(PACKAGE / "source" / "r15_public_source_audit.json")
    require(obj["artifact_type"] == "R15_PUBLIC_SOURCE_LINEAGE_AND_JULY_BREAK_AUDIT", "source-audit type changed")
    annual = {int(row["year"]): row for row in obj["annual_sources"]}
    expected = {2020: 432892, 2021: 428315, 2022: 354207, 2023: 325091, 2024: 327696}
    require({year: row["row_count"] for year, row in annual.items()} == expected, "annual raw row counts changed")
    require(all(row["retrieval_date_recorded"] == "not recorded in monthly cache" for row in annual.values()), "retrieval-date limitation changed")
    rows = read_csv(PACKAGE / "source" / "r15_raw_july_25_31_audit.csv")
    keyed = {(row["date"], row["initiation_stream"]): row for row in rows}
    require(keyed[("2021-07-27", "non_officer")]["J01"] == "0", "pre-break raw J01 changed")
    require(keyed[("2021-07-28", "non_officer")]["J01"] == "34", "first-day raw J01 changed")
    require(keyed[("2021-07-27", "officer")]["dispatch_nonblank"] == "479", "27 July officer dispatch count changed")
    require(keyed[("2021-07-28", "officer")]["dispatch_nonblank"] == "230", "28 July officer dispatch count changed")
    require(keyed[("2021-07-29", "officer")]["dispatch_nonblank"] == "5", "29 July officer dispatch count changed")
    require(all(row["dispatch_nonblank"] == row["dispatch_parseable"] for row in rows), "nonblank dispatch parseability changed")
    require(all(row["arrival_nonblank"] == row["arrival_parseable"] for row in rows), "nonblank arrival parseability changed")
    script = (PACKAGE / "scripts" / "audit_public_source_lineage.py").read_text(encoding="utf-8")
    require("--source-root" in script and "BELAND_PUBLIC_SOURCE_ROOT" in script, "source audit is not portable")
    require("cache_mtime_utc" not in script, "source audit retains inaccurate UTC field name")


def verify_r15_1_refinements() -> None:
    obj = load_json(PACKAGE / "source" / "r15_1_refinement_diagnostics.json")
    require(obj["paper_version"] == "R15.1", "R15.1 refinement version changed")
    require(obj["scientific_results_version"] == "R15", "scientific-results version changed")
    require(obj["ida_time_path_days"] == 22, "Ida time path length changed")
    require(obj["raw_aggregate_parity_rows"] == 14, "raw/aggregate parity row count changed")
    require(obj["raw_aggregate_state_cells_checked"] == 56, "raw/aggregate parity cell count changed")
    require(obj["raw_aggregate_parity_status"] == "MATCH", "raw/aggregate parity failed")
    phases = obj["alternating_nonoverlap_sensitivity"]
    require(
        [(row["reference_count"], row["denominator_including_Ida"], row["Ida_rank_including_Ida"]) for row in phases]
        == [(76, 77, 1), (75, 76, 1)],
        "alternating non-overlap sensitivity changed",
    )
    parity = read_csv(PACKAGE / "source" / "r15_1_raw_aggregate_parity.csv")
    require(len(parity) == 14, "raw/aggregate parity artifact is incomplete")
    require(all(row["parity_status"] == "MATCH" for row in parity), "raw/aggregate parity artifact contains mismatch")
    for row in parity:
        for state in ("J00", "J10", "J01", "J11"):
            require(row[f"raw_{state}"] == row[f"aggregate_{state}"], f"raw/aggregate {state} mismatch")


def verify_snapshot_parity() -> None:
    receipt = load_json(PACKAGE / "REPRODUCTION_SNAPSHOT_PARITY.json")
    require(receipt["byte_identical"] is True, "snapshot parity is not byte-identical")
    require(receipt["file_count"] > 50, "snapshot parity file count is unexpectedly small")


def verify_m7b() -> None:
    obj = load_json(CANDIDATE / "m7b_same_estimator_reference_geometry" / "M7B_INDEPENDENT_REPLICATION.json")
    require(obj["status"] == "PASS", "M7B replication is not PASS")
    require(obj["reference"]["n"] == 217, "M7B reference count changed")
    require(obj["ida"]["parity_max_abs"] <= 1e-10, "M7B Ida parity exceeds tolerance")


def verify_m7d_e() -> None:
    obj = load_json(CANDIDATE / "m7d_e_within_disposition_dispatch_observability" / "M7D_E_INDEPENDENT_REPLICATION.json")
    require(obj["overall"] == "PASS", "M7D-E replication is not PASS")
    require(obj["independent_identity_max_abs_residual"] <= 1e-12, "M7D-E identity residual exceeds tolerance")
    require(obj["primary_tables_used_as_numeric_inputs"] is False, "M7D-E independence boundary changed")


def verify_m8p() -> None:
    experiment = PILOT / "experiments" / "nola_2025-01-01_2026-08-11_m8p_public_observability_replay"
    validation = load_json(experiment / "metadata" / "validation_report.json")
    require(validation["status"] == "PASS", "M8P validation is not PASS")
    require(len(validation["checks"]) == 20 and all(row["passed"] for row in validation["checks"]), "M8P checks changed")
    results = load_json(experiment / "data" / "processed" / "m8p_results.json")
    require(results["identified_set_comparison"]["strict_contractions_proved"] == [], "M8P contraction boundary changed")


def verify_formal_supplements() -> None:
    formal = PILOT / "formal_verification_r11_1"
    phase_relative = Path(
        "experiments/nola_2020-01-01_2024-12-31_beland_plus_wave4r/"
        "candidate/m8d_r1_conditional_identification_frontier_repair/"
        "M8D_R1_PHASE_DIAGRAM.json"
    )
    with tempfile.TemporaryDirectory(prefix="beland_formal_") as temporary:
        temporary_pilot = Path(temporary) / "pilot_911_dv"
        temporary_formal = temporary_pilot / "formal_verification_r11_1"
        shutil.copytree(formal, temporary_formal)
        temporary_phase = temporary_pilot / phase_relative
        temporary_phase.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(windows_safe_path(PILOT / phase_relative), temporary_phase)
        for relative in ("certificates/verify_certificates.py", "enumeration/verify_witness_regimes.py"):
            subprocess.run([sys.executable, str(temporary_formal / relative)], cwd=temporary_formal, check=True)


def main() -> None:
    verify_manifest()
    verify_pdfs()
    verify_main_source()
    verify_r15()
    verify_source_audit()
    verify_r15_1_refinements()
    verify_snapshot_parity()
    verify_m7b()
    verify_m7d_e()
    verify_m8p()
    verify_formal_supplements()
    print("RELEASE_VERIFICATION_PASS")


if __name__ == "__main__":
    main()
