from __future__ import annotations

import csv
import hashlib
import json
import os
import re
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

PRIVATE_ONLY_MARKERS = tuple(
    value.lower()
    for value in (
        "LA" + "PD",
        "PRIVATE" + "_R16_2",
        "LA" + "PD_EXTRACT_ROOT",
        "private_" + "la" + "pd_measurement_audit",
        "beland ppt" + "_260521_164810",
        "May 2026" + " seminar deck",
        "Coworker_" + "Communication",
        "Online_Reviewer" + "\\R16_2",
    )
)
PUBLIC_TEXT_SUFFIXES = {
    ".bib",
    ".csv",
    ".html",
    ".json",
    ".lean",
    ".md",
    ".ps1",
    ".py",
    ".sha256",
    ".tex",
    ".toml",
    ".txt",
}


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
    require(not any(relative.startswith(".git/") for relative in listed), "manifest includes Git internals")
    require(not any(marker in relative.lower() for marker in PRIVATE_ONLY_MARKERS for relative in listed), "manifest includes a private-only filename")


def pdf_pages(path: Path) -> int:
    return len(PdfReader(path).pages)


def pdf_text(path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def verify_pdfs() -> None:
    paper = PACKAGE / "paper"
    names = {
        "Public_CAD_Main_2026-08-26_R16_2.pdf",
        "Public_CAD_Empirical_Supplement_2026-08-26_R16_2.pdf",
        "Public_CAD_2026-08-26_R16_2.pdf",
        "Public_CAD_Research_Status_Note_2026-08-26_R16_2.pdf",
        "Public_CAD_Legacy_Technical_Archive_2026-08-26_R16_2.pdf",
    }
    actual = {path.name for path in paper.glob("*.pdf")}
    require(actual == names, f"unexpected PDF set: {sorted(actual)}")
    main = paper / "Public_CAD_Main_2026-08-26_R16_2.pdf"
    supplement = paper / "Public_CAD_Empirical_Supplement_2026-08-26_R16_2.pdf"
    combined = paper / "Public_CAD_2026-08-26_R16_2.pdf"
    status = paper / "Public_CAD_Research_Status_Note_2026-08-26_R16_2.pdf"
    legacy = paper / "Public_CAD_Legacy_Technical_Archive_2026-08-26_R16_2.pdf"
    require(10 <= pdf_pages(main) <= 14, "main paper is not 10--14 pages")
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


def verify_public_private_separation() -> None:
    for path in PACKAGE.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(PACKAGE)
        if relative.parts and relative.parts[0] in {".git", "tmp"}:
            continue
        relative_lower = relative.as_posix().lower()
        require(
            not any(marker in relative_lower for marker in PRIVATE_ONLY_MARKERS),
            f"private-only filename entered public package: {relative}",
        )
        if path.suffix.lower() in PUBLIC_TEXT_SUFFIXES:
            content = windows_safe_path(path).read_text(encoding="utf-8", errors="ignore").lower()
            require(
                not any(marker in content for marker in PRIVATE_ONLY_MARKERS),
                f"private-only content entered public package: {relative}",
            )
    for path in (PACKAGE / "paper").glob("*.pdf"):
        content = pdf_text(path).lower()
        require(
            not any(marker in content for marker in PRIVATE_ONLY_MARKERS),
            f"private-only content entered public PDF: {path.name}",
        )


def verify_main_source() -> None:
    text = (PACKAGE / "source" / "main_paper_r16_2.tex").read_text(encoding="utf-8")
    forbidden = (
        "R12",
        "R13",
        "R14",
        "Paper R15",
        "Paper R16",
        "previous version",
        "referee",
        "post-review",
        "was inaccurate",
        "original estimator",
        r"U_{\mathrm{direct}}",
        r"U_{\mathrm{full}}",
        "Q upper",
        "D upper",
        "threshold-sensitive",
        "alternating_phase",
        "rank 1/152",
        r"rank $1/152$",
        r"J_{01}",
    )
    lower = text.lower()
    require(not any(term.lower() in lower for term in forbidden), "main paper contains revision-history language")
    framing_forbidden = (
        "beland ppt",
        "May seminar",
        "Table 6",
        "Table 8",
        "LA" + "PD extract",
        "contaminated",
        "artifact",
        "invalid",
        "the authors failed",
        "Professor Beland should",
        "the seminar deck is wrong",
        "failure",
    )
    require(
        not any(term.lower() in lower for term in framing_forbidden),
        "main paper contains forbidden critical or private framing",
    )
    required = (
        "53.2 percentage points",
        "larger than all 151 post-change ordinary-week comparisons",
        "43.4 percent on 31 August",
        "49.3 percent on 1 September",
        "65.4 percent in 2024",
        "66.0 percent in 2025",
        "66.8 percent in the 2026 snapshot",
        "conditional window-wise multinomial bootstrap",
        "This post-change set was defined after the July transition was identified",
        "The standardized result is therefore secondary",
        "The supplement calls this the stage-era set",
        "public missing-dispatch share",
        "one-day 10 September excursion to 34.7 percent",
        "three of the four public configurations",
        "retaining every second window removes adjacent overlap",
        "Data and code availability",
        "Yuwen Zhu",
        "Environmental shocks can affect both police-service production and the administrative observation process",
        "response clock",
        "endpoint coverage",
        "call-initiation",
        "priority definition",
        "construct validity",
        "Validating police-service measures under environmental and system stress",
        "That no call activity or officer action occurred",
        "mapping from officer-initiated activity to the released public record",
        "What the validation supports",
        "Are documented initiation streams separated and stable",
        "What are the start and end points of the response clock",
        "The New Orleans evidence directly motivates the first two checks",
        "Call volume &",
        "Response time &",
        "Priority split &",
        "Police activity/coverage &",
        "The same validation logic applies when heat, smoke, pollution, outages, or disasters",
    )
    for phrase in required:
        require(phrase in text, f"main paper missing consistency phrase: {phrase}")
    require("Cristobal" not in text, "main paper retains the supplementary Cristobal comparison")
    requirements = (PACKAGE / "requirements.txt").read_text(encoding="utf-8").lower()
    require("pandas" not in requirements, "requirements incorrectly claim pandas")
    builder = (PACKAGE / "scripts" / "build_r15_evidence.py").read_text(encoding="utf-8")
    require('STATES = ("J00", "J10", "J01", "J11")' in builder, "builder does not declare exactly four states")
    for phrase in ("field-presence topology", "record-production discontinuity", "all-record, full-count"):
        require(phrase not in text, f"main paper retains superseded wording: {phrase}")
    require(text.count(r"\begin{figure}") == 2, "main paper does not contain exactly two figures")
    require(text.count(r"\begin{equation}") <= 2, "main paper contains more than two equations")
    abstract = text.split(r"\begin{plainbox}[title=Abstract]", 1)[1].split(r"\end{plainbox}", 1)[0]
    conclusion = text.split(r"\section{Conclusion}", 1)[1].split(r"\bibliographystyle", 1)[0]
    abstract_words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", abstract)
    conclusion_words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", conclusion)
    require(len(abstract_words) < 190, f"abstract is not below 190 words: {len(abstract_words)}")
    require(len(conclusion_words) < 250, f"conclusion is not below 250 words: {len(conclusion_words)}")


def verify_r16_release() -> None:
    obj = load_json(PACKAGE / "source" / "r16_2_release_metadata.json")
    require(obj["artifact_type"] == "R16_2_FRAMING_RELEASE_METADATA", "R16.2 metadata type changed")
    require(obj["paper_version"] == "R16.2", "paper version changed")
    require(obj["scientific_results_version"] == "R15.1", "scientific-results version changed")
    require(obj["predecessor_commit"] == "7d2654525609c2e8eda6580d2572f6db0699fadd", "R16.1 predecessor changed")
    require(obj["editorial_successor"] is True, "R16.2 is not marked as an editorial successor")
    require(obj["framing_successor"] is True, "R16.2 is not marked as a framing successor")
    require(obj["numerical_results_changed"] is False, "R16.2 incorrectly marks numerical change")
    version = (PACKAGE / "VERSION.txt").read_text(encoding="utf-8")
    require("Paper version: R16.2" in version, "VERSION.txt paper version mismatch")
    require("Scientific-results version: R15.1" in version, "VERSION.txt results version mismatch")
    expected_hashes = obj["frozen_r15_source_sha256"]
    current_files = {
        current.name: current
        for current in sorted((PACKAGE / "source").glob("r15*"))
        if current.is_file()
    }
    require(set(current_files) == set(expected_hashes), "frozen R15.1 source inventory changed")
    for name, expected_hash in expected_hashes.items():
        current = current_files[name]
        require(sha256(current) == expected_hash, f"frozen R15.1 object changed: {name}")


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
    walked_root = windows_safe_path(SNAPSHOT)
    rows: dict[str, str] = {}
    for directory, _, names in os.walk(walked_root):
        directory_path = Path(directory)
        for name in names:
            path = directory_path / name
            rows[path.relative_to(walked_root).as_posix()] = sha256(path)
    digest = hashlib.sha256()
    for relative, file_hash in sorted(rows.items()):
        digest.update(relative.encode("utf-8") + b"\0" + file_hash.encode("ascii") + b"\n")
    require(len(rows) == receipt["file_count"], "snapshot parity file count changed")
    require(digest.hexdigest() == receipt["tree_sha256"], "frozen reproduction snapshot hash changed")


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
        shutil.copytree(windows_safe_path(formal), temporary_formal)
        temporary_phase = temporary_pilot / phase_relative
        temporary_phase.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(windows_safe_path(PILOT / phase_relative), temporary_phase)
        for relative in ("certificates/verify_certificates.py", "enumeration/verify_witness_regimes.py"):
            subprocess.run([sys.executable, str(temporary_formal / relative)], cwd=temporary_formal, check=True)


def main() -> None:
    verify_manifest()
    verify_pdfs()
    verify_public_private_separation()
    verify_main_source()
    verify_r16_release()
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
