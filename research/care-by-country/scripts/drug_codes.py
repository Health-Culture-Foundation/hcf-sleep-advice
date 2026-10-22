"""Write scripts/codes/drug-codes.json: ATC (and RxNorm where exact) for every name in a row's `drugs`.

ATC codes below were checked by hand against the WHO ATC/DDD index (https://atcddd.fhi.no/atc_ddd_index/,
index last updated 2026-01-20) on 2026-10-22. RxNorm ids are fetched from NLM RxNav at run time.

ATC codes are WHOCC material (https://atcddd.fhi.no/copyright_disclaimer/): store the bare code only, with
no ATC level names, hierarchy or DDDs, and keep them out of the dataset's CC BY licence (see LICENSE).

usage: python3 -I drug_codes.py RESEARCH_DIR
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

root = Path(sys.argv[1])
S = {}


def s(names, atc, other=None, note=None):
    for n in names.split("|"):
        S[n] = {"atc": atc}
        if other:
            S[n]["atcOther"] = other
        if note:
            S[n]["note"] = note


s("acetazolamide", "S01EC01", note="The index gives acetazolamide one code, used for all routes.")
s("agomelatine", "N06AX22")
s("alimemazine", "R06AD01")
s("amitriptyline", "N06AA09")
s("amphetamine", "N06BA01", note="WHO name: amfetamine.")
s("armodafinil", "N06BA13")
s("atomoxetine", "N06BA09")
s("brotizolam", "N05CD09")
s("buprenorphine", "N02AE01", ["N07BC01"], "N02AE01 = analgesic; N07BC01 = opioid dependence.")
s("bupropion", "N06AX12")
s("cabergoline", "N04BC06", ["G02CB03"], "N04BC06 = dopamine agonist; G02CB03 = prolactin inhibitor.")
s("cannabinoids", "N02BG10")
s("carbamazepine", "N03AF01")
s("chlorprothixene", "N05AF03")
s("clarithromycin", "J01FA09")
s("clomipramine", "N06AA04")
s("clonazepam", "N03AE01")
s("codeine", "R05DA04", note="The index gives plain codeine one code; analgesic codeine products are coded as combinations.")
s("daridorexant", "N05CJ03")
s("dexamethasone", "H02AB02",
  ["A01AC02", "C05AA09", "D07AB19", "D07XB05", "D10AA03", "R01AD03", "S01BA01", "S01CB01", "S02BA06", "S03BA01"],
  "H02AB02 = systemic; the others are local or topical forms.")
s("dexamfetamine|dextroamphetamine", "N06BA02")
s("diazepam", "N05BA01")
s("diphenhydramine", "R06AA02", ["D04AA32"], "R06AA02 = systemic; D04AA32 = topical.")
s("dipyridamole", "B01AC07")
s("doxepin", "N06AA12", ["D04AX01"], "N06AA12 = systemic; D04AX01 = topical.")
s("doxylamine", "R06AA09")
s("eszopiclone", "N05CF04")
s("etizolam", "N05BA19")
s("ferrous sulfate", "B03AA07")
s("flunitrazepam", "N05CD03")
s("flurazepam", "N05CD01")
s("gabapentin", "N02BF01")
s("hydroxyzine", "N05BB01")
s("ibuprofen", "M01AE01", ["C01EB16", "G02CC01", "M02AA13", "R02AX02"],
  "M01AE01 = oral anti-inflammatory; the others are IV (ductus), vaginal, topical and throat forms.")
s("lemborexant", "N05CJ02")
s("levodopa", "N04BA01", ["N04BA02"],
  "N04BA02 = levodopa with decarboxylase inhibitor (the usual product); the row says only 'levodopa'.")
s("levomepromazine", "N05AA02")
s("lisdexamfetamine", "N06BA12")
s("lorazepam", "N05BA06")
s("lormetazepam", "N05CD06")
s("melatonin|melatonin (immediate-release)|melatonin (prolonged-release)|melatonin 2 mg PR|melatonin 2 mg prolonged-release",
  "N05CH01")
s("melperone", "N05AD03")
s("methylphenidate", "N06BA04")
s("mianserin", "N06AX03")
s("midazolam", "N05CD08")
s("mirtazapine", "N06AX11")
s("modafinil", "N06BA07")
s("montelukast", "R03DC03")
s("nitrazepam", "N05CD02")
s("olanzapine", "N05AH03")
s("oxazepam", "N05BA04")
s("oxybutynin", "G04BD04")
s("oxycodone", "N02AA05")
s("acetaminophen", "N02BE01", note="WHO name: paracetamol.")
s("pipamperone", "N05AD05")
s("pitolisant", "N07XX11")
s("pramipexole", "N04BC05")
s("pregabalin", "N02BF02")
s("promethazine", "R06AD02", ["D04AA10"], "R06AD02 = systemic; D04AA10 = topical.")
s("prothipendyl", "N05AX07")
s("quetiapine", "N05AH04")
s("ramelteon", "N05CH02")
s("ropinirole", "N04BC04")
s("rotigotine", "N04BC09")
s("sodium oxybate", "N07XX04", ["N01AX11"], "N07XX04 = other nervous system drugs (narcolepsy); N01AX11 = anaesthetic.")
s("solriamfetol", "N06BA14")
s("sulthiame", "N03AX03", note="WHO name: sultiame.")
s("suvorexant", "N05CJ01")
s("tasimelteon", "N05CH03")
s("temazepam", "N05CD07")
s("tiagabine", "N03AG06")
s("tirzepatide", "A10BX16")
s("trazodone", "N06AX05")
s("triazolam", "N05CD05")
s("trimipramine", "N06AA06")
s("tryptophan", "N06AX02")
s("valerian", "N05CM09", note="Coded as valerian root.")
s("valproic acid", "N03AG01")
s("venlafaxine", "N06AX16")
s("zaleplon", "N05CF03")
s("zolpidem", "N05CF02")
s("zonisamide", "N03AX15")
s("zopiclone", "N05CF01")
# Classes that match exactly one ATC group
s("Z-drugs", "N05CF", note="ATC group, not a single substance.")
s("antipsychotics|antipsychotics (class, e.g. quetiapine)", "N05A", note="ATC group, not a single substance.")
s("opioids", "N02A", note="ATC group, not a single substance.")
s("hypnotics", "N05C", note="ATC group, not a single substance.")
# No confirmed code
for names, note in {
    "benzodiazepines|long-acting benzodiazepines|shorter-acting benzodiazepines":
        "Class spread over more than one ATC group; no single code.",
    "antihistamines": "Class spread over more than one ATC group; no single code.",
    "sedating antidepressants": "Not an ATC group.",
    "intranasal corticosteroids": "Several substances; the row names no single drug.",
    "ferric carboxymaltose|iron sucrose|iron dextran|ferumoxytol":
        "Not listed by name in the index; injected iron has only a group code (B03AC). Left null until checked.",
    "gabapentin enacarbil": "Not listed by name in the index.",
    "calcium/magnesium/potassium/sodium oxybates (low-sodium oxybate)": "Not listed by name in the index.",
    "aceprometazine+meprobamate":
        "Combination; aceprometazine is not listed by name. N05CX01 is a candidate, unconfirmed.",
    "lavender": "The index lists only lavender oil (N05BX05); the row does not say which preparation.",
    "Chaihu Shugan San|Xiaoyao San|cannabis|chamomile|hops|kava|kava-kava|melissa|passiflora|passionflower|saffron":
        "Not listed by name in the index (herbal or traditional preparation).",
}.items():
    s(names, None, note=note)

# RxNorm: only an exact, single ingredient (TTY=IN) match. Query by the row's name (US spelling).


def rxnorm(name):
    q = urllib.parse.urlencode({"name": name, "search": 0})
    ids = json.load(urllib.request.urlopen(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?{q}", timeout=20))
    ids = ids.get("idGroup", {}).get("rxnormId", [])
    if len(ids) != 1:
        return None
    p = json.load(urllib.request.urlopen(f"https://rxnav.nlm.nih.gov/REST/rxcui/{ids[0]}/property.json?propName=TTY", timeout=20))
    tty = [c["propValue"] for c in (p.get("propConceptGroup") or {}).get("propConcept", [])]
    return ids[0] if tty == ["IN"] else None


cache = {}
for n, v in S.items():
    if v["atc"] and len(v["atc"]) == 7:  # substances only
        q = n.split(" (")[0].split(" 2 mg")[0]
        if q not in cache:
            cache[q] = rxnorm(q)
            time.sleep(0.1)
        v["rxnorm"] = cache[q]

names = {d for r in json.loads((root / "comparison.json").read_text()) for d in r["drugs"] or []}
missing = names - set(S)
if missing:
    sys.exit(f"names with no decision: {sorted(missing)}")
out = {
    "_source": {
        "atc": "WHO Collaborating Centre for Drug Statistics Methodology, ATC/DDD Index "
               "(https://atcddd.fhi.no/atc_ddd_index/), index last updated 2026-01-20, checked 2026-10-22. "
               "Use of ATC codes in an open dataset is an open question (see README).",
        "rxnorm": "NLM RxNav REST API (https://rxnav.nlm.nih.gov/), exact name, single ingredient (TTY=IN) only.",
        "licence": "ATC codes are WHOCC material, excluded from the dataset's CC BY licence. Bare codes only: no ATC names, hierarchy or DDDs. Source: WHO Collaborating Centre for Drug Statistics Methodology, https://atcddd.fhi.no/copyright_disclaimer/",
        "rule": "atc is null unless the index lists the name (or its WHO spelling) as a substance, or the name is a "
                "class matching exactly one ATC group. atcOther lists other codes the index gives the same substance; "
                "atc is the systemic code in the group that fits sleep use.",
    },
    "drugs": dict(sorted(((k, v) for k, v in S.items() if k in names), key=lambda kv: kv[0].lower())),
}
(root / "scripts" / "codes" / "drug-codes.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
hits = [n for n, v in out["drugs"].items() if v.get("rxnorm")]
print(len(out["drugs"]), "names;", sum(1 for v in out["drugs"].values() if v["atc"]), "with ATC;", len(hits), "with RxNorm")
print("no RxNorm:", [n for n, v in out["drugs"].items() if "rxnorm" in v and not v["rxnorm"]])
