"""BELAND-PLUS M7D-E within-disposition dispatch-field observability.

Uses only the admitted M7D-D hashed disposition sidecar and locked 2021 CAD.
All quantities are public administrative field observables.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


OUT = Path(__file__).resolve().parent
CANDIDATE = OUT.parent
PILOT = OUT.parents[3]
M7B = CANDIDATE / "m7b_same_estimator_reference_geometry"
M7C = CANDIDATE / "m7d_c_public_administrative_stage_flow"
M7D = CANDIDATE / "m7d_d_public_disposition_schema_completion"
RAW = PILOT / "source_data" / "socrata" / "nola_3pha-hum9" / "2021" / "cad_operational"
IDA = date(2021, 8, 29)
NAMED = ("GOA", "RTF", "NAT", "UNF")
CATS = NAMED + ("OTHER", "MISSING")
TOL_PARENT = 1e-10
TOL_IDENTITY = 1e-12
MIN_REFERENCE_N = 20
DOMINANCE_RATIO = 2.0


def clean(x) -> str:
    return "" if x is None else str(x).strip()


def category(x) -> str:
    value = clean(x).upper().rstrip(".")
    if not value or value in {"NONE", "NULL"}: return "MISSING"
    return value if value in NAMED else "OTHER"


def parse_dt(x):
    try: return datetime.fromisoformat(clean(x).replace("Z", "+00:00")).replace(tzinfo=None) if clean(x) else None
    except ValueError: return None


def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()


def record(path: Path) -> dict:
    return {"path":str(path.resolve()),"bytes":path.stat().st_size,"sha256":sha(path)}


def write_json(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8",newline="")


def write_csv(name,rows,fields=None):
    fields=fields or list(rows[0])
    with (OUT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)


def fresh():
    return {"n":0,**{f"J{d}{a}":0 for d in (0,1) for a in (0,1)},
            **{f"H{j}_{r}":0 for j in ("01","11") for r in CATS}}


def load_sidecar_and_tally():
    registry=json.loads((M7D/"M7D_D_PUBLIC_SOURCE_REGISTRY.json").read_text(encoding="utf-8"))
    digest=next(x["locked_annual_digest"] for x in registry["datasets"] if x["year"]==2021)
    disposition={}
    with gzip.open(M7D/"M7D_D_DISPOSITION_SIDECAR.csv.gz","rt",encoding="utf-8",newline="") as f:
        for row in csv.DictReader(f):
            if row["source_year"]=="2021": disposition[row["trace_token"]]=row["disposition"]
    cube=defaultdict(lambda:defaultdict(fresh)); joined=0
    paths=sorted(RAW.glob("*.csv.gz"))
    if len(paths)!=12: raise RuntimeError("locked 2021 cache incomplete")
    for path in paths:
        with gzip.open(path,"rt",encoding="utf-8-sig",newline="") as f:
            for row in csv.DictReader(f):
                tc=parse_dt(row.get("timecreate"))
                if tc is None or clean(row.get("selfinitiated")).upper()!="N": continue
                token=hashlib.sha256(f"{digest}||{clean(row.get('nopd_item'))}".encode()).hexdigest()
                if token not in disposition: raise RuntimeError("M7D-D sidecar join failure")
                ta=parse_dt(row.get("timearrive")); d=int(bool(clean(row.get("timedispatch")))); a=int(ta is not None and ta>=tc)
                hb=("00-05","06-11","12-17","18-23")[tc.hour//6]
                s=f"{clean(row.get('initialtype')).upper() or 'UNKNOWN'}|{hb}|numeric"
                v=cube[(tc.date().isoformat(),tc.hour//12)][s]; v["n"]+=1; v[f"J{d}{a}"]+=1
                if a: v[f"H{d}{a}_{category(disposition[token])}"]+=1
                joined+=1
    return {k:dict(v) for k,v in cube.items()},joined


def compute_window(cube,start):
    rows=[]
    for b in range(10):
        day=start+timedelta(days=b//2); half=b%2
        e=cube.get((day.isoformat(),half),{}); r=cube.get(((day-timedelta(days=7)).isoformat(),half),{})
        common=sorted(set(e)&set(r)); den=sum(r[s]["n"] for s in common); w={s:r[s]["n"]/den for s in common} if den else {}
        def mass(side,field): return sum(weight*side[s][field]/side[s]["n"] for s,weight in w.items())
        row={"window_start":start.isoformat(),"bin":f"B{b+1}","common_support_strata":len(common),"weight_sum":sum(w.values())}
        for j in ("01","11"):
            row[f"event_J{j}"]=mass(e,f"J{j}");row[f"reference_J{j}"]=mass(r,f"J{j}")
            row[f"Delta_J{j}"]=row[f"event_J{j}"]-row[f"reference_J{j}"]
            for cat in CATS:
                row[f"event_H{j}_{cat}"]=mass(e,f"H{j}_{cat}");row[f"reference_H{j}_{cat}"]=mass(r,f"H{j}_{cat}")
                row[f"Delta_H{j}_{cat}"]=row[f"event_H{j}_{cat}"]-row[f"reference_H{j}_{cat}"]
        rows.append(row)
    return rows


def analyze(ida_rows):
    h=[]; qrows=[]; kit=[]; witnesses=[]; aggregate=[]; agg_kit=[]
    for row in ida_rows:
        for cat in CATS:
            h01e,h01r=row[f"event_H01_{cat}"],row[f"reference_H01_{cat}"]
            h11e,h11r=row[f"event_H11_{cat}"],row[f"reference_H11_{cat}"]
            me,mr=h01e+h11e,h01r+h11r
            qe=h11e/me if me>0 else None; qr=h11r/mr if mr>0 else None
            h.append({"bin":row["bin"],"disposition":cat,"event_H01":h01e,"reference_H01":h01r,"Delta_H01":h01e-h01r,
                      "event_H11":h11e,"reference_H11":h11r,"Delta_H11":h11e-h11r,"event_m":me,"reference_m":mr})
            qrows.append({"bin":row["bin"],"disposition":cat,"q_event":qe,"q_reference":qr,
                          "Delta_q":qe-qr if qe is not None and qr is not None else None,
                          "status":"DEFINED" if qe is not None and qr is not None else "NOT_DEFINED_IN_CELL"})
            product=(h01e-h01r)*(h11e-h11r)
            witnesses.append({"bin":row["bin"],"disposition":cat,"Delta_H01":h01e-h01r,"Delta_H11":h11e-h11r,
                              "product":product,"composition_only_model":"FALSIFIED_FOR_CELL" if product<0 else "NOT_FALSIFIED_BY_SIGN_WITNESS"})
            if qe is not None and qr is not None:
                mass11=.5*(qe+qr)*(me-mr); within11=.5*(me+mr)*(qe-qr)
                mass01=.5*((1-qe)+(1-qr))*(me-mr); within01=-.5*(me+mr)*(qe-qr)
                kit.append({"bin":row["bin"],"disposition":cat,"status":"DEFINED","event_m":me,"reference_m":mr,
                            "q_event":qe,"q_reference":qr,"Delta_H11":h11e-h11r,"MASS_COMPONENT_11":mass11,
                            "WITHIN_DISPOSITION_COMPONENT_11":within11,"identity_residual_11":h11e-h11r-mass11-within11,
                            "Delta_H01":h01e-h01r,"MASS_COMPONENT_01":mass01,"WITHIN_DISPOSITION_COMPONENT_01":within01,
                            "identity_residual_01":h01e-h01r-mass01-within01})
            else:
                kit.append({"bin":row["bin"],"disposition":cat,"status":"NOT_DEFINED_IN_CELL","event_m":me,"reference_m":mr,
                            "q_event":qe,"q_reference":qr,"Delta_H11":h11e-h11r,"MASS_COMPONENT_11":None,
                            "WITHIN_DISPOSITION_COMPONENT_11":None,"identity_residual_11":None,"Delta_H01":h01e-h01r,
                            "MASS_COMPONENT_01":None,"WITHIN_DISPOSITION_COMPONENT_01":None,"identity_residual_01":None})
        total_e=row["event_J01"]+row["event_J11"];total_r=row["reference_J01"]+row["reference_J11"]
        qall_e=row["event_J11"]/total_e if total_e else None;qall_r=row["reference_J11"]/total_r if total_r else None
        aggregate.append({"bin":row["bin"],"q_all_event":qall_e,"q_all_reference":qall_r,
                          "Delta_q_all":qall_e-qall_r if qall_e is not None and qall_r is not None else None,
                          "event_arrival_observed_mass":total_e,"reference_arrival_observed_mass":total_r})
        if qall_e is None or qall_r is None: continue
        comp=0.0;within=0.0;cat_rows=[]
        for cat in CATS:
            me=row[f"event_H01_{cat}"]+row[f"event_H11_{cat}"];mr=row[f"reference_H01_{cat}"]+row[f"reference_H11_{cat}"]
            pie=me/total_e;pir=mr/total_r
            qe=row[f"event_H11_{cat}"]/me if me else 0.0;qr=row[f"reference_H11_{cat}"]/mr if mr else 0.0
            cc=.5*(qe+qr)*(pie-pir);wc=.5*(pie+pir)*(qe-qr);comp+=cc;within+=wc
            cat_rows.append({"disposition":cat,"pi_event":pie,"pi_reference":pir,"q_event_effective":qe,"q_reference_effective":qr,
                             "composition_component":cc,"within_component":wc,"zero_mass_q_convention":bool(not me or not mr)})
        delta=qall_e-qall_r
        agg_kit.append({"bin":row["bin"],"Delta_q_all":delta,"composition_component":comp,"within_disposition_component":within,
                        "identity_residual":delta-comp-within,"categories":cat_rows})
    return h,qrows,kit,witnesses,aggregate,agg_kit


def empirical(ida,values):
    vals=[v for v in values if v is not None and math.isfinite(v)]
    n=len(vals)
    if ida is None or n<MIN_REFERENCE_N:
        return {"status":"DESCRIPTIVE_ONLY","reference_defined_n":n,"minimum_required":MIN_REFERENCE_N,"ida_value":ida}
    vals=sorted(vals)
    return {"status":"ADEQUATE_DESCRIPTIVE_REFERENCE","reference_defined_n":n,"ida_value":ida,
            "reference_min":vals[0],"reference_max":vals[-1],"rank_ascending":1+sum(v<ida for v in vals),
            "add_one_lower_tail":(1+sum(v<=ida for v in vals))/(n+1),"add_one_upper_tail":(1+sum(v>=ida for v in vals))/(n+1)}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    inputs=[M7B/"M7B_IDA_ABNORMAL_CELLS.csv",M7B/"M7B_REFERENCE_WINDOW_REGISTRY.json",M7B/"M7B_REFERENCE_G_MATRICES.csv",
            M7C/"M7D_C_RESULTS.json",M7C/"M7D_C_K_DECOMPOSITION.csv",M7D/"M7D_D_DISPOSITION_SIDECAR.csv.gz",
            M7D/"M7D_D_DISPOSITION_SEMANTIC_REGISTRY.json",M7D/"M7D_D_DISPOSITION_DECOMPOSITION.csv",M7D/"M7D_D_SNAPSHOT_RECONCILIATION.json"]
    write_json("M7D_E_FROZEN_INPUTS.json",{"artifact_type":"M7D_E_FROZEN_INPUTS","created_utc":datetime.now(timezone.utc).isoformat(),
        "files":[record(p) for p in inputs],"minimum_2021_reference_n":MIN_REFERENCE_N,"dominance_ratio":DOMINANCE_RATIO,
        "zero_mass_aggregate_q_convention":"q=0 only inside exact aggregate identity when category mass is zero; cell q remains NOT_DEFINED_IN_CELL"})
    cube,joined=load_sidecar_and_tally();ida=compute_window(cube,IDA)
    h,qrows,kit,witnesses,aggregate,agg_kit=analyze(ida)
    write_csv("M7D_E_H_MASSES.csv",h);write_csv("M7D_E_WITHIN_DISPOSITION_Q.csv",qrows);write_csv("M7D_E_KITAGAWA_DECOMPOSITION.csv",kit)
    write_csv("M7D_E_COMPOSITION_ONLY_WITNESSES.csv",witnesses);write_csv("M7D_E_AGGREGATE_Q.csv",aggregate)
    write_json("M7D_E_AGGREGATE_KITAGAWA.json",{"artifact_type":"M7D_E_AGGREGATE_KITAGAWA","zero_mass_convention":"documented in frozen inputs","bins":agg_kit})

    # Parent and predecessor parity.
    frozen_g={}
    with (M7B/"M7B_REFERENCE_G_MATRICES.csv").open(encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            if r["window_start"]==IDA.isoformat():frozen_g[r["bin"]]=r
    parent_res=[row[f"Delta_J{j}"]-float(frozen_g[row["bin"]][f"Delta_J{j}"]) for row in ida for j in ("01","11")]
    drows={(r["bin"],r["parent"]):r for r in csv.DictReader((M7D/"M7D_D_DISPOSITION_DECOMPOSITION.csv").open(encoding="utf-8",newline=""))}
    hmap={(r["bin"],r["disposition"]):r for r in h};predecessor_res=[]
    for (b,j),r in drows.items():
        for cat in CATS: predecessor_res.append(float(r[f"Delta_H_{cat}"])-float(hmap[(b,cat)][f"Delta_H{j[1:]}"]))
    kit_res=[abs(float(r[x])) for r in kit if r["status"]=="DEFINED" for x in ("identity_residual_01","identity_residual_11")]
    agg_res=[abs(r["identity_residual"]) for r in agg_kit]

    # Prespecified 2021-only reference distribution.
    registry=json.loads((M7B/"M7B_REFERENCE_WINDOW_REGISTRY.json").read_text(encoding="utf-8"))
    refs=[r for r in registry["windows"] if r["start"].startswith("2021-")]
    reference_windows={r["start"]:analyze(compute_window(cube,date.fromisoformat(r["start"])))[1] for r in refs}
    qmap={(r["bin"],r["disposition"]):r for r in qrows};ref_results=[]
    for b in ("B6","B7"):
        for cat in NAMED:
            values=[]
            for start,rows in reference_windows.items():
                rr=next(x for x in rows if x["bin"]==b and x["disposition"]==cat);values.append(rr["Delta_q"])
            focal=qmap[(b,cat)]["Delta_q"]
            ref_results.append({"bin":b,"disposition":cat,"candidate_2021_reference_n":len(refs),**empirical(focal,values)})
    write_json("M7D_E_2021_REFERENCE_RESULTS.json",{"artifact_type":"M7D_E_2021_REFERENCE_RESULTS","selection":"frozen eligible M7B registry rows with start year 2021",
        "outcome_based_selection":False,"exchangeability_claimed":False,"results":ref_results})

    primary=[]
    for b in ("B6","B7"):
        ak=next(x for x in agg_kit if x["bin"]==b);a=abs(ak["composition_component"]);w=abs(ak["within_disposition_component"])
        case="COMPOSITION_DOMINATES" if a>=DOMINANCE_RATIO*w else ("WITHIN_DISPOSITION_DOMINATES" if w>=DOMINANCE_RATIO*a else "BOTH_MATERIAL")
        primary.append({"bin":b,"Delta_q_all":ak["Delta_q_all"],"composition_component":ak["composition_component"],
                        "within_disposition_component":ak["within_disposition_component"],"interpretation_case":case})
    parity=max(max(abs(x) for x in parent_res),max(abs(x) for x in predecessor_res));identity=max(kit_res+agg_res)
    status="M7D_E_BLOCKED_BY_ESTIMATOR_PARITY" if parity>TOL_PARENT or identity>TOL_IDENTITY else "M7D_E_BLOCKED_BY_REPLICATION"
    write_json("M7D_E_RESULTS.json",{"artifact_type":"M7D_E_RESULTS","status":status,"primary_results":primary,
        "joined_eligible_rows":joined,"parent_estimator_parity_max_abs_residual":parity,"kitagawa_identity_max_abs_residual":identity,
        "composition_only_falsified_primary_cells":sum(r["composition_only_model"]=="FALSIFIED_FOR_CELL" and r["bin"] in {"B6","B7"} and r["disposition"] in NAMED for r in witnesses),
        "closure_firewall":"M7D-C closure result hash-bound only; not rerun or counted as independent evidence",
        "claims_excluded":["physical dispatch","response probability","queue","performance","deprioritization","capacity","causality"]})
    finalize()


def finalize():
    write_json("artifact_manifest.json",{"artifact_type":"M7D_E_ARTIFACT_MANIFEST","files":[record(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!="artifact_manifest.json"]})


if __name__=="__main__":main()
