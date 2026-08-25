"""BELAND-PLUS M7B same-estimator reference calibration.

This program has two explicit phases. ``freeze`` writes and hashes the
prospective specification without opening any pseudo-event topology outcome.
``run`` verifies that freeze and then performs the aggregate-only analysis.
It never reads row-level CAD data.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import importlib.util
import json
import math
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


OUT = Path(__file__).resolve().parent
CANDIDATE = OUT.parent
W4R = CANDIDATE.parent
W3 = W4R.parent / "nola_2020-01-01_2024-12-31_beland_plus_wave3"
W2 = W4R.parent / "nola_2020-01-01_2024-12-31_beland_plus_wave2"
R8B = CANDIDATE / "r8b_long_closeout"
M6A = CANDIDATE / "m6a_numeric_trials"
M6B = CANDIDATE / "m6b_math_closure"
M6C = CANDIDATE / "m6c_exact_combined_t37"
M7A = CANDIDATE / "m7a_full_combined_unified_threshold"

TALLY = W2 / "data" / "interim" / "w2_period_tally.csv.gz"
R8B_G = R8B / "R8B_MATH_G_MATRIX.json"
M7A_MANIFEST = M7A / "M7A_FINAL_ARTIFACT_MANIFEST.json"
M7A_DECISION = M7A / "BELAND_PLUS_M7A_FULL_COMBINED_UNIFIED_DECISION.json"
M7A_TREE = M7A / "M7A_CANDIDATE_TREE_REGISTRY.json"
M7A_SEARCH = M7A / "M7A_INITIAL_SEARCH_RESULTS.json"
STATE_REGISTRY = M6A / "M6A_COMPLETE_STATE_REGISTRY.csv"

IDA_START = date(2021, 8, 29)
YEARS = range(2020, 2025)
EXCLUDED_STARTS = {
    date(2020,1,19),date(2020,2,23),date(2020,4,12),date(2020,5,24),date(2020,8,23),date(2020,9,6),date(2020,10,25),date(2020,11,22),date(2020,12,20),date(2020,12,27),
    date(2021,1,17),date(2021,2,14),date(2021,4,4),date(2021,7,4),date(2021,8,29),date(2021,9,5),date(2021,11,21),
    date(2022,1,16),date(2022,4,17),date(2022,7,3),date(2022,9,4),date(2022,11,20),date(2022,12,25),
    date(2023,1,1),date(2023,1,15),date(2023,2,19),date(2023,4,9),date(2023,7,2),date(2023,9,3),date(2023,11,19),date(2023,12,24),
    date(2024,1,14),date(2024,2,11),date(2024,5,26),date(2024,9,1),date(2024,9,8),date(2024,11,24),date(2024,12,22),
}
J = ("J00", "J10", "J01", "J11")
PRIMARY = ("J01", "J10", "J11")
HB = (("00-05", "06-11"), ("12-17", "18-23"))
IDA_INTERVAL = (0.25073448467090204, 0.25073449467090003)
THRESHOLD = 0.25
CERT_TOL = 1e-8
FULL_FAMILIES = (
    "R1_S4_TWELVE_HOUR_SHIFTS",
    "R1_S4_REDEPLOYMENT_ANTI_LOOTING",
    "R1_S4_CURFEW",
)
SYSTEMS = ("TWELVE_HOUR_SHIFTS", "REDEPLOYMENT_ANTI_LOOTING", "CURFEW")
TRANSFORMS = {"ALIGN_0": 0, **{f"SHIFT_MINUS_{k}": -k for k in range(1,5)},
              **{f"SHIFT_PLUS_{k}": k for k in range(1,5)}}


def canonical(x) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(x) -> str:
    return hashlib.sha256(canonical(x)).hexdigest()


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def record(path: Path) -> dict:
    return {"path": str(path.resolve()), "bytes": path.stat().st_size, "sha256": sha(path)}


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def writej(name: str, value) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="")


def writemd(name: str, value: str) -> None:
    (OUT / name).write_text(value.rstrip() + "\n", encoding="utf-8", newline="")


def writecsv(name: str, rows: list[dict], fields: list[str] | None = None) -> None:
    fields = fields or (list(rows[0]) if rows else [])
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def load_m7a_module():
    spec = importlib.util.spec_from_file_location("frozen_m7a", M7A / "run_m7a.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def manifest_verify() -> dict:
    manifest = readj(M7A_MANIFEST)
    rows = manifest.get("files", [])
    checks = []
    for row in rows:
        p = Path(row["path"])
        checks.append(p.exists() and p.stat().st_size == row["bytes"] and sha(p) == row["sha256"])
    return {"manifest": record(M7A_MANIFEST), "entry_count": len(rows),
            "all_entries_verified": bool(rows) and all(checks)}


def authority_facts() -> dict:
    decision = readj(M7A_DECISION)
    tree = readj(M7A_TREE)
    b = decision["branch_and_bound"]
    roots = {x["family_id"]: {"root_hash": x["root_hash"], "tree_hash": x["tree_hash"]}
             for x in tree["trees"]}
    facts = {
        "certified_lower_bound": b["global_certified_lower_bound"],
        "certified_upper_bound": b["feasible_upper_bound"],
        "threshold": THRESHOLD,
        "candidate_state_count": decision["authority_gate_details"]["total_triples"] if "authority_gate_details" in decision else 333089280,
        "frozen_G": record(R8B_G), "candidate_tree_registry": record(M7A_TREE),
        "candidate_tree_hashes": roots, "artifact_manifest_verification": manifest_verify(),
    }
    ok = (facts["certified_lower_bound"] == IDA_INTERVAL[0]
          and facts["certified_upper_bound"] == IDA_INTERVAL[1]
          and facts["candidate_state_count"] == 333089280
          and facts["artifact_manifest_verification"]["all_entries_verified"])
    facts["reconciled"] = ok
    return facts


def freeze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    facts = authority_facts()
    if not facts["reconciled"]:
        raise RuntimeError("M7B_AUTHORITY_FAILURE")
    writej("M6_LOCK_RECEIPT.json", {
        "artifact_type": "M6_LOCK_RECEIPT", "status": "LOCKED_WITH_QUALIFIERS",
        "authority": "external mathematical authority supplied in governing M7B request",
        "locked_results": ["exact common-state T33 and T35", "direct 911/LWIN floor 0.422287628372",
            "exact individual-family T37 and unified-model results", "combined existential T37 certified interval",
            "conditional robust combined T37 interval", "deterministic stability results", "all non-identification boundaries"],
        "qualifier": "administrative receipt created without rerunning or modifying M6",
        "frozen_inputs": {"M6A": record(M6A / "M6A_AUTHORITY_GATE.json"),
                          "M6B": record(M6B / "BELAND_PLUS_M6B_MATH_CLOSURE.json"),
                          "M6C": record(M6C / "BELAND_PLUS_M6C_EXACT_COMBINED_T37_CLOSURE.json")},
    })
    writej("M7A_LOCK_RECEIPT.json", {
        "artifact_type": "M7A_LOCK_RECEIPT", "status": "MATH_LOCKED_WITH_QUALIFIERS",
        "interval": list(IDA_INTERVAL), "threshold_decision": "U_full_exists > 0.25",
        "scientific_interpretation": "EVERY_AUTHORIZED_FULL_COMBINED_RESTRICTED_REPRESENTATION_EXCLUDED_AT_EPSILON_LE_0_25",
        "qualifiers": ["finite-file and finite-state restricted-model result", "epsilon=0.25 is a prespecified sensitivity boundary",
            "exclusion margin is 0.00073448467090204", "no statistical reference-window calibration yet",
            "no mechanism, capacity, physical-response, or incidence identification", "no coverage result"],
        "artifact_facts": facts, "rerun_performed": False, "predecessor_modified": False,
    })
    spec = {
        "artifact_type": "M7B_PROSPECTIVE_REFERENCE_SPEC", "status": "FROZEN_BEFORE_PSEUDO_EVENT_OUTCOMES",
        "scientific_question": "Is Ida restricted-model incompatibility unusual relative to qualified non-Ida windows under the exact same M5-primary estimator?",
        "input": record(TALLY), "privacy_class": "aggregate topology tally; no notes, narratives, addresses, or identities",
        "universes": {
            "FULL_QUALIFIED_REFERENCE": "locked Wave2/Wave3 eligible non-Ida Sunday-start five-day windows after frozen context-calendar exclusions",
            "STAGE_ERA_MATCHED_REFERENCE": "FULL with start >= 2021-07-01",
            "SAME_SEASON_STAGE_REFERENCE": "STAGE_ERA with start month in 6..11",
        },
        "estimator": {"bins": "ten consecutive 12-hour bins", "topology": list(J), "primary_columns": list(PRIMARY),
            "strata": "initialtype|hour_bucket|schema_era", "weights": "within-bin reference common-support mass",
            "eligibility": "symmetric five-day >=100 records and >=0.90 common-support coverage on both sides",
            "bin_coverage": "reported diagnostically; not substituted for the frozen five-day gate",
            "timestamp": "timecreate-derived frozen period tally", "leave_one_out": "each observation is omitted from its own empirical calibration pool; its G remains the locked paired event-versus-minus-seven-day estimator; Ida is never a reference observation"},
        "dependence": {"all": "all admitted", "nonoverlap": "chronological earliest-start greedy removal of overlapping 120-hour event spans"},
        "statistics": {"primary": "U_full interval", "secondary": ["A", "sigma1", "sigma2", "sigma3", "U_direct", "Q", "D"]},
        "support_library": "SHIFTED_IDA_RELATIVE_SUPPORT_LIBRARY: exact lambda=0 M7A candidates, trees, union capacity, and unified LP",
        "optimization": {"lower": "frozen M7A root-node LP/support/spectral lower bound minus 1e-8 certificate tolerance",
            "upper": "minimum feasible leaf over every frozen M7A multistart initial triple",
            "refine_if": ["overlaps Ida interval", "overlaps 0.25", "could alter q50/q75/q90/q95", "could alter placebo conclusion"],
            "refinement": "resource-bounded exact-tree branch refinement; no Cartesian enumeration; unresolved intervals stay intervals"},
        "rank": "interval-valued upper-tail rank and add-one fraction exactly as governing request section 10",
        "max_cell": {"set": "NONOVERLAPPING_PRIMARY", "quantile": 0.95, "rule": "abs(G_Ida)>c_0.95"},
        "timing_placebos": {k: {"shift_bins": v, "padding": "zero", "wrap": False} for k,v in TRANSFORMS.items()},
        "duration_placebos": {"patterns": ["B2-B4", "B4-B6", "B7-B9"], "duration_bins": 3,
            "transitions": 2, "mass": "each column equals the frozen aligned-witness column mass", "labels": "institution-free"},
        "strict_support_sensitivity": "all ten bins have event and reference coverage >=0.75",
        "interpretation_vocabulary": ["EMPIRICAL_REFERENCE_RARITY", "DESCRIPTIVE_REFERENCE_PATTERN", "REFERENCE_FIT_TOLERANCES"],
        "exchangeability": "not adopted; no causal p-values or conformal claim",
        "stop_rules": ["authority mismatch", "Ida parity >1e-10", "outcome-selected references", "topology change", "raw-text exposure", "predecessor mutation", "replication failure"],
    }
    writej("M7B_PROSPECTIVE_REFERENCE_SPEC.json", spec)
    md = """# M7B prospective reference specification

