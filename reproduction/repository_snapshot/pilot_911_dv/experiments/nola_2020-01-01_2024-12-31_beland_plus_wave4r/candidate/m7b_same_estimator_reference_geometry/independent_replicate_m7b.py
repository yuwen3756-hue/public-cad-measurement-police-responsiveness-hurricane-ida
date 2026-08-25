"""Independent aggregate-only replication for the frozen M7B calibration.

This intentionally does not import ``run_m7b.py`` or any M7B primary numeric
output.  It reconstructs the paired, within-bin common-support estimator and
uses the frozen M7A root geometry plus the frozen initial feasible starts.
"""
from __future__ import annotations

import csv, gzip, hashlib, json, math
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

OUT = Path(__file__).resolve().parent
CANDIDATE = OUT.parent
ROOT = OUT.parents[3]
W2 = ROOT / "experiments" / "nola_2020-01-01_2024-12-31_beland_plus_wave2" / "data" / "interim" / "w2_period_tally.csv.gz"
R8 = CANDIDATE / "r8b_long_closeout" / "R8B_MATH_G_MATRIX.json"
M6 = CANDIDATE / "m6a_numeric_trials" / "M6A_COMPLETE_STATE_REGISTRY.csv"
M7A = CANDIDATE / "m7a_full_combined_unified_threshold"
TREE = M7A / "M7A_CANDIDATE_TREE_REGISTRY.json"
SEARCH = M7A / "M7A_INITIAL_SEARCH_RESULTS.json"
SPEC = OUT / "M7B_PROSPECTIVE_REFERENCE_SPEC.json"
REGISTRY = OUT / "M7B_REFERENCE_WINDOW_REGISTRY.json"
FREEZE = OUT / "M7B_PROSPECTIVE_FREEZE_RECEIPT.json"
PRIMARY_FREEZE = OUT / "M7B_PRIMARY_RESULTS_FREEZE.json"
COORDS = ("J01", "J10", "J11")
FAMILIES = ("R1_S4_TWELVE_HOUR_SHIFTS", "R1_S4_REDEPLOYMENT_ANTI_LOOTING", "R1_S4_CURFEW")

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def stable_basis(rows):
    q = []
    for x in rows:
        z = np.array(x, dtype=float)
        for v in q: z -= v * float(v @ z)
        n = np.linalg.norm(z)
        if n > 1e-12: q.append(z / n)
    return np.column_stack(q) if q else np.empty((10, 0))

def lp_score(g, X, omega):
    p = X.shape[1]
    values = []
    for j in range(3):
        A = np.vstack((np.c_[X, -np.ones(10)], np.c_[-X, -np.ones(10)],
                       np.c_[X, np.zeros(10)], np.c_[-X, np.zeros(10)]))
        b = np.r_[g[:, j], -g[:, j], omega, omega]
        r = linprog(np.r_[np.zeros(p), 1.0], A_ub=A, b_ub=b,
                    bounds=[(None, None)] * p + [(0, None)], method="highs-ds",
                    options={"dual_feasibility_tolerance": 1e-9,
                             "primal_feasibility_tolerance": 1e-9})
        if not r.success: raise RuntimeError(r.message)
        values.append(float(r.fun))
    return max(values)

def read_tally():
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: np.zeros(5, dtype=float))))
    with gzip.open(W2, "rt", newline="") as f:
        for r in csv.DictReader(f):
            # The locked M5 primary signature is the non-officer/self-initiated
            # universe; other initiation categories are not pooled into it.
            if r["si"] != "non_officer_self_initiated": continue
            key = f"{r['initialtype'].strip().upper() or 'UNKNOWN'}|{r['hour_bucket']}|{'text' if r['year'] == '2023' else 'numeric'}"
            out[r["date"]][r["hour_bucket"]][key] += np.array([float(r[x]) for x in ("n", "J00", "J10", "J01", "J11")])
    return out

def bins_for(start: date):
    # B1/B2 are 00-11/12-23 on the first day, then repeat for five days.
    out = []
    for d in range(5):
        ds = (start + timedelta(days=d)).isoformat()
        out.append((ds, {"00-05", "06-11"}))
        out.append((ds, {"12-17", "18-23"}))
    return out

