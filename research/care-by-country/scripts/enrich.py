"""Add the optional standard-named fields (notes/formats.md, "Recommendation for comparison.json") to comparison.json.

Run after merge.py. Reads only local tables in scripts/codes/; never changes an existing field.
Re-running is safe: the added fields are dropped and rebuilt.

usage: python3 -I enrich.py RESEARCH_DIR
"""
import collections
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
codes = Path(__file__).with_name("codes")

# ISO 3166-1 alpha-2. Europe, European Union, International and WHO have no country code.
COUNTRY = {
    "Argentina": "AR", "Australia": "AU", "Brazil": "BR", "Canada": "CA", "Chile": "CL", "China": "CN",
    "Denmark": "DK", "Finland": "FI", "France": "FR", "Germany": "DE", "India": "IN", "Ireland": "IE",
    "Italy": "IT", "Japan": "JP", "Mexico": "MX", "Netherlands": "NL", "New Zealand": "NZ", "Norway": "NO",
    "Saudi Arabia": "SA", "Singapore": "SG", "South Korea": "KR", "Spain": "ES", "Sweden": "SE",
    "Switzerland": "CH", "Taiwan": "TW", "UK": "GB", "US": "US",
    "Europe": None, "European Union": None, "International": None, "WHO": None,
}
# ISO 3166-2, matched on the start of `jurisdiction`. Other jurisdictions (EU, consensus groups) get null.
REGION = {"England": "GB-ENG", "Scotland": "GB-SCT", "Ontario": "CA-ON", "Queensland": "AU-QLD"}
# ICD-11 MMS, checked in the WHO ICD-11 browser (release 2026-01) on 2026-10-22.
ICD11 = {
    "chronic insomnia": "7A00",          # Chronic insomnia
    "obstructive sleep apnea": "7A41",   # Obstructive sleep apnoea
    "pediatric OSA": "7A41",             # 7A41's definition includes the paediatric criterion
    "narcolepsy": "7A20",                # Narcolepsy (7A20.0 type 1, 7A20.1 type 2)
    "restless legs": "7A80",             # Restless legs syndrome
    "pediatric insomnia": None,          # rows mix short-term and chronic; 7A00 or 7A01 per row, not checked
    "circadian rhythm disorders": None,  # rows span several of 7A60-7A65
    "other": None,
}
PATHWAY_FIELDS = ["performer", "setting", "step", "after", "target", "payer", "program", "ruleType"]
NEW = ["countryCode", "regionCode", "conditionCodes", "drugCodes", "strengthGrade", "certaintyOfEvidence",
       "gradingSystem"] + PATHWAY_FIELDS

drugs = json.loads((codes / "drug-codes.json").read_text())["drugs"]
strength = json.loads((codes / "strength-map.json").read_text())["map"]
pathway = json.loads((codes / "pathway-coverage.json").read_text())["rows"]

path = root / "comparison.json"
rows = json.loads(path.read_text())
before = [{k: v for k, v in r.items() if k not in NEW} for r in rows]
problems = []

out = []
for r in before:
    e = dict(r)
    if r["country"] not in COUNTRY:
        problems.append(f"no country code decision: {r['country']}")
    e["countryCode"] = COUNTRY.get(r["country"])
    j = r.get("jurisdiction") or ""
    e["regionCode"] = next((c for name, c in REGION.items() if j.startswith(name)), None)
    if r["condition"] not in ICD11:
        problems.append(f"no ICD-11 decision: {r['condition']}")
    e["conditionCodes"] = {"icd11": ICD11.get(r["condition"])}
    e["drugCodes"] = []
    for d in r.get("drugs") or []:
        c = drugs.get(d)
        if c is None:
            problems.append(f"no drug code decision: {d}")
            c = {}
        e["drugCodes"].append({"name": d, "atc": c.get("atc"), "rxnorm": c.get("rxnorm")})
    if r["strength"] not in strength:
        problems.append(f"no strength decision: {r['strength']!r}")
    e["strengthGrade"], e["certaintyOfEvidence"], e["gradingSystem"] = strength.get(r["strength"], [None, None, None])
    p = pathway.get(r["id"], {})
    if p and r["layer"] == "guideline":
        problems.append(f"pathway fields on a guideline row: {r['id']}")
    for k in PATHWAY_FIELDS:
        e[k] = p.get(k)
    out.append(e)

for k in set(pathway) - {r["id"] for r in rows}:
    problems.append(f"pathway-coverage.json id not in data: {k}")
# Existing values must come through untouched.
assert [{k: v for k, v in e.items() if k not in NEW} for e in out] == before
if problems:
    sys.exit("\n".join(sorted(set(problems))))

path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
n = len(out)
print(n, "rows enriched")
for k in ["countryCode", "regionCode", "strengthGrade", "certaintyOfEvidence", "gradingSystem", "payer", "ruleType", "target"]:
    print(f"  {k}: {sum(1 for e in out if e[k])}/{n} filled")
print("  conditionCodes.icd11:", sum(1 for e in out if e["conditionCodes"]["icd11"]), "/", n)
dc = [d for e in out for d in e["drugCodes"]]
print("  drugCodes:", len(dc), "mentions,", sum(1 for d in dc if d["atc"]), "with ATC,", sum(1 for d in dc if d["rxnorm"]), "with RxNorm")
print("  strengthGrade:", dict(collections.Counter(e["strengthGrade"] for e in out)))