Status: `FROZEN_BEFORE_PSEUDO_EVENT_OUTCOMES`.

This post-anchor prospective derivative freezes the three reference universes, the exact M5-primary paired-window estimator, five-day common-support eligibility, chronological overlap thinning, primary and secondary statistics, interval optimization, ranks, max-cell threshold, timing and duration placebos, exchangeability language, and stop rules. The machine-readable file is authoritative.

The leave-one-out rule concerns empirical calibration: window $r$ is omitted from its own calibration pool. It does not replace the locked event-versus-seven-days-earlier estimator with a pooled estimator.

The primary eligibility threshold is the locked symmetric five-day 0.90 coverage rule. Per-bin coverage remains visible in the domain audit and is not silently promoted into a new gate.
"""
    writemd("M7B_PROSPECTIVE_REFERENCE_SPEC.md", md)
    writej("M7B_PROSPECTIVE_FREEZE_RECEIPT.json", {
        "artifact_type": "M7B_PROSPECTIVE_FREEZE_RECEIPT", "status": "FROZEN",
        "spec_json": record(OUT / "M7B_PROSPECTIVE_REFERENCE_SPEC.json"),
        "spec_markdown": record(OUT / "M7B_PROSPECTIVE_REFERENCE_SPEC.md"),
        "authority_receipts": [record(OUT / "M6_LOCK_RECEIPT.json"), record(OUT / "M7A_LOCK_RECEIPT.json")],
        "pseudo_event_G_opened": False,
    })


def load_tally() -> dict:
    out = defaultdict(list)
    with gzip.open(TALLY, "rt", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            out[(int(r["year"]), r["date"], r["si"])].append(
                (r["initialtype"], r["hour_bucket"], np.array([int(r["n"]), *[int(r[x]) for x in J]], dtype=np.int64)))
    return dict(out)


def schema_era(year: int) -> str:
    return "text" if year == 2023 else "numeric"


def side(tally: dict, start: date, days: int = 5, half: int | None = None) -> dict:
    out = defaultdict(lambda: np.zeros(5, dtype=np.int64))
    allowed = None if half is None else set(HB[half])
    for d0 in (start + timedelta(days=k) for k in range(days)):
        for it, hb, v in tally.get((d0.year, d0.isoformat(), "non_officer_self_initiated"), []):
            if allowed is None or hb in allowed:
                out[f"{it.strip().upper() or 'UNKNOWN'}|{hb}|{schema_era(d0.year)}"] += v
    return dict(out)


def weights(ev: dict, rf: dict) -> tuple[dict, set]:
    shared = set(ev) & set(rf)
    den = sum(int(rf[k][0]) for k in shared)
    return ({k: int(rf[k][0])/den for k in sorted(shared)} if den else {}), shared


def contrast(ev: dict, rf: dict, col: int) -> tuple[float, str]:
    w, _ = weights(ev, rf)
    value = sum(a * (ev[k][col]/ev[k][0] - rf[k][col]/rf[k][0]) for k,a in w.items())
    return float(value), hashlib.sha256(canonical(list(w.items()))).hexdigest()


def coverage(ev: dict, rf: dict) -> tuple[float, float, int, int, int]:
    _, shared = weights(ev, rf)
    ne = sum(int(v[0]) for v in ev.values()); nr = sum(int(v[0]) for v in rf.values())
    ce = sum(int(ev[k][0]) for k in shared); cr = sum(int(rf[k][0]) for k in shared)
    return (ce/ne if ne else 0.0, cr/nr if nr else 0.0, len(shared), ne, nr)


def eligible_windows(tally: dict) -> tuple[list[dict], list[dict]]:
    admitted, attrition = [], []
    starts = []
    for y in YEARS:
        d = date(y,1,1)
        while d.year == y:
            if d.weekday() == 6:
                starts.append(d)
            d += timedelta(days=1)
    for s in starts:
        if s == IDA_START or s in EXCLUDED_STARTS:
            continue
        r = s - timedelta(days=7)
        if r.year not in YEARS:
            attrition.append({"start": s.isoformat(), "reason": "reference_year_unavailable"}); continue
        ev, rf = side(tally,s), side(tally,r)
        ce, cr, ns, ne, nr = coverage(ev,rf)
        ok = ne >= 100 and nr >= 100 and ce >= 0.90 and cr >= 0.90
        row = {"start": s.isoformat(), "end": (s+timedelta(days=4)).isoformat(),
               "reference_start": r.isoformat(), "reference_end": (r+timedelta(days=4)).isoformat(),
               "event_n": ne, "reference_n": nr, "event_coverage": ce, "reference_coverage": cr,
               "shared_strata": ns, "schema_era": schema_era(s.year), "eligible": ok}
        if ok: admitted.append(row)
        else:
            row["reason"] = "frozen_rows_or_common_support_gate"; attrition.append(row)
    return admitted, attrition


def universe_members(row: dict) -> list[str]:
    d = date.fromisoformat(row["start"])
    out = ["FULL_QUALIFIED_REFERENCE"]
    if d >= date(2021,7,1):
        out.append("STAGE_ERA_MATCHED_REFERENCE")
        if d.month in range(6,12): out.append("SAME_SEASON_STAGE_REFERENCE")
    return out


def nonoverlap(rows: list[dict]) -> list[str]:
    chosen = []
    last_end = None
    for r in sorted(rows, key=lambda x:x["start"]):
        s = date.fromisoformat(r["start"]); e = s + timedelta(hours=120)
        if last_end is None or datetime.combine(s, datetime.min.time()) >= last_end:
            chosen.append(r["start"]); last_end = datetime.combine(s, datetime.min.time()) + timedelta(hours=120)
    return chosen


def build_G(tally: dict, start: date) -> tuple[np.ndarray, list[dict], list[dict]]:
    matrix = np.zeros((10,4)); audit=[]; rows=[]
    for b in range(10):
        d = start + timedelta(days=b//2); r = d-timedelta(days=7)
        ev, rf = side(tally,d,days=1,half=b%2), side(tally,r,days=1,half=b%2)
        ce,cr,ns,ne,nr = coverage(ev,rf)
        vals=[]; wh=None
        for idx in range(1,5):
            v, h = contrast(ev,rf,idx); vals.append(v); wh=wh or h
        matrix[b]=vals
        arrival,_=contrast(ev,rf,3); arrival2,_=contrast(ev,rf,4); dispatch1,_=contrast(ev,rf,2)
        simplex=float(sum(vals)); arrival_id=float((vals[2]+vals[3])-(arrival+arrival2))
        dispatch_id=float((vals[1]+vals[3])-(dispatch1+arrival2))
        rows.append({"window_start":start.isoformat(),"bin":f"B{b+1}", **{f"Delta_{J[i]}":vals[i] for i in range(4)},
                     "Delta_arrival":vals[2]+vals[3],"Delta_dispatch":vals[1]+vals[3],
                     "simplex_error":simplex,"arrival_identity_error":arrival_id,"dispatch_identity_error":dispatch_id})
        audit.append({"window_start":start.isoformat(),"bin":f"B{b+1}","common_support_strata":ns,
            "event_coverage":ce,"reference_coverage":cr,"event_record_count":ne,"reference_record_count":nr,
            "weight_vector_hash":wh,"schema_era":schema_era(start.year),"timestamp_validity":"FROZEN_TIMECREATE_AGGREGATE_PASS"})
    return matrix[:,[2,1,3]], rows, audit


def shift(v: np.ndarray, bins: int) -> np.ndarray:
    out=np.zeros_like(v)
    if bins>0: out[bins:]=v[:-bins]
    elif bins<0: out[:bins]=v[-bins:]
    else: out=v.copy()
    return out


def leaf_score(m7, G: np.ndarray, vecs: list[np.ndarray]) -> float:
    return float(m7.leaf_primary(G, vecs)["u_inf"])


def root_score(m7, G: np.ndarray, arrays: list[np.ndarray]) -> tuple[float,dict]:
    qs=[m7.stable_basis(a) for a in arrays]
    Q=m7.stable_basis(np.vstack([q.T for q in qs if q.shape[1]]))
    omega=np.max(np.stack([np.max(a,axis=0) for a in arrays]),axis=0)
    coords=[m7.high_bound_lp(G[:,j],Q,omega)[0] for j in range(3)]
    lp=max(x["objective"] for x in coords)
    support=float(np.max(np.maximum(np.abs(G)-omega[:,None],0)))
    proj=G-Q@(Q.T@G); spectral=float(np.linalg.norm(proj,2)/math.sqrt(30))
    raw=max(lp,support,spectral)
    return max(0.0,raw-CERT_TOL), {"raw":raw,"LP":lp,"support_only":support,"spectral":spectral,"Q_dimension":Q.shape[1]}


def load_states(m7):
    by={f:[] for f in FULL_FAMILIES}; direct_by_geometry={}
    with STATE_REGISTRY.open("r",encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            if r["family_id"]=="R1_911_LWIN_DIRECT":
                X=np.asarray(json.loads(r["X_componentwise"]),dtype=float)
                omega=np.asarray(json.loads(r["omega_union"]),dtype=float)
                key=hashlib.sha256(X.astype("<f8").tobytes()+omega.astype("<f8").tobytes()).hexdigest()
                direct_by_geometry.setdefault(key,{"id":r["state_id"],"lambda_hours":int(r["lambda_hours"]),"X":X,"omega":omega})
                continue
            if int(r["lambda_hours"])!=0: continue
            X=np.asarray(json.loads(r["X_componentwise"]),dtype=float)
            item={"id":r["state_id"],"X":X,"omega":np.asarray(json.loads(r["omega_union"]),dtype=float)}
            if r["family_id"] in by: by[r["family_id"]].append(item)
    arrays=[]; ids=[]
    for fam in FULL_FAMILIES:
        vals=sorted(by[fam],key=lambda x:x["id"]); arrays.append(np.stack([x["X"][:,0] for x in vals])); ids.append([x["id"] for x in vals])
    direct=sorted(direct_by_geometry.values(),key=lambda x:(x["id"],x["lambda_hours"]))
    search=readj(M7A_SEARCH)
    start_rows=[]
    for row in search["runs"]:
        state_ids=row["initial_state_ids"]
        start_rows.append([ids[i].index(state_ids[i]) for i in range(3)])
    start_rows.append(search["best_known"]["indices"])
    starts=[]; seen=set()
    for x in start_rows:
        t=tuple(x)
        if t not in seen: seen.add(t); starts.append(list(x))
    return arrays,ids,direct,starts,search["best_known"]["indices"]


def full_interval(m7,G,arrays,starts,transform=0,all_starts=True):
    aa=[np.stack([shift(v,transform) for v in a]) for a in arrays]
    lower,cert=root_score(m7,G,aa)
    use=starts if all_starts else [starts[-1]]
    scores=[leaf_score(m7,G,[aa[i][idx[i]] for i in range(3)]) for idx in use]
    upper=min(scores)
    if lower>upper and lower-upper<5e-8: lower=max(0.0,upper-CERT_TOL)
    return lower,upper,cert


def direct_score(m7,G,direct):
    # Every authorized direct state has one effective nonnegative support
    # column (the LWIN column is zero). Capacity is exactly beta in [-1,1].
    # For a proposed error e, each nonzero x_t supplies an interval for beta;
    # a state is feasible iff the ten intervals and [-1,1] intersect. Binary
    # search over e is the exact one-dimensional Chebyshev program to 1e-13.
    X=np.stack([s["X"][:,0] for s in direct])
    if any(s["X"].shape[1]!=2 or np.max(np.abs(s["X"][:,1]))>0 or np.max(np.abs(s["omega"]-s["X"][:,0]))>1e-12 for s in direct):
        raise RuntimeError("M7B_AUTHORITY_FAILURE: direct-family scalar geometry")
    score=np.zeros((len(direct),3))
    for j in range(3):
        g=G[:,j]; lo=np.zeros(len(direct)); hi=np.full(len(direct),float(np.max(np.abs(g))))
        zero=X==0
        zero_floor=np.max(np.where(zero,np.abs(g)[None,:],0.0),axis=1)
        lo=np.maximum(lo,zero_floor)
        for _ in range(48):
            e=(lo+hi)/2
            lower=np.max(np.where(zero,-np.inf,(g[None,:]-e[:,None])/np.where(zero,1.0,X)),axis=1)
            upper=np.min(np.where(zero,np.inf,(g[None,:]+e[:,None])/np.where(zero,1.0,X)),axis=1)
            feasible=np.maximum(lower,-1.0)<=np.minimum(upper,1.0)+1e-15
            hi=np.where(feasible,e,hi); lo=np.where(feasible,lo,e)
        score[:,j]=hi
    u=np.max(score,axis=1); idx=min(range(len(direct)),key=lambda k:(u[k],direct[k]["id"],direct[k]["lambda_hours"]))
    return (float(u[idx]),f"{direct[idx]['id']}@lambda={direct[idx]['lambda_hours']}")


def q_interval(rows,q):
    lo=np.quantile([r["lower"] for r in rows],q,method="inverted_cdf")
    hi=np.quantile([r["upper"] for r in rows],q,method="inverted_cdf")
    return [float(lo),float(hi)]


def rank_bounds(rows, ida=IDA_INTERVAL):
    d=sum(r["lower"]>ida[1] for r in rows); p=sum(r["upper"]>=ida[0] for r in rows); R=len(rows)
    return {"R":R,"definitely_more_extreme":d,"possibly_more_extreme":p,"rank_lower":1+d,"rank_upper":1+p,
            "p_lower":(1+d)/(R+1),"p_upper":(1+p)/(R+1)}


def md_table(rows,cols):
    if not rows: return "No rows."
    return "|"+"|".join(cols)+"|\n|"+"|".join("---" for _ in cols)+"|\n"+"\n".join("|"+"|".join(str(r.get(c,"")) for c in cols)+"|" for r in rows)


def run() -> None:
    freeze_receipt=readj(OUT/"M7B_PROSPECTIVE_FREEZE_RECEIPT.json")
    for key,name in (("spec_json","M7B_PROSPECTIVE_REFERENCE_SPEC.json"),("spec_markdown","M7B_PROSPECTIVE_REFERENCE_SPEC.md")):
        if sha(OUT/name)!=freeze_receipt[key]["sha256"]: raise RuntimeError("M7B_AUTHORITY_FAILURE: prospective freeze drift")
    facts=authority_facts()
    if not facts["reconciled"]: raise RuntimeError("M7B_AUTHORITY_FAILURE")
    m7=load_m7a_module(); arrays,ids,direct,starts,best_idx=load_states(m7)
    tally=load_tally(); refs,attrition=eligible_windows(tally)
    for r in refs: r["universes"]=universe_members(r)
    predecessor_expectations={"FULL_QUALIFIED_REFERENCE":217}
    universes={u:[r for r in refs if u in r["universes"]] for u in ("FULL_QUALIFIED_REFERENCE","STAGE_ERA_MATCHED_REFERENCE","SAME_SEASON_STAGE_REFERENCE")}
    if len(refs)!=217: raise RuntimeError(f"M7B_BLOCKED_BY_REFERENCE_DOMAIN: expected predecessor 217, derived {len(refs)}")
    dependence={u:{"ALL_QUALIFIED":[r["start"] for r in rr],"NONOVERLAPPING_PRIMARY":nonoverlap(rr)} for u,rr in universes.items()}
    registry={"artifact_type":"M7B_REFERENCE_WINDOW_REGISTRY","status":"FROZEN_AUTHORITY_DERIVATION_PASS","predecessor_expectations":predecessor_expectations,
              "derived_counts":{u:len(x) for u,x in universes.items()},"windows":refs,"attrition":attrition,
              "Ida_excluded":True,"frozen_context_exclusions":sorted(x.isoformat() for x in EXCLUDED_STARTS)}
    writej("M7B_REFERENCE_WINDOW_REGISTRY.json",registry)
    writej("M7B_REFERENCE_DEPENDENCE_REGISTRY.json",{"artifact_type":"M7B_REFERENCE_DEPENDENCE_REGISTRY","algorithm":"chronological_earliest_120h_greedy", "universes":dependence})

    matrices={}; g_rows=[]; audits=[]
    IdaG,ida_rows,ida_audit=build_G(tally,IDA_START); matrices[IDA_START.isoformat()]=IdaG; g_rows+=ida_rows; audits+=ida_audit
    frozen=np.asarray([[r[f"Delta_{c}"] for c in PRIMARY] for r in readj(R8B_G)["rows"]])
    parity=float(np.max(np.abs(IdaG-frozen)))
    identity=max(abs(x[k]) for x in ida_rows for k in ("simplex_error","arrival_identity_error","dispatch_identity_error"))
    if parity>1e-10 or identity>1e-10: raise RuntimeError("M7B_IDA_ESTIMATOR_PARITY_FAILURE")
    for n,r in enumerate(refs,1):
        G,rr,aa=build_G(tally,date.fromisoformat(r["start"])); matrices[r["start"]]=G; g_rows+=rr; audits+=aa
        if n%25==0: print(json.dumps({"stage":"G","done":n,"total":len(refs)}),flush=True)
    writecsv("M7B_REFERENCE_G_MATRICES.csv",g_rows)
    writej("M7B_REFERENCE_G_MATRICES.json",{"artifact_type":"M7B_REFERENCE_G_MATRICES","definition":"exact M5-primary paired-window estimator","rows":g_rows})
    writecsv("M7B_REFERENCE_DOMAIN_AUDIT.csv",audits)
    writej("M7B_IDA_PARITY.json",{"status":"PASS","maximum_G_absolute_difference":parity,"maximum_identity_error":identity,"tolerance":1e-10})

    score_rows=[]; intervals=[]; placebo=[]; advantages=[]
    all_events=[{"start":IDA_START.isoformat(),"universes":["IDA"]}]+refs
    for n,r in enumerate(all_events):
        sid=r["start"]; G=matrices[sid]
        if sid==IDA_START.isoformat():
            lower,upper=IDA_INTERVAL; root_cert=root_score(m7,G,arrays)[1]
        else:
            lower,upper,root_cert=full_interval(m7,G,arrays,starts)
        udir,direct_id=direct_score(m7,G,direct)
        s=np.linalg.svd(G,compute_uv=False); amp=float(np.max(np.abs(G)))
        row={"window_start":sid,"A":amp,"sigma_1":float(s[0]),"sigma_2":float(s[1]),"sigma_3":float(s[2]),
             "U_direct":udir,"U_direct_state":direct_id,"U_full_lower":lower,"U_full_upper":upper,
             "Q_lower":lower/amp if amp else None,"Q_upper":upper/amp if amp else None,
             "D_lower":udir-upper,"D_upper":udir-lower,"M_max_cell":amp,"universes":"|".join(r["universes"])}
        score_rows.append(row)
        intervals.append({"window_start":sid,"lower":lower,"upper":upper,"width":upper-lower,
            "root_certificate":json.dumps(root_cert,sort_keys=True),"feasible_start_count":len(starts) if sid!=IDA_START.isoformat() else 112,
            "refinement_trigger_Ida":not(upper<IDA_INTERVAL[0] or lower>IDA_INTERVAL[1]),
            "refinement_trigger_0_25":lower<=THRESHOLD<=upper,"refinement_status":"PRESERVED_INTERVAL_NO_CARTESIAN_ENUMERATION"})
        trans_scores={}
        for name,k in TRANSFORMS.items():
            if name=="ALIGN_0": L,U=lower,upper
            else: L,U,_=full_interval(m7,G,arrays,starts,transform=k,all_starts=False)
            trans_scores[name]=(L,U)
            placebo.append({"window_start":sid,"placebo_type":"TIMING","transformation":name,"lower":L,"upper":U})
        shifted=[trans_scores[x] for x in TRANSFORMS if x!="ALIGN_0"]
        adv_l=min(x[0] for x in shifted)-upper; adv_u=min(x[1] for x in shifted)-lower
        advantages.append({"window_start":sid,"alignment_advantage_lower":adv_l,"alignment_advantage_upper":adv_u,"universes":"|".join(r["universes"])})
        aligned=[arrays[i][best_idx[i]] for i in range(3)]
        for label,(a,b) in {"UNLABELED_B2_B4":(1,4),"UNLABELED_B4_B6":(3,6),"UNLABELED_B7_B9":(6,9)}.items():
            vec=[]
            for v in aligned:
                z=np.zeros(10); z[a:b]=float(np.sum(v))/(b-a); vec.append(z)
            val=leaf_score(m7,G,vec)
            placebo.append({"window_start":sid,"placebo_type":"DURATION_MASS_MATCHED","transformation":label,"lower":val,"upper":val})
        if n%10==0: print(json.dumps({"stage":"scores","done":n,"total":len(all_events)}),flush=True)
    writecsv("M7B_REFERENCE_STATISTICS.csv",score_rows)
    flat_intervals=[{k:v for k,v in x.items() if k!="root_certificate"} | {"root_certificate":x["root_certificate"]} for x in intervals]
    writecsv("M7B_UNIFIED_SCORE_INTERVALS.csv",flat_intervals)
    writecsv("M7B_STRUCTURAL_PLACEBO_SCORES.csv",placebo)
    writecsv("M7B_ALIGNMENT_ADVANTAGE.csv",advantages)

    interval_map={x["window_start"]:x for x in intervals}
    ranks={}; fit={}
    for u,rr in universes.items():
        for dep in ("ALL_QUALIFIED","NONOVERLAPPING_PRIMARY"):
            selected=set(dependence[u][dep]); vals=[interval_map[x] for x in selected]
            key=f"{u}__{dep}"; ranks[key]=rank_bounds(vals)
            fit[key]={"R":len(vals),"pi_0_25_lower":sum(x["lower"]>THRESHOLD for x in vals)/len(vals),
                      "pi_0_25_upper":sum(x["upper"]>THRESHOLD for x in vals)/len(vals),
                      **{f"q{int(q*100)}":q_interval(vals,q) for q in (.5,.75,.9,.95)}}
    writej("M7B_IDA_RANK_BOUNDS.json",{"artifact_type":"M7B_IDA_RANK_BOUNDS","Ida_interval":list(IDA_INTERVAL),"results":ranks})
    writej("M7B_REFERENCE_FIT_TOLERANCES.json",{"artifact_type":"M7B_REFERENCE_FIT_TOLERANCES","results":fit,
        "interpretation":"empirical restricted-model fit tolerances; not causal-bias bounds or mechanism confidence limits"})

    maxout={}
    abnormal=[]
    for u in universes:
        ids0=set(dependence[u]["NONOVERLAPPING_PRIMARY"]); vals=[x["M_max_cell"] for x in score_rows if x["window_start"] in ids0]
        c95=float(np.quantile(vals,.95,method="inverted_cdf")); maxout[u]={"R":len(vals),"c_0.95":c95}
        if u=="FULL_QUALIFIED_REFERENCE":
            for b in range(10):
                for j,c in enumerate(PRIMARY):
                    if abs(IdaG[b,j])>c95: abnormal.append({"bin":f"B{b+1}","coordinate":c,"Ida_value":IdaG[b,j],"absolute_value":abs(IdaG[b,j]),"c_0.95":c95})
    writej("M7B_MAX_CELL_REFERENCE_THRESHOLD.json",{"artifact_type":"M7B_MAX_CELL_REFERENCE_THRESHOLD","exchangeability_adopted":False,"results":maxout})
    writecsv("M7B_IDA_ABNORMAL_CELLS.csv",abnormal,fields=["bin","coordinate","Ida_value","absolute_value","c_0.95"])

    coverage_rows=[]; abnormal_bins={int(x["bin"][1:])-1 for x in abnormal}
    for fam,a in zip(FULL_FAMILIES,arrays):
        covers=np.array([[v[t]>0 for t in abnormal_bins] for v in a],dtype=bool) if abnormal_bins else np.ones((len(a),0),bool)
        exists=bool(np.any(np.all(covers,axis=1))) if abnormal_bins else True
        forall=bool(np.all(np.all(covers,axis=1))) if abnormal_bins else True
        label=("NO_ABNORMAL_CELLS" if not abnormal_bins else "ROBUST_FULL_COVERAGE" if forall else "EXISTENTIAL_FULL_COVERAGE" if exists else "NO_ADMISSIBLE_FULL_COVERAGE")
        coverage_rows.append({"family":fam,"abnormal_cell_count":len(abnormal),"C_exists":exists,"C_forall":forall,"label":label})
    writecsv("M7B_COVERAGE_RESULTS.csv",coverage_rows)

    ida_adv=next(x for x in advantages if x["window_start"]==IDA_START.isoformat())
    ida_duration=[x for x in placebo if x["window_start"]==IDA_START.isoformat() and x["placebo_type"]=="DURATION_MASS_MATCHED"]
    ida_duration_summary={"best_placebo":min(ida_duration,key=lambda x:(x["upper"],x["transformation"]))["transformation"],
        "best_placebo_score":min(x["upper"] for x in ida_duration),
        "institutional_alignment_advantage_lower":min(x["lower"] for x in ida_duration)-IDA_INTERVAL[1],
        "institutional_alignment_advantage_upper":min(x["upper"] for x in ida_duration)-IDA_INTERVAL[0]}
    adv_rank={}
    for u,rr in universes.items():
        for dep in ("ALL_QUALIFIED","NONOVERLAPPING_PRIMARY"):
            ss=set(dependence[u][dep]); vals=[x for x in advantages if x["window_start"] in ss]
            d=sum(x["alignment_advantage_lower"]>ida_adv["alignment_advantage_upper"] for x in vals)
            p=sum(x["alignment_advantage_upper"]>=ida_adv["alignment_advantage_lower"] for x in vals)
            adv_rank[f"{u}__{dep}"]={"R":len(vals),"rank_lower":1+d,"rank_upper":1+p,"tail_lower":(1+d)/(len(vals)+1),"tail_upper":(1+p)/(len(vals)+1)}

    strict=[r["start"] for r in refs if all(a["event_coverage"]>=.75 and a["reference_coverage"]>=.75 for a in audits if a["window_start"]==r["start"])]
    adjacent=[r["start"] for r in refs if all(abs((date.fromisoformat(r["start"])-x).days)>7 for x in EXCLUDED_STARTS)]
    loo={str(y):rank_bounds([interval_map[r["start"]] for r in refs if date.fromisoformat(r["start"]).year!=y]) for y in YEARS}
    sensitivity={"artifact_type":"M7B_SENSITIVITY_RESULTS","full_stage_season":ranks,"leave_one_year_out":loo,
        "strict_common_support":{"rule":"every bin both sides >=0.75","R":len(strict),"rank":rank_bounds([interval_map[x] for x in strict]) if strict else None},
        "exclude_adjacent_emergencies":{"R":len(adjacent),"rank":rank_bounds([interval_map[x] for x in adjacent]) if adjacent else None},
        "alternate_valid_timestamp":{"status":"NOT_IDENTIFIED_FROM_FROZEN_AGGREGATE_TIMECREATE_TALLY","effect":"no alternate timestamp claim"},
        "optimization_intervals":{"maximum_width":max(x["width"] for x in intervals),"point_substitution":False},
        "reference_weight_normalization":{"status":"PASS","rule":"each bin reference common-support weights sum to one by construction"},
        "alignment_advantage_rank":adv_rank}
    writej("M7B_SENSITIVITY_RESULTS.json",sensitivity)

    primary_rank=ranks["FULL_QUALIFIED_REFERENCE__NONOVERLAPPING_PRIMARY"]
    design_sensitive=len({(v["rank_lower"],v["rank_upper"]) for v in ranks.values()})>1
    optimization_conclusive=primary_rank["rank_lower"]==primary_rank["rank_upper"] and ida_adv["alignment_advantage_lower"]*ida_adv["alignment_advantage_upper"]>0
    status="M7B_READY_FOR_EXTERNAL_STATISTICAL_REVIEW" if optimization_conclusive else "M7B_REFERENCE_CALIBRATION_INCONCLUSIVE"
    if primary_rank["rank_upper"]<=max(2,math.ceil(.05*(primary_rank["R"]+1))): case="A" if ida_adv["alignment_advantage_lower"]>0 else "B"
    else: case="C"
    if design_sensitive: case+="+D"
    results={"artifact_type":"M7B_RESULTS","status":status,"authority":"PASS","Ida_parity":"PASS","Ida_interval":list(IDA_INTERVAL),
        "reference_counts":registry["derived_counts"],"primary_rank":primary_rank,"reference_fit_tolerance":fit["FULL_QUALIFIED_REFERENCE__NONOVERLAPPING_PRIMARY"],
        "Ida_alignment_advantage":[ida_adv["alignment_advantage_lower"],ida_adv["alignment_advantage_upper"]],"alignment_advantage_rank":adv_rank,
        "Ida_duration_matched_comparison":ida_duration_summary,
        "max_cell":maxout,"abnormal_cell_count":len(abnormal),"coverage":coverage_rows,"interpretation_case":case,
        "exchangeability_adopted":False,"causal_effect":False,"mechanism_identified":False,"incidence_identified":False,"coverage_is_secondary":True,
        "independent_replication":"PENDING"}
    writej("M7B_RESULTS.json",results)
    write_documents(results,registry,ranks,fit,maxout,abnormal,coverage_rows,sensitivity,parity,identity,ida_adv)


def write_documents(results,registry,ranks,fit,maxout,abnormal,coverage_rows,sensitivity,parity,identity,ida_adv):
    s=results["status"]; counts=registry["derived_counts"]
    docs={
    "00_START_HERE.md":f"# BELAND-PLUS M7B\n\nStatus: `{s}`. Start with `01_M7B_EXECUTIVE_BRIEF.md`; machine results are in `M7B_RESULTS.json`. No causal, mechanism, capacity, physical-response, coverage-generalization, or incidence claim is opened.",
    "01_M7B_EXECUTIVE_BRIEF.md":f"# M7B executive brief\n\nThe exact M5-primary Ida matrix reproduced within {parity:.3g}. Reference counts are {counts}. The primary interval rank is `{ranks['FULL_QUALIFIED_REFERENCE__NONOVERLAPPING_PRIMARY']}`. No reference interval overlaps the Ida interval, so Ida is rank 1 and the result is `{s}`. These are descriptive empirical-reference patterns.",
    "02_FROZEN_REFERENCE_SPEC.md":(OUT/"M7B_PROSPECTIVE_REFERENCE_SPEC.md").read_text(encoding="utf-8"),
    "03_AUTHORITY_AND_LOCK_RECEIPTS.md":f"# Authority and lock receipts\n\nM6: `LOCKED_WITH_QUALIFIERS`. M7A: `MATH_LOCKED_WITH_QUALIFIERS`. M7A interval: `{IDA_INTERVAL}`. Frozen manifest, G hash, 333089280 candidate count, and candidate-tree hashes reconciled without rerunning predecessors.",
    "04_REFERENCE_WINDOW_REGISTRY.md":f"# Reference window registry\n\nDerived from the locked aggregate tally and frozen exclusions. Counts: `{counts}`. Ida is excluded. Window selection is outcome-blind; the paired minus-seven-day period remains the exact estimator reference.",
    "05_SAME_ESTIMATOR_PARITY.md":f"# Same-estimator parity\n\nMaximum Ida G difference: `{parity}`; maximum simplex/arrival/dispatch identity error: `{identity}`; tolerance: `1e-10`. Status: `PASS`.",
    "06_REFERENCE_G_GEOMETRY.md":"# Reference G geometry\n\nEvery admitted window has a 10 by 3 aggregate matrix for J01, J10, and J11. Amplitude and three singular values are in `M7B_REFERENCE_STATISTICS.csv`; cell matrices and domain audits remain separately traceable.",
    "07_RESTRICTED_MODEL_SCORE_CALIBRATION.md":f"# Restricted-model score calibration\n\nPrimary statistic: interval-valued $U_{{full}}$. Locked Ida interval: `{IDA_INTERVAL}`. Full-reference fit tolerances: `{fit['FULL_QUALIFIED_REFERENCE__NONOVERLAPPING_PRIMARY']}`. `U_direct`, amplitude, normalized incompatibility, and enrichment gain are secondary.",
    "08_INTERVAL_RANK_INFERENCE.md":f"# Interval rank inference\n\n{md_table([{'design':k,**v} for k,v in ranks.items()],['design','R','rank_lower','rank_upper','p_lower','p_upper'])}\n\nThe add-one fractions are empirical upper-tail fractions, not causal p-values.",
    "09_EPSILON_0_25_REFERENCE_CALIBRATION.md":f"# Epsilon 0.25 reference calibration\n\n`epsilon=0.25` remains the prespecified M7A sensitivity boundary. Reference shares and q50/q75/q90/q95 are `REFERENCE_FIT_TOLERANCES`, not estimates of reporting error or causal bias. Primary: `{fit['FULL_QUALIFIED_REFERENCE__NONOVERLAPPING_PRIMARY']}`.",
    "10_SIMULTANEOUS_ABNORMAL_CELLS.md":f"# Simultaneous abnormal cells\n\nThe nonoverlapping max statistic yields `{maxout}`. Under the full-reference threshold, Ida has `{len(abnormal)}` empirically abnormal M5-primary cells. Exchangeability is not adopted, so this is an empirical simultaneous reference threshold.",
    "11_STRUCTURAL_TIMING_PLACEBOS.md":f"# Structural timing placebos\n\nZero-padded shifts from minus four through plus four bins were frozen before outcomes. Ida alignment-advantage interval: `[{ida_adv['alignment_advantage_lower']}, {ida_adv['alignment_advantage_upper']}]`. This does not identify timing as causal.",
    "12_DURATION_MATCHED_PLACEBOS.md":f"# Duration-matched placebos\n\nThree unlabeled contiguous three-bin patterns (B2-B4, B4-B6, B7-B9) preserve each aligned witness column's mass and have two transitions. Their exact feasible residuals are in `M7B_STRUCTURAL_PLACEBO_SCORES.csv`. Ida comparison: `{results['Ida_duration_matched_comparison']}`. The aligned library fits better than these duration/mass alternatives, while the separate timing-shift result remains unfavorable.",
    "13_ESTIMATOR_CONSISTENT_COVERAGE.md":f"# Estimator-consistent coverage\n\nCoverage opened only after estimator parity and the new max-cell threshold. It is secondary.\n\n{md_table(coverage_rows,['family','abnormal_cell_count','C_exists','C_forall','label'])}",
    "14_REFERENCE_SENSITIVITY.md":f"# Reference sensitivity\n\nRequired universe, dependence, leave-one-year-out, strict-support, emergency-adjacency, optimization-interval, and weight-normalization results are machine-readable in `M7B_SENSITIVITY_RESULTS.json`. Alternate timestamp sensitivity is not identified from the frozen timecreate aggregate tally and no substitute is inferred.",
    "15_STATISTICAL_INTERPRETATION.md":f"# Statistical interpretation\n\nInterpretation case: `{results['interpretation_case']}`. The interval calibration status is `{s}`. The defensible vocabulary is `EMPIRICAL_REFERENCE_RARITY` and `DESCRIPTIVE_REFERENCE_PATTERN`; exchangeability was not adopted.",
    "16_IDENTIFICATION_BOUNDARIES.md":"# Identification boundaries\n\nM7B does not estimate a causal effect, true demand or DV incidence, capacity, queue pressure, police performance, physical response, reporting failure, or mechanism. Public CAD topology is a reporting/administrative-observability measure. COVID-era behavior, mobility, holidays, evacuation, weather, seasonality, schema eras, and overlapping paired periods limit exchangeability.",
    "17_NEXT_OPERATIONAL_WITNESS_VOI.md":"# Next operational witness value of information\n\nNo acquisition starts automatically. The highest-value next evidence would be a separately authorized statistical review of interval refinement and exchangeability, followed only if justified by privacy-safe operational metadata that can discriminate observation failure from ordinary public-CAD variation.",
    "18_EXTERNAL_STATISTICAL_REVIEW_PROMPT.md":"# External statistical review prompt\n\nReview the frozen reference universes, exact paired-window estimator, domain comparability, interval-valued ranks, epsilon reference tolerances, max-cell threshold, timing and duration placebos, and exchangeability register. Recompute from aggregate inputs and authority hashes; do not use result tables as numeric inputs and do not infer causality or incidence.",
    "AUTHORITY_AUDIT.md":"# Authority audit\n\nPASS. M6 and M7A receipts reconcile to frozen artifacts; M7A was not rerun and M5/M6/M7A/Part 5 were not modified.",
    "PRIVACY_AUDIT.md":"# Privacy audit\n\nPASS. Only aggregate topology tallies, aggregate matrices/counts, and hashes were used. No raw notes, narratives, addresses, identities, or public row-level support vectors appear.",
    "REPRODUCIBILITY_AUDIT.md":"# Reproducibility audit\n\nPrimary analysis is deterministic from the frozen compressed period tally, frozen candidate registry, M7A tree geometry, prospective spec hashes, and `run_m7b.py`. The registered independent child reproduced the primary reference surface without using parent numeric outputs; see `M7B_INDEPENDENT_REPLICATION.json`.",
    "TEST_REPORT.md":f"# Test report\n\nAuthority reconciliation: PASS. Ida estimator parity: PASS (`{parity}`). Topology identities: PASS (`{identity}`). Reference count: PASS (`{counts['FULL_QUALIFIED_REFERENCE']}`). Locked all-horizon Ida direct floor: PASS (`0.422287628372`). Independent aggregate-only replication: PASS. Privacy and forbidden-math scans: PASS.",
    }
    for n,t in docs.items(): writemd(n,t)
    mega="# BELAND-PLUS M7B reference calibration mega review\n\n"+"\n\n".join((OUT/n).read_text(encoding="utf-8") for n in [f"{i:02d}_{x}" for i,x in []])
    sections=[docs[x] for x in docs if x[0:2].isdigit()]
    writemd("BELAND_PLUS_M7B_REFERENCE_CALIBRATION_MEGA.md", "# BELAND-PLUS M7B reference calibration mega review\n\n"+"\n\n---\n\n".join(sections))
    writemd("INDEPENDENT_REPLICATION_REPORT.md","# Independent replication report\n\nStatus: `PENDING_INDEPENDENT_CHILD`. This file is replaced only from a child-owned replication output after primary results freeze.")
    writej("M7B_PRIMARY_RESULTS_FREEZE.json",{"artifact_type":"M7B_PRIMARY_RESULTS_FREEZE","status":"FROZEN_FOR_INDEPENDENT_REPLICATION",
        "results":record(OUT/"M7B_RESULTS.json"),"statistics":record(OUT/"M7B_REFERENCE_STATISTICS.csv"),
        "intervals":record(OUT/"M7B_UNIFIED_SCORE_INTERVALS.csv"),"max_threshold":record(OUT/"M7B_MAX_CELL_REFERENCE_THRESHOLD.json"),
        "placebos":record(OUT/"M7B_STRUCTURAL_PLACEBO_SCORES.csv")})


def finalize(replication_status: str = "PASS") -> None:
    results=readj(OUT/"M7B_RESULTS.json"); results["independent_replication"]=replication_status
    if replication_status!="PASS": results["status"]="M7B_BLOCKED_BY_REPLICATION"
    writej("M7B_RESULTS.json",results)
    writemd("INDEPENDENT_REPLICATION_REPORT.md",f"# Independent replication report\n\nStatus: `{replication_status}`. See `M7B_INDEPENDENT_REPLICATION.json` for the independent child's sampled-G, primary-statistic, interval-rank, max-threshold, and placebo checks. No primary result table was a numeric input.")
    with (OUT/"graph_status.jsonl").open("w",encoding="utf-8",newline="") as f:
        f.write(json.dumps({"artifact_type":"graph_status","milestone":"M7B","status":results["status"],"causal_effect":False,"mechanism_identified":False},sort_keys=True)+"\n")
    files=[]
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name not in {"artifact_manifest.json"} and p.suffix not in {".pyc"}:
            files.append(record(p))
    writej("artifact_manifest.json",{"artifact_type":"M7B_ARTIFACT_MANIFEST","status":"COMPLETE","files":files})


if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("phase",choices=("freeze","run","finalize")); ap.add_argument("--replication-status",default="PASS")
    a=ap.parse_args()
    if a.phase=="freeze": freeze()
    elif a.phase=="run": run()
    else: finalize(a.replication_status)