def g_matrix(tally, start):
    ref = start - timedelta(days=7)
    result = np.zeros((10, 3)); diagnostics = []
    for b, ((ed, eh), (rd, rh)) in enumerate(zip(bins_for(start), bins_for(ref))):
        ev, rf = {}, {}
        for hb in eh:
            for k, v in tally[ed][hb].items(): ev[k] = ev.get(k, np.zeros(5)) + v
        for hb in rh:
            for k, v in tally[rd][hb].items(): rf[k] = rf.get(k, np.zeros(5)) + v
        shared = sorted(set(ev) & set(rf))
        den = sum(rf[k][0] for k in shared)
        # The five-day gate is locked at window level.  A rare empty 12-hour
        # intersection is retained as a flagged zero contrast, rather than
        # silently changing the frozen registry post-outcome.
        if den <= 0:
            diagnostics.append({"shared": 0, "reference_common_n": 0.0, "simplex_error": 0.0, "empty_bin": True})
            continue
        delta = np.zeros(4)
        for k in shared:
            w = rf[k][0] / den
            delta += w * (ev[k][1:] / ev[k][0] - rf[k][1:] / rf[k][0])
        result[b] = delta[[2, 1, 3]]  # J01,J10,J11
        diagnostics.append({"shared": len(shared), "reference_common_n": float(den), "simplex_error": float(delta.sum())})
    return result, diagnostics

def nonoverlap(items):
    keep, last = [], None
    for x in sorted(items, key=lambda z: z["start"]):
        s = date.fromisoformat(x["start"])
        if last is None or s >= last:
            keep.append(x); last = s + timedelta(days=5)
    return keep

def shift(g, k):
    z = np.zeros_like(g)
    if k >= 0: z[k:] = g[:10-k]
    else: z[:k] = g[-k:]
    return z

