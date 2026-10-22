"""Write scripts/codes/drug-codes.json: ATC (and RxNorm where exact) for every name in a row's `drugs`.

ATC codes below were checked by hand against the WHO ATC/DDD index (https://atcddd.fhi.no/atc_ddd_index/,
index last updated 2026-01-20) on 2026-10-22. RxNorm ids are fetched from NLM RxNav at run time.

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


def s(names, atc, atc_name, other=None, note=None):
    for n in names.split("|"):
        S[n] = {"atc": atc, "atcName": atc_name}
        if other:
            S[n]["atcOther"] = other
        if note:
            S[n]["note"] = note


s("acetazolamide", "S01EC01", "acetazolamide", note="The index lists acetazolamide only under S01EC (antiglaucoma), which covers systemic use.")
s("agomelatine", "N06AX22", "agomelatine")
s("alimemazine", "R06AD01", "alimemazine")
s("amitriptyline", "N06AA09", "amitriptyline")
s("amphetamine", "N06BA01", "amfetamine", note="WHO name: amfetamine.")
s("armodafinil", "N06BA13", "armodafinil")
s("atomoxetine", "N06BA09", "atomoxetine")
s("brotizolam", "N05CD09", "brotizolam")
s("buprenorphine", "N02AE01", "buprenorphine", ["N07BC01"], "N02AE01 = analgesic; N07BC01 = opioid dependence.")
s("bupropion", "N06AX12", "bupropion")
s("cabergoline", "N04BC06", "cabergoline", ["G02CB03"], "N04BC06 = dopamine agonist; G02CB03 = prolactin inhibitor.")
s("cannabinoids", "N02BG10", "cannabinoids")
s("carbamazepine", "N03AF01", "carbamazepine")
s("chlorprothixene", "N05AF03", "chlorprothixene")
s("clarithromycin", "J01FA09", "clarithromycin")
s("clomipramine", "N06AA04", "clomipramine")
s("clonazepam", "N03AE01", "clonazepam")
s("codeine", "R05DA04", "codeine", note="Plain codeine is listed only under R05DA (cough suppressants); analgesic codeine is classed in combinations (N02AA59, N02AJ).")
s("daridorexant", "N05CJ03", "daridorexant")
s("dexamethasone", "H02AB02", "dexamethasone",
  ["A01AC02", "C05AA09", "D07AB19", "D07XB05", "D10AA03", "R01AD03", "S01BA01", "S01CB01", "S02BA06", "S03BA01"],
  "H02AB02 = systemic; the others are local or topical forms.")
s("dexamfetamine|dextroamphetamine", "N06BA02", "dexamfetamine")
s("diazepam", "N05BA01", "diazepam")
s("diphenhydramine", "R06AA02", "diphenhydramine", ["D04AA32"], "R06AA02 = systemic; D04AA32 = topical.")
s("dipyridamole", "B01AC07", "dipyridamole")
s("doxepin", "N06AA12", "doxepin", ["D04AX01"], "N06AA12 = systemic; D04AX01 = topical.")
s("doxylamine", "R06AA09", "doxylamine")
s("eszopiclone", "N05CF04", "eszopiclone")
s("etizolam", "N05BA19", "etizolam")
s("ferrous sulfate", "B03AA07", "ferrous sulfate")
s("flunitrazepam", "N05CD03", "flunitrazepam")
s("flurazepam", "N05CD01", "flurazepam")
s("gabapentin", "N02BF01", "gabapentin")
s("hydroxyzine", "N05BB01", "hydroxyzine")
s("ibuprofen", "M01AE01", "ibuprofen", ["C01EB16", "G02CC01", "M02AA13", "R02AX02"],
  "M01AE01 = oral anti-inflammatory; the others are IV (ductus), vaginal, topical and throat forms.")
s("lemborexant", "N05CJ02", "lemborexant")
s("levodopa", "N04BA01", "levodopa", ["N04BA02"],
  "N04BA02 = levodopa with decarboxylase inhibitor (the usual product); the row says only 'levodopa'.")
s("levomepromazine", "N05AA02", "levomepromazine")
s("lisdexamfetamine", "N06BA12", "lisdexamfetamine")
s("lorazepam", "N05BA06", "lorazepam")
s("lormetazepam", "N05CD06", "lormetazepam")
s("melatonin|melatonin (immediate-release)|melatonin (prolonged-release)|melatonin 2 mg PR|melatonin 2 mg prolonged-release",
  "N05CH01", "melatonin")
s("melperone", "N05AD03", "melperone")
s("methylphenidate", "N06BA04", "methylphenidate")
s("mianserin", "N06AX03", "mianserin")
s("midazolam", "N05CD08", "midazolam")
s("mirtazapine", "N06AX11", "mirtazapine")
s("modafinil", "N06BA07", "modafinil")
s("montelukast", "R03DC03", "montelukast")
s("nitrazepam", "N05CD02", "nitrazepam")
s("olanzapine", "N05AH03", "olanzapine")
s("oxazepam", "N05BA04", "oxazepam")
s("oxybutynin", "G04BD04", "oxybutynin")
s("oxycodone", "N02AA05", "oxycodone")
s("acetaminophen", "N02BE01", "paracetamol", note="WHO name: paracetamol.")
s("pipamperone", "N05AD05", "pipamperone")
s("pitolisant", "N07XX11", "pitolisant")
s("pramipexole", "N04BC05", "pramipexole")
s("pregabalin", "N02BF02", "pregabalin")
s("promethazine", "R06AD02", "promethazine", ["D04AA10"], "R06AD02 = systemic; D04AA10 = topical.")
s("prothipendyl", "N05AX07", "prothipendyl")
s("quetiapine", "N05AH04", "quetiapine")
s("ramelteon", "N05CH02", "ramelteon")
s("ropinirole", "N04BC04", "ropinirole")
s("rotigotine", "N04BC09", "rotigotine")
s("sodium oxybate", "N07XX04", "sodium oxybate", ["N01AX11"], "N07XX04 = other nervous system drugs (narcolepsy); N01AX11 = anaesthetic.")
s("solriamfetol", "N06BA14", "solriamfetol")
s("sulthiame", "N03AX03", "sultiame", note="WHO name: sultiame.")
s("suvorexant", "N05CJ01", "suvorexant")
s("tasimelteon", "N05CH03", "tasimelteon")
s("temazepam", "N05CD07", "temazepam")
s("tiagabine", "N03AG06", "tiagabine")
s("tirzepatide", "A10BX16", "tirzepatide")
s("trazodone", "N06AX05", "trazodone")
s("triazolam", "N05CD05", "triazolam")
s("trimipramine", "N06AA06", "trimipramine")
s("tryptophan", "N06AX02", "tryptophan")
s("valerian", "N05CM09", "Valerianae radix")
s("valproic acid", "N03AG01", "valproic acid")
s("venlafaxine", "N06AX16", "venlafaxine")
s("zaleplon", "N05CF03", "zaleplon")
s("zolpidem", "N05CF02", "zolpidem")
s("zonisamide", "N03AX15", "zonisamide")
s("zopiclone", "N05CF01", "zopiclone")
# Classes that match exactly one ATC group
s("Z-drugs", "N05CF", "Benzodiazepine related drugs", note="ATC group, not a single substance.")
s("antipsychotics|antipsychotics (class, e.g. quetiapine)", "N05A", "ANTIPSYCHOTICS", note="ATC group, not a single substance.")
s("opioids", "N02A", "OPIOIDS", note="ATC group, not a single substance.")
s("hypnotics", "N05C", "HYPNOTICS AND SEDATIVES", note="ATC group, not a single substance.")
# No confirmed code
for names, note in {
    "benzodiazepines|long-acting benzodiazepines|shorter-acting benzodiazepines":
        "Class split across N05BA (anxiolytics) and N05CD (hypnotics); no single code.",
    "antihistamines": "Class split across R06A (systemic) and D04A (topical); no single code.",
    "sedating antidepressants": "Not an ATC group.",
    "intranasal corticosteroids": "Several substances; the row names no single drug.",
    "ferric carboxymaltose|iron sucrose|iron dextran|ferumoxytol":
        "Not listed by name in the index; parenteral iron is classed only at group level (B03AC). Left null until checked.",
    "gabapentin enacarbil": "Not listed by name in the index.",
    "calcium/magnesium/potassium/sodium oxybates (low-sodium oxybate)": "Not listed by name in the index.",
    "aceprometazine+meprobamate":
        "Combination; aceprometazine is not listed by name. N05CX01 (meprobamate, combinations) is a candidate, unconfirmed.",
    "lavender": "The index lists only lavender oil (Lavandulae aetheroleum, N05BX05); the row does not say which preparation.",
    "Chaihu Shugan San|Xiaoyao San|cannabis|chamomile|hops|kava|kava-kava|melissa|passiflora|passionflower|saffron":
        "Not listed by name in the index (herbal or traditional preparation).",
}.items():
    s(names, None, None, note=note)

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
