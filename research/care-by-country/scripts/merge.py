"""Merge subagent outputs into research/care-by-country/comparison.json.

usage: python3 -I merge.py NOTES_DIR OUT_DIR
"""
import collections
import json
import re
import sys
from pathlib import Path

notes, out = Path(sys.argv[1]), Path(sys.argv[2])
SOURCES = ["us", "uk", "europe", "canada-oceania-latam", "asia-who", "other-conditions"]
ORDER = ["guideline", "pathway", "coverage"]
FIELDS = ["id", "layer", "country", "jurisdiction", "body", "guidelineTitle", "guidelineYear",
          "status", "condition", "decision", "recommendation", "direction", "strength", "drugs",
          "citation", "freeToRead", "freeUrl", "whatWasRead", "conflictsOfInterest",
          "numbersToVerify", "notes", "researchFile"]

TA758_QUOTE = ("Solriamfetol is recommended as an option for treating excessive daytime sleepiness in "
               "adults with narcolepsy with or without cataplexy. This is only if modafinil and either "
               "dexamfetamine or methylphenidate have not worked well enough or are not suitable.")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


rows = []
for src in SOURCES:
    p = notes / f"{src}.json"
    if not p.exists():
        print("missing", p, file=sys.stderr)
        continue
    for r in json.loads(p.read_text()):
        r = dict(r)
        full = r["country"]
        # "Canada (Ontario ...)" -> country Canada, jurisdiction "Ontario ..."
        m = re.match(r"^([^()]+?)\s*\((.+)\)$", full)
        r["country"], r["jurisdiction"] = (m.group(1), m.group(2)) if m else (full, None)
        r["researchFile"] = f"{src}.md"
        # Lead re-read NICE TA758 in Chrome (2026-10-21).
        if "TA758" in json.dumps(r) and r["country"] == "UK" and "secondary" in str(r.get("whatWasRead")):
            r["whatWasRead"] = "guideline web page (read in Chrome by lead session, 2026-10-21)"
            r["notes"] = (r.get("notes") or "") + f' Verified wording: "{TA758_QUOTE}"'
        rows.append(r)

rows.sort(key=lambda r: (r["country"], r["condition"], ORDER.index(r.get("layer", "guideline")),
                         r["decision"], str(r.get("guidelineYear"))))
seen = collections.Counter()
for r in rows:
    base = "-".join(slug(x) for x in (r["country"], r["condition"], r["decision"]))
    seen[base] += 1
    r["id"] = f"{base}-{seen[base]}"

rows = [{k: r.get(k) for k in FIELDS} | {k: v for k, v in r.items() if k not in FIELDS} for r in rows]
(out / "comparison.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")

comp = json.loads((notes / "existing-comparisons.json").read_text())
(out / "existing-comparisons.json").write_text(json.dumps(comp, indent=2, ensure_ascii=False) + "\n")

pmids = sorted({str(r["citation"].get("pmid")) for r in rows if isinstance(r.get("citation"), dict) and r["citation"].get("pmid")}
               | {str(c["pmid"]) for c in comp if c.get("pmid")})
Path(sys.argv[0]).with_name("pmids.txt").write_text("\n".join(pmids) + "\n")
print(len(rows), "rows;", len(comp), "comparisons;", len(pmids), "unique PMIDs")
print(collections.Counter(r["country"] for r in rows).most_common())
print(collections.Counter(r["layer"] for r in rows))