def main():
    # Read only authority/specification artifacts and aggregate frozen input.
    spec, registry, freeze = (json.loads(x.read_text(encoding="utf-8")) for x in (SPEC, REGISTRY, FREEZE))
    primary_hashes = json.loads(PRIMARY_FREEZE.read_text(encoding="utf-8"))
    if spec["status"] != "FROZEN_BEFORE_PSEUDO_EVENT_OUTCOMES" or primary_hashes["status"] != "FROZEN_FOR_INDEPENDENT_REPLICATION":
        raise RuntimeError("frozen M7B inputs unavailable")
    tally = read_tally()
    trees = json.loads(TREE.read_text(encoding="utf-8"))["trees"]
    roots = [t["nodes"][t["root_hash"]] for t in trees]
    Q = stable_basis([v for n in roots for v in np.asarray(n["orthonormal_span_basis"], float).T])
    omega_root = np.maximum.reduce([np.asarray(n["support_max"], float) for n in roots])
    states = {}
    with M6.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): states[r["state_id"]] = np.asarray(json.loads(r["omega_union"]), float)
    search = json.loads(SEARCH.read_text(encoding="utf-8"))
    triples = sorted({tuple(x["initial_state_ids"]) for x in search["runs"]} | {tuple(search["best_known"]["state_ids"])})
    vectors = []
    for t in triples:
        if all(x in states for x in t):
            X = np.column_stack([states[x] for x in t]); vectors.append((t, X, np.max(X, axis=1)))
    if not vectors: raise RuntimeError("no frozen feasible M7A starts")
    ida, ida_d = g_matrix(tally, date(2021, 8, 29))
    locked = json.loads(R8.read_text(encoding="utf-8"))["rows"]
    target = np.array([[r[f"Delta_{x}"] for x in COORDS] for r in locked], dtype=float)
    parity = float(np.max(np.abs(ida - target)))
    if parity > 1e-10: raise RuntimeError(f"Ida estimator parity {parity}")
    windows = [x for x in registry["windows"] if x.get("eligible")]
    if len(windows) != 217: raise RuntimeError(f"registry count {len(windows)}")
    scored, matrices = [], {}
    for w in windows:
        g, d = g_matrix(tally, date.fromisoformat(w["start"]))
        lo = lp_score(g, Q, omega_root) - 1e-8
        uppers = [(lp_score(g, X, o), ids) for ids, X, o in vectors]
        hi, chosen = min(uppers, key=lambda x: (x[0], x[1]))
        row = {"start": w["start"], "universes": w["universes"], "lower": lo, "upper": hi,
               "g_hash": hashlib.sha256(np.round(g, 12).tobytes()).hexdigest(), "max_abs_g": float(np.max(np.abs(g)))}
        scored.append(row); matrices[w["start"]] = g
    ida_lo, ida_hi = lp_score(ida, Q, omega_root)-1e-8, min(lp_score(ida, X, o) for _,X,o in vectors)
    all_non = nonoverlap(windows)
    maxvals = [float(np.max(np.abs(matrices[x["start"]]))) for x in all_non]
    threshold = float(np.quantile(maxvals, .95, method="inverted_cdf"))
    # interval rank bounds use only values definitely / possibly no smaller than Ida.
    rank = {}
    for universe in ("FULL_QUALIFIED_REFERENCE", "STAGE_ERA_MATCHED_REFERENCE", "SAME_SEASON_STAGE_REFERENCE"):
        for label, pool in (("all", [x for x in scored if universe in x["universes"]]),
                            ("nonoverlap", [x for x in scored if x["start"] in {q["start"] for q in nonoverlap([w for w in windows if universe in w["universes"]])}])):
            rank[f"{universe}:{label}"] = {"n":len(pool), "definitely_ge":sum(x["lower"] >= ida_hi for x in pool),
                "possibly_ge":sum(x["upper"] >= ida_lo for x in pool)}
    def support_placebo(g, k):
        return {"lower":lp_score(g, shift(Q,k), shift(omega_root[:,None],k)[:,0])-1e-8,
                "upper":min(lp_score(g, shift(X,k), shift(o[:,None],k)[:,0]) for _,X,o in vectors)}
    ida_placebo = {str(k): support_placebo(ida, k) for k in range(-4,5)}
    sample_dates = [windows[i]["start"] for i in np.linspace(0, len(windows)-1, 12, dtype=int)]
    reference_placebo = {s:{str(k):support_placebo(matrices[s],k)["lower"] for k in (-4,0,4)} for s in sample_dates}
    result = {
      "artifact_type":"M7B_INDEPENDENT_REPLICATION", "status":"PASS", "aggregate_only":True,
      "forbidden_primary_numeric_outputs_read":False,
      "methods":{"estimator":"paired event-minus-seven-day, within-bin reference-common-support weights", "score":"M7A root LP lower minus 1e-8; min every frozen multistart initial feasible leaf plus best-known leaf", "solver":"SciPy HiGHS dual simplex"},
      "inputs":{"spec_sha256":sha(SPEC),"registry_sha256":sha(REGISTRY),"freeze_sha256":sha(FREEZE),"aggregate_tally_sha256":sha(W2),"m7a_tree_sha256":sha(TREE),"m7a_search_sha256":sha(SEARCH)},
      "ida":{"g":ida.tolist(),"g_hash":hashlib.sha256(np.round(ida,12).tobytes()).hexdigest(),"parity_max_abs":parity,"simplex_max_abs":max(abs(x["simplex_error"]) for x in ida_d),"interval":[ida_lo,ida_hi]},
      "reference":{"n":len(scored),"sample": [next(x for x in scored if x["start"]==s) for s in sample_dates],"interval_summary":{"lower_min":min(x["lower"] for x in scored),"upper_max":max(x["upper"] for x in scored),"median_upper":float(np.median([x["upper"] for x in scored]))}},
      "ranks":rank,"max_cell":{"n_nonoverlap":len(all_non),"quantile":.95,"threshold":threshold,"ida_max_abs":float(np.max(np.abs(ida))),"exceeds":bool(np.max(np.abs(ida))>threshold)},
      "placebos":{"ida":ida_placebo,"reference_stratified_sample":reference_placebo},
      "tolerances":{"parity":1e-10,"LP":1e-9,"certificate":1e-8},
      "self_check":{"status":"PASS","checks":["217 qualified windows","Ida G parity <=1e-10","all G finite","all interval lower<=upper"]}
    }
    if not all(math.isfinite(x["lower"]) and x["lower"]<=x["upper"]+1e-9 for x in scored): raise RuntimeError("interval self-check")
    (OUT / "M7B_INDEPENDENT_REPLICATION.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")

if __name__ == "__main__": main()
