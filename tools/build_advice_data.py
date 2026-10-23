"""Build advice/data.json, the trimmed public copy of the sleep advice dataset.

Usage: python3 -I tools/build_advice_data.py path/to/data/sleep-advice.json advice/data.json
Source: data/sleep-advice.json on branch lit-search-2026-10 (PR #2).
Left out on purpose: ICD-11/ICHI codes (licence check pending), editor notes,
links to the private health-glossary, Do One Thing commitments.
"""
import json, sys

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))

def cite(c):
    c = c or {}
    return {k: c.get(k) for k in ("authors", "year", "title", "journal", "doi", "pmid") if c.get(k)}

items = []
for i in d["items"]:
    if i["status"] != "active" or i["kind"] == "group":
        continue
    cp = i.get("categoryPath") or []
    ev = i.get("evidence") or {}
    tags = {k: (v or {}).get("value") for k, v in (i.get("tags") or {}).items()}
    items.append({
        "id": i["id"],
        "kind": i["kind"],
        "plain": i.get("plain"),
        "plainBefore": i.get("plainBefore"),
        "paragraph": (i.get("paragraph") or {}).get("text"),
        "category": cp[0]["name"] if cp else None,
        "subcategory": cp[1]["name"] if len(cp) > 1 else None,
        "origin": i.get("origin"),
        "audience": i.get("audience") or [],
        "audienceNote": i.get("audienceNote"),
        "tags": tags,
        "facets": {k: (i.get("facets") or {}).get(k) or [] for k in ("mechanism", "timeOfDay", "condition")},
        "disagreements": i.get("disagreements") or [],
        "conflictsWith": [c.get("id") for c in i.get("conflictsWith") or []],
        "evidenceSummary": ev.get("summary"),
        "sources": [{"citation": c.get("citation"), "url": c.get("readUrl") or c.get("url"), "doi": c.get("doi"),
                     "freeToRead": c.get("freeToRead")} for c in (ev.get("citations") or []) + (ev.get("moreSources") or [])],
        "findings": [{"studyType": f.get("studyType"), "population": f.get("population"), "direction": f.get("direction"),
                      "keyResult": f.get("keyResult"), "whatWasRead": f.get("whatWasRead"), "citation": cite(f.get("citation")),
                      "freeUrl": f.get("freeUrl")} for f in ev.get("literature") or []],
    })

json.dump({"version": d.get("version"), "lastChecked": d.get("lastChecked"), "license": "CC BY 4.0, Health Culture Foundation",
           "scales": d.get("scales"), "audienceTags": d.get("audienceTags"), "items": items},
          open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print(len(items), "items,", sum(len(x["findings"]) for x in items), "findings,",
      sum(1 for x in items if x["disagreements"]), "with disagreements,", sum(1 for x in items if x["plainBefore"]), "rewritten")
