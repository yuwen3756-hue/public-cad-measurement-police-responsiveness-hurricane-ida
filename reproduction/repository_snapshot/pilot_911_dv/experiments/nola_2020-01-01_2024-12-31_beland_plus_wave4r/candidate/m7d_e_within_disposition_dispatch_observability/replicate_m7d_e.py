"""Independent aggregate-only replication of M7D-E."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


HERE=Path(__file__).resolve().parent
PILOT=HERE.parents[3]
M7B=HERE.parent/"m7b_same_estimator_reference_geometry"
M7D=HERE.parent/"m7d_d_public_disposition_schema_completion"
RAW=PILOT/"source_data"/"socrata"/"nola_3pha-hum9"/"2021"/"cad_operational"
IDA=date(2021,8,29);NAMED=("GOA","RTF","NAT","UNF");CATS=NAMED+("OTHER","MISSING");TOL=1e-12


def norm(x):return "" if x is None else str(x).strip()


def cat(x):
    v=norm(x).upper().rstrip(".")
    return "MISSING" if not v or v in {"NONE","NULL"} else (v if v in NAMED else "OTHER")


def when(x):
    try:return datetime.fromisoformat(norm(x).replace("Z","+00:00")).replace(tzinfo=None) if norm(x) else None
    except ValueError:return None


def blank():return {"total":0,**{f"j{d}{a}":0 for d in (0,1) for a in (0,1)},**{f"h{j}_{r}":0 for j in ("01","11") for r in CATS}}


def independently_build():
    reg=json.loads((M7D/"M7D_D_PUBLIC_SOURCE_REGISTRY.json").read_text(encoding="utf-8"));digest=next(x["locked_annual_digest"] for x in reg["datasets"] if x["year"]==2021)
    side={}
    with gzip.open(M7D/"M7D_D_DISPOSITION_SIDECAR.csv.gz","rt",encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            if r["source_year"]=="2021":side[r["trace_token"]]=r["disposition"]
    # Independent layout: date -> half -> stratum.
    data=defaultdict(lambda:defaultdict(lambda:defaultdict(blank)))
    for path in sorted(RAW.glob("*.csv.gz")):
        with gzip.open(path,"rt",encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                tc=when(r.get("timecreate"))
                if tc is None or norm(r.get("selfinitiated")).upper()!="N":continue
                token=hashlib.sha256(f"{digest}||{norm(r.get('nopd_item'))}".encode()).hexdigest(); disp=cat(side[token])
                ta=when(r.get("timearrive"));d=int(bool(norm(r.get("timedispatch"))));a=int(ta is not None and ta>=tc)
                hb=("00-05","06-11","12-17","18-23")[tc.hour//6];s=f"{norm(r.get('initialtype')).upper() or 'UNKNOWN'}|{hb}|numeric"
                x=data[tc.date().isoformat()][tc.hour//12][s];x["total"]+=1;x[f"j{d}{a}"]+=1
                if a:x[f"h{d}{a}_{disp}"]+=1
    return data


def compute(data):
    masses=[];qrows=[];kit=[];witness=[];aggregate=[]
    frozen={}
    with (M7B/"M7B_REFERENCE_G_MATRICES.csv").open(encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            if r["window_start"]==IDA.isoformat():frozen[r["bin"]]=r
    parent=[]
    for i in range(10):
        day=IDA+timedelta(days=i//2);half=i%2;e=data[day.isoformat()][half];r=data[(day-timedelta(days=7)).isoformat()][half]
        common=sorted(set(e)&set(r));den=sum(r[s]["total"] for s in common);weights={s:r[s]["total"]/den for s in common}
        def z(side,field):return sum(w*side[s][field]/side[s]["total"] for s,w in weights.items())
        parent01=z(e,"j01")-z(r,"j01");parent11=z(e,"j11")-z(r,"j11")
        parent.extend((parent01-float(frozen[f"B{i+1}"]["Delta_J01"]),parent11-float(frozen[f"B{i+1}"]["Delta_J11"])))
        per={}
        for c in CATS:
            a01,b01=z(e,f"h01_{c}"),z(r,f"h01_{c}");a11,b11=z(e,f"h11_{c}"),z(r,f"h11_{c}")
            me,mr=a01+a11,b01+b11;qe=a11/me if me else None;qr=b11/mr if mr else None
            row={"bin":f"B{i+1}","disposition":c,"event_H01":a01,"reference_H01":b01,"Delta_H01":a01-b01,
                 "event_H11":a11,"reference_H11":b11,"Delta_H11":a11-b11,"event_m":me,"reference_m":mr}
            masses.append(row);qrows.append({"bin":row["bin"],"disposition":c,"q_event":qe,"q_reference":qr,"Delta_q":qe-qr if qe is not None and qr is not None else None})
            prod=(a01-b01)*(a11-b11);witness.append({"bin":row["bin"],"disposition":c,"product":prod,"falsified":prod<0})
            if qe is not None and qr is not None:
                m11=.5*(qe+qr)*(me-mr);w11=.5*(me+mr)*(qe-qr);m01=.5*(2-qe-qr)*(me-mr);w01=-.5*(me+mr)*(qe-qr)
                kit.append({"bin":row["bin"],"disposition":c,"status":"DEFINED","MASS_COMPONENT_11":m11,"WITHIN_DISPOSITION_COMPONENT_11":w11,
                            "residual_11":a11-b11-m11-w11,"MASS_COMPONENT_01":m01,"WITHIN_DISPOSITION_COMPONENT_01":w01,"residual_01":a01-b01-m01-w01})
            else:kit.append({"bin":row["bin"],"disposition":c,"status":"NOT_DEFINED_IN_CELL"})
            per[c]=(me,mr,qe,qr)
        te=sum(x[0] for x in per.values());tr=sum(x[1] for x in per.values());qae=sum(z(e,f"h11_{c}") for c in CATS)/te;qar=sum(z(r,f"h11_{c}") for c in CATS)/tr
        comp=within=0.0
        for c,(me,mr,qe,qr) in per.items():
            pe,pr=me/te,mr/tr;qe=qe if qe is not None else 0.0;qr=qr if qr is not None else 0.0
            comp+=.5*(qe+qr)*(pe-pr);within+=.5*(pe+pr)*(qe-qr)
        aggregate.append({"bin":f"B{i+1}","q_all_event":qae,"q_all_reference":qar,"Delta_q_all":qae-qar,
                          "composition_component":comp,"within_disposition_component":within,"residual":qae-qar-comp-within})
    return {"masses":masses,"q":qrows,"kitagawa":kit,"witnesses":witness,"aggregate":aggregate,"parent_parity_max":max(abs(x) for x in parent)}


def main():
    independent=compute(independently_build());independent["artifact_type"]="M7D_E_INDEPENDENT_AGGREGATES";independent["created_utc"]=datetime.now(timezone.utc).isoformat();independent["primary_tables_used"]=False
    frozen=HERE/"M7D_E_INDEPENDENT_AGGREGATES.json";frozen.write_text(json.dumps(independent,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    # Comparison-only reads begin after independent freeze.
    def csvmap(name):
        with (HERE/name).open(encoding="utf-8",newline="") as f:return {(r["bin"],r.get("disposition","")):r for r in csv.DictReader(f)}
    pm=csvmap("M7D_E_H_MASSES.csv");pq=csvmap("M7D_E_WITHIN_DISPOSITION_Q.csv");pk=csvmap("M7D_E_KITAGAWA_DECOMPOSITION.csv");pw=csvmap("M7D_E_COMPOSITION_ONLY_WITNESSES.csv")
    pa=json.loads((HERE/"M7D_E_AGGREGATE_KITAGAWA.json").read_text(encoding="utf-8"));pa={x["bin"]:x for x in pa["bins"]}
    residuals=[];status_ok=True
    for r in independent["masses"]:
        p=pm[(r["bin"],r["disposition"])]
        for x in ("event_H01","reference_H01","Delta_H01","event_H11","reference_H11","Delta_H11","event_m","reference_m"):residuals.append(r[x]-float(p[x]))
    for r in independent["q"]:
        p=pq[(r["bin"],r["disposition"])]
        for x in ("q_event","q_reference","Delta_q"):
            status_ok &= ((r[x] is None)==(p[x]==""))
            if r[x] is not None:residuals.append(r[x]-float(p[x]))
    for r in independent["kitagawa"]:
        p=pk[(r["bin"],r["disposition"])];status_ok &= r["status"]==p["status"]
        if r["status"]=="DEFINED":
            for x in ("MASS_COMPONENT_11","WITHIN_DISPOSITION_COMPONENT_11","MASS_COMPONENT_01","WITHIN_DISPOSITION_COMPONENT_01"):residuals.append(r[x]-float(p[x]))
    for r in independent["witnesses"]:
        p=pw[(r["bin"],r["disposition"])];residuals.append(r["product"]-float(p["product"]));status_ok &= r["falsified"]==(p["composition_only_model"]=="FALSIFIED_FOR_CELL")
    for r in independent["aggregate"]:
        p=pa[r["bin"]]
        for x in ("Delta_q_all","composition_component","within_disposition_component"):residuals.append(r[x]-float(p[x]))
    maxres=max(abs(x) for x in residuals);identity=max([abs(x.get("residual_01",0)) for x in independent["kitagawa"]]+[abs(x.get("residual_11",0)) for x in independent["kitagawa"]]+[abs(x["residual"]) for x in independent["aggregate"]])
    passed=status_ok and max(maxres,identity,independent["parent_parity_max"])<=TOL
    result={"artifact_type":"M7D_E_INDEPENDENT_REPLICATION","primary_tables_used_as_numeric_inputs":False,
            "primary_tables_opened_only_after_independent_freeze":True,"numeric_comparisons":len(residuals),"status_comparisons_pass":status_ok,
            "max_abs_numeric_residual":maxres,"independent_identity_max_abs_residual":identity,
            "independent_parent_parity_max_abs_residual":independent["parent_parity_max"],"tolerance":TOL,"overall":"PASS" if passed else "FAIL"}
    (HERE/"M7D_E_INDEPENDENT_REPLICATION.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    results=json.loads((HERE/"M7D_E_RESULTS.json").read_text(encoding="utf-8"));results["replication"]="PASS" if passed else "FAIL";results["status"]="M7D_E_READY_FOR_EXTERNAL_MEASUREMENT_REVIEW" if passed else "M7D_E_BLOCKED_BY_REPLICATION"
    (HERE/"M7D_E_RESULTS.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    manifest=[]
    for p in sorted(x for x in HERE.iterdir() if x.is_file() and x.name!="artifact_manifest.json"):
        manifest.append({"path":str(p.resolve()),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    (HERE/"artifact_manifest.json").write_text(json.dumps({"artifact_type":"M7D_E_ARTIFACT_MANIFEST","files":manifest},indent=2,sort_keys=True)+"\n",encoding="utf-8")


if __name__=="__main__":main()
