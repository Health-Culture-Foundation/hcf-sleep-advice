"""Join the SAM wiki extract, the health-glossary sleep entries and the
editorial layer into one dataset.

    python3 -I scripts/build.py

Reads:  sources/sam-wiki/extract.json, sources/health-glossary/sleep-entries.json,
        sources/citation-access.json, editorial/items.json, editorial/sources.json
Writes: data/sleep-advice.json, data/sleep-advice.csv, data/glossary-mapping.csv

Fails if any wiki item or glossary entry is left unmapped, or if an editorial
entry points at something that doesn't exist.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAST_CHECKED = "2026-10-21"
LICENSE = {"id": "CC-BY-4.0", "url": "https://creativecommons.org/licenses/by/4.0/", "attribution": "Health Culture Foundation"}
SCALES = ["reach", "ease", "impact", "novelty", "evidenceSupport"]
# Wiki column name -> dataset name. Commonality is renamed reach (Kalman's v1.2
# feedback); red flags are flipped so 5 is always the good end.
FROM_WIKI = {"commonality": "reach", "ease": "ease", "impact": "impact", "novelty": "novelty", "evidenceSupport": "evidenceSupport"}
CODES_NOTE = (
    "Copied from the SAM wiki, where some codes were AI-drafted. Not checked against the WHO ICD-11 "
    "browser or the ICHI classification. Codes are assigned per category (ICHI) and subcategory (ICD-11), "
    "not per item."
)


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def tags_for(item: dict) -> dict:
    page = item.get("page", {})
    page_scores = dict(page.get("scores", {}))
    if "redFlags" in page_scores:
        page_scores["evidenceSupport"] = 6 - page_scores.pop("redFlags")
    rationale = dict(page.get("rationale", {}))
    if "redFlags" in rationale:
        rationale["evidenceSupport"] = rationale.pop("redFlags")
    sets = {
        "itemPage": page_scores,
        "summaryTable": item.get("summaryTable", {}),
        "classificationTable": item.get("classificationTables", {}),
    }
    out = {}
    for wiki_key, key in FROM_WIKI.items():
        scores = {name: s[wiki_key] for name, s in sets.items() if wiki_key in s}
        value, chosen = None, None
        for name in ("itemPage", "summaryTable", "classificationTable"):
            if name in scores:
                value, chosen = scores[name], name
                break
        vals = list(scores.values())
        out[key] = {
            "value": value,
            "from": chosen,
            "wikiScores": scores,
            "spread": (max(vals) - min(vals)) if vals else None,
            "rationale": rationale.get(wiki_key),
            "status": "wiki draft, unreviewed" if value is not None else "not scored",
        }
    return out


def resolve_citations(cites: list[dict], refs: dict, access: dict) -> list[dict]:
    out = []
    for c in cites:
        ref = refs.get(str(c["ref"]), {})
        acc = access["wikiReferences"].get(str(c["ref"]), {})
        out.append(
            {
                "wikiRef": c["ref"],
                "citation": ref.get("citation"),
                "url": ref.get("url") or c["url"],
                "doi": acc.get("doi"),
                "freeToRead": acc.get("free"),
                "accessCheckedBy": acc.get("how"),
                "readUrl": acc.get("readUrl"),
            }
        )
    return out


def editorial_source(key: str, sources: dict, access: dict) -> dict:
    s = sources[key]
    acc = access["editorialSources"].get(key, {})
    return {
        "source": key,
        "citation": s["citation"],
        "url": s.get("url"),
        "doi": s.get("doi"),
        "freeToRead": acc.get("free"),
        "accessCheckedBy": acc.get("how"),
        "readUrl": acc.get("readUrl"),
        "whatWasChecked": s.get("checked"),
    }


def main() -> None:
    wiki = load("sources/sam-wiki/extract.json")
    gloss = load("sources/health-glossary/sleep-entries.json")
    access = load("sources/citation-access.json")
    ed = load("editorial/items.json")
    sources = load("editorial/sources.json")["sources"]

    cats = {c["id"]: c for c in wiki["categories"]}
    subs = {s["id"]: (c, s) for c in wiki["categories"] for s in c["subcategories"]}
    witems = {i["id"]: i for i in wiki["items"]}
    refs = wiki["references"]
    gentries = {e["glossaryId"]: e for e in gloss["entries"]}
    published = {t["glossaryId"]: t["term"] for t in gloss["publishedSleepTerms"]}
    url_tpl = gloss["source"]["siteTermUrl"]

    errors = []
    seen_ids, seen_wiki = set(), set()
    gloss_map: dict[str, list] = {g: [] for g in gentries}
    records = []

    def gref(g: dict, advice_id: str) -> dict:
        e = gentries.get(g["id"])
        if not e:
            errors.append(f"{advice_id}: unknown glossary id {g['id']}")
            return {}
        gloss_map[g["id"]].append((advice_id, g["relation"]))
        return {
            "glossaryId": g["id"],
            "term": e["term"],
            "relation": g["relation"],
            "status": "proposed term, AI-drafted, unreviewed",
            "url": url_tpl.format(id=g["id"]) if e["inCommittedBuild"] else None,
        }

    def check_sources(row: dict, aid: str) -> None:
        for d in row.get("disagreements", []):
            for p in d["positions"]:
                if p["source"] != "wiki" and p["source"] not in sources:
                    errors.append(f"{aid}: unknown source {p['source']}")
        for k in row.get("extraSources", []):
            if k not in sources:
                errors.append(f"{aid}: unknown extra source {k}")

    for row in ed["items"]:
        aid = row["id"]
        if aid in seen_ids:
            errors.append(f"duplicate id {aid}")
        seen_ids.add(aid)
        check_sources(row, aid)
        for t in row.get("audience", []):
            if t not in ed["audienceTags"]:
                errors.append(f"{aid}: unknown audience tag {t}")

        glossary = [gref(g, aid) for g in row.get("glossary", [])]
        if row.get("from") == "glossary":
            e = gentries.get(row["glossaryId"])
            if not e:
                errors.append(f"{aid}: unknown glossary id {row['glossaryId']}")
                continue
            glossary.insert(0, gref({"id": row["glossaryId"], "relation": "same"}, aid))
            cat, sub = subs[row["placeIn"]]
            rec = {
                "id": aid,
                "kind": row.get("kind", "advice"),
                "origin": "health-glossary",
                "wikiNumber": None,
                "categoryPath": [{"id": cat["id"], "name": cat["name"]}, {"id": sub["id"], "name": sub["name"]}],
                "placement": "proposed (glossary entry, not in the wiki taxonomy)",
                "sourceWording": e["term"],
                "plain": row["plain"],
                "paragraph": {"text": e["definition"], "from": "health-glossary aiDefinition", "status": f"AI draft, unreviewed (confidence {e['confidence']})"},
                "evidence": {"summary": None, "status": "no evidence summary; see glossary review note", "reviewNote": e["reviewNote"], "citations": []},
                "tags": {k: {"value": None, "status": "not scored"} for k in SCALES},
            }
        else:
            num = row["wiki"]
            w = witems.get(num)
            if not w:
                errors.append(f"{aid}: unknown wiki item {num}")
                continue
            seen_wiki.add(num)
            cat, sub = subs[w["subcategory"]]
            page = w.get("page", {})
            sci = page.get("scientificSupport")
            all_cites = []
            for k in ("scientificSupport", "background", "practicalTip"):
                for c in page.get(k, {}).get("citations", []):
                    if c["ref"] not in {x["ref"] for x in all_cites}:
                        all_cites.append(c)
            tip = page.get("practicalTipShort")
            rec = {
                "id": aid,
                "kind": "advice",
                "origin": "sam-wiki",
                "wikiNumber": num,
                "categoryPath": [{"id": cat["id"], "name": cat["name"]}, {"id": sub["id"], "name": sub["name"]}],
                "placement": "listed in the wiki's 'New Sleep Advices' (not yet placed)" if w.get("listedUnderNewSleepAdvices") else "wiki taxonomy",
                "sourceWording": page.get("title") or w["text"],
                "plain": row["plain"],
                "paragraph": {"text": tip, "from": "SAM wiki practical tip", "status": "wiki text, unedited"} if tip else {"text": None, "status": "to write"},
                "evidence": {
                    "summary": sci["text"] if sci else None,
                    "status": (
                        "wiki text with citations" if all_cites else "wiki text, no citations" if sci else "no write-up in the wiki"
                    ),
                    "citations": resolve_citations(all_cites, refs, access),
                },
                "tags": tags_for(w),
            }
        rec["evidence"]["moreSources"] = [editorial_source(k, sources, access) for k in row.get("extraSources", [])]
        rec["audience"] = row.get("audience") or ["all-ages-and-cultures"]
        rec["audienceNote"] = row.get("audienceNote")
        rec["disagreements"] = row.get("disagreements", [])
        if rec["origin"] == "sam-wiki":
            c = cats[rec["categoryPath"][0]["id"]]
            rec["codes"] = {
                "ichi": c["ichi"],
                "icd11": subs[rec["categoryPath"][1]["id"]][1]["icd11"],
                "verified": False,
                "note": CODES_NOTE,
            }
        else:
            rec["codes"] = {"ichi": [], "icd11": [], "verified": False, "note": "No codes: not in the wiki taxonomy."}
        rec["glossary"] = [g for g in glossary if g]
        rec["glossaryTerms"] = [
            {"glossaryId": t, "term": published.get(t), "url": url_tpl.format(id=t)} for t in row.get("glossaryTerms", [])
        ]
        for t in row.get("glossaryTerms", []):
            if t not in published:
                errors.append(f"{aid}: unknown published glossary term {t}")
        rec["editorNotes"] = row.get("notes")
        rec["plainStatus"] = "drafted by Claude 2026-10-21, unreviewed"
        rec["tested"] = {"withReaders": False}
        rec["changeLog"] = []
        rec["license"] = LICENSE["id"]
        rec["lastChecked"] = LAST_CHECKED
        records.append(rec)

    for m in wiki["myths"]:
        e = ed["myths"].get(m["id"])
        if not e:
            errors.append(f"myth {m['id']} has no editorial entry")
            continue
        records.append(
            {
                "id": e["id"],
                "kind": "myth",
                "origin": "sam-wiki",
                "wikiNumber": m["id"],
                "categoryPath": [{"id": "myths", "name": "Busting sleep myths"}],
                "placement": "wiki myths tab",
                "sourceWording": f"Myth: {m['myth']}",
                "plain": e["plain"],
                "paragraph": {"text": m["truth"], "from": "SAM wiki 'Truth' line", "status": "wiki text, unedited"},
                "evidence": {
                    "summary": m["text"],
                    "status": "wiki text with citations" if m["citations"] else "wiki text, no citations",
                    "citations": resolve_citations(m["citations"], refs, access),
                    "moreSources": [],
                },
                "tags": {k: {"value": None, "status": "not scored"} for k in SCALES},
                "audience": e["audience"],
                "audienceNote": None,
                "disagreements": [],
                "codes": {"ichi": [], "icd11": [], "verified": False, "note": "No codes in the wiki for myths."},
                "glossary": [],
                "glossaryTerms": [],
                "relatedAdvice": e["related"],
                "editorNotes": e.get("notes"),
                "plainStatus": "drafted by Claude 2026-10-21, unreviewed",
                "tested": {"withReaders": False},
                "changeLog": [],
                "license": LICENSE["id"],
                "lastChecked": LAST_CHECKED,
            }
        )

    missing = sorted(set(witems) - seen_wiki)
    if missing:
        errors.append(f"wiki items with no editorial entry: {missing}")
    unmapped = sorted(g for g, v in gloss_map.items() if not v)
    if unmapped:
        errors.append(f"glossary entries not mapped: {unmapped}")
    if errors:
        raise SystemExit("\n".join(errors))

    out = {
        "name": "HCF Sleep Advice",
        "version": "0.1.0-draft",
        "description": "Sleep advice from the Health Culture Foundation's SAM wiki and the health-glossary sleep drafts, joined into one list with plain wording, evidence, tags, audiences and where sources disagree. Draft: nothing here has been reviewed.",
        "license": LICENSE,
        "lastChecked": LAST_CHECKED,
        "schema": "SCHEMA.md",
        "scales": {
            "reach": "How widely known the advice is (was 'commonality'). 1 rare, 5 universal. Low reach is not bad: niche advice that should be better known is the point of tracking it.",
            "ease": "How easy it is to do (was 'practicality' / 'ease of implementation'). 1 impractical, 5 effortless.",
            "impact": "How big the effect is thought to be. 1 minimal, 5 game-changer.",
            "novelty": "How surprising it is. 1 obvious, 5 feels like a secret.",
            "evidenceSupport": "How well research supports it (the wiki's 'scientific red flags', flipped). 1 red flag, 5 strongly supported.",
        },
        "audienceTags": ed["audienceTags"],
        "sources": {
            "samWiki": wiki["source"],
            "healthGlossary": gloss["source"],
            "taggingTaxonomy": {"title": "Sleep Advice Coding Ideas (Advice Tagging Taxonomy v1.2)", "url": "https://docs.google.com/document/d/19gFTE4sa5e1rvHIZkovttb1w4qix2TBQ6BbWm3PeoR4"},
        },
        "categories": [
            {"id": c["id"], "name": c["name"], "ichi": c["ichi"], "subcategories": [{"id": s["id"], "name": s["name"], "icd11": s["icd11"]} for s in c["subcategories"]]}
            for c in wiki["categories"]
        ],
        "items": records,
    }
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    (data / "sleep-advice.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cols = [
        "id", "kind", "origin", "wikiNumber", "category", "subcategory", "placement", "plain", "sourceWording",
        "paragraph", "evidenceStatus", "citationCount", "freeCitationCount",
        *[f"{s}" for s in SCALES], *[f"{s}Spread" for s in SCALES],
        "audience", "audienceNote", "disagreementCount", "disagreements", "glossaryIds", "ichi", "icd11", "codesVerified",
        "editorNotes", "license", "lastChecked",
    ]
    with (data / "sleep-advice.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in records:
            cites = r["evidence"]["citations"] + r["evidence"]["moreSources"]
            w.writerow(
                {
                    "id": r["id"],
                    "kind": r["kind"],
                    "origin": r["origin"],
                    "wikiNumber": r["wikiNumber"] or "",
                    "category": r["categoryPath"][0]["name"],
                    "subcategory": r["categoryPath"][1]["name"] if len(r["categoryPath"]) > 1 else "",
                    "placement": r["placement"],
                    "plain": r["plain"],
                    "sourceWording": r["sourceWording"],
                    "paragraph": r["paragraph"].get("text") or "",
                    "evidenceStatus": r["evidence"]["status"],
                    "citationCount": len(cites),
                    "freeCitationCount": sum(1 for c in cites if c.get("freeToRead")),
                    **{s: r["tags"][s]["value"] if r["tags"][s]["value"] is not None else "" for s in SCALES},
                    **{f"{s}Spread": r["tags"][s].get("spread") if r["tags"][s].get("spread") is not None else "" for s in SCALES},
                    "audience": "; ".join(r["audience"]),
                    "audienceNote": r["audienceNote"] or "",
                    "disagreementCount": len(r["disagreements"]),
                    "disagreements": " | ".join(d["about"] for d in r["disagreements"]),
                    "glossaryIds": "; ".join(f"{g['glossaryId']} ({g['relation']})" for g in r["glossary"]),
                    "ichi": "; ".join(c["code"] for c in r["codes"]["ichi"]),
                    "icd11": "; ".join(c["code"] for c in r["codes"]["icd11"]),
                    "codesVerified": "no",
                    "editorNotes": r["editorNotes"] or "",
                    "license": r["license"],
                    "lastChecked": r["lastChecked"],
                }
            )

    with (data / "glossary-mapping.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["glossaryId", "term", "glossaryFile", "inCommittedBuild", "adviceId", "relation"])
        for gid, links in gloss_map.items():
            e = gentries[gid]
            for aid, rel in links:
                w.writerow([gid, e["term"], e["file"], e["inCommittedBuild"], aid, rel])

    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"{len(records)} records {kinds} -> data/sleep-advice.json, .csv, glossary-mapping.csv")


if __name__ == "__main__":
    main()
