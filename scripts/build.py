"""Join the SAM wiki extract, the health-glossary sleep entries and the
editorial layer into one dataset.

    python3 -I scripts/build.py

Reads:  sources/sam-wiki/extract.json, sources/health-glossary/sleep-entries.json,
        sources/citation-access.json, sources/code-check.json,
        editorial/items.json, editorial/sources.json, editorial/relations.json,
        editorial/scores.json
Writes: data/sleep-advice.json, data/sleep-advice.csv, data/glossary-mapping.csv,
        data/sleep-advice.skos.ttl, TAXONOMY.md

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
    "Copied from the SAM wiki. Each code was looked up in the WHO browsers on 2026-10-21 (see "
    "sources/code-check.json): all exist, two ICD-11 titles in the wiki are outdated. Whether each code "
    "fits the advice has not been reviewed. Codes are assigned per category (ICHI) and subcategory "
    "(ICD-11), not per item."
)
CONCEPT_BASE = "https://health-culture.org/sleep-advice/"


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

    records = apply_concepts(records, load("editorial/relations.json"), subs, errors)
    apply_scores(records, load("editorial/scores.json"), errors)
    code_check = load("sources/code-check.json")
    apply_code_check(records, code_check)
    facets = load("editorial/facets.json")
    apply_facets(records, facets, code_check, errors)

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
        "conceptBase": CONCEPT_BASE,
        "facets": facets["facets"],
        "categories": [
            {
                "id": c["id"],
                "name": c["name"],
                "ichi": [checked_code(x, code_check["ichi"]) for x in c["ichi"]],
                "subcategories": [
                    {"id": s["id"], "name": s["name"], "icd11": [checked_code(x, code_check["icd11"]) for x in s["icd11"]]}
                    for s in c["subcategories"]
                ],
            }
            for c in wiki["categories"]
        ],
        "items": records,
    }
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    (data / "sleep-advice.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cols = [
        "id", "status", "mergedInto", "kind", "origin", "wikiNumber", "category", "subcategory", "placement", "plain",
        "altLabels", "broader", "narrower", "related", "conflictsWith", "mechanism", "timeOfDay", "condition",
        "conditionIcd11", "sourceWording",
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
                    "status": r["status"],
                    "mergedInto": r.get("mergedInto") or "",
                    "altLabels": "; ".join(r["altLabels"]),
                    "broader": "; ".join(r["broader"]),
                    "narrower": "; ".join(r["narrower"]),
                    "related": "; ".join(r["related"]),
                    "conflictsWith": "; ".join(c["id"] for c in r["conflictsWith"]),
                    "mechanism": "; ".join(r.get("facets", {}).get("mechanism", [])),
                    "timeOfDay": "; ".join(r.get("facets", {}).get("timeOfDay", [])),
                    "condition": "; ".join(r.get("facets", {}).get("condition", [])),
                    "conditionIcd11": "; ".join(c["code"] for c in r.get("conditionCodes", [])),
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
                    "codesVerified": r["codes"]["verified"],
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

    write_skos(out)
    write_taxonomy_md(out)

    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"{len(records)} records {kinds} -> data/sleep-advice.json, .csv, .skos.ttl, glossary-mapping.csv, TAXONOMY.md")


def checked_code(code: dict, check: dict) -> dict:
    c = check["codes"].get(code["code"], {})
    return {
        "code": code["code"],
        "title": c.get("currentTitle") or code["title"],
        "wikiTitle": code["title"],
        "exists": c.get("exists"),
        "titleOutdatedInWiki": c.get("titleOutdated", False),
    }


def apply_code_check(records: list[dict], check: dict) -> None:
    for r in records:
        codes = r["codes"]
        if not (codes["ichi"] or codes["icd11"]):
            continue
        codes["ichi"] = [checked_code(x, check["ichi"]) for x in codes["ichi"]]
        codes["icd11"] = [checked_code(x, check["icd11"]) for x in codes["icd11"]]
        codes["verified"] = "code exists; fit not reviewed"
        codes["checkedOn"] = check["checked"]


def apply_concepts(records: list[dict], rel: dict, subs: dict, errors: list) -> list[dict]:
    """Turn items into SKOS-style concepts: labels, hierarchy, merges, conflicts."""
    for g in rel["groups"]:
        cat, sub = subs[g["placeIn"]]
        records.append(
            {
                "id": g["id"],
                "kind": "group",
                "origin": "editorial",
                "wikiNumber": None,
                "categoryPath": [{"id": cat["id"], "name": cat["name"]}, {"id": sub["id"], "name": sub["name"]}],
                "placement": "proposed grouping concept",
                "sourceWording": g["plain"],
                "plain": g["plain"],
                "paragraph": {"text": None, "status": "to write"},
                "evidence": {"summary": None, "status": "see narrower items", "citations": [], "moreSources": []},
                "tags": {k: {"value": None, "status": "not scored"} for k in SCALES},
                "audience": ["all-ages-and-cultures"],
                "audienceNote": None,
                "disagreements": [],
                "codes": {"ichi": [], "icd11": [], "verified": False, "note": "Grouping concept; no codes."},
                "glossary": [],
                "glossaryTerms": [],
                "editorNotes": g.get("notes"),
                "plainStatus": "drafted by Claude 2026-10-21, unreviewed",
                "tested": {"withReaders": False},
                "changeLog": [],
                "license": LICENSE["id"],
                "lastChecked": LAST_CHECKED,
                "_alt": g.get("altLabels", []),
                "_broader": g.get("broader", []),
            }
        )
    by_id = {r["id"]: r for r in records}

    def known(i: str, where: str) -> bool:
        if i not in by_id:
            errors.append(f"relations.json {where}: unknown id {i}")
            return False
        return True

    for r in records:
        alt = list(r.pop("_alt", []))
        # Wiki titles read "advice – reason"; only the advice part is a label.
        wording = (r["sourceWording"] or "").split(" – ")[0].strip()
        if r["kind"] == "myth":
            wording = ""
        if wording and wording.lower().rstrip(".") != r["plain"].lower().rstrip("."):
            alt.append(wording)
        alt += [g["term"] for g in r["glossary"] if g["relation"] == "same"]
        alt += rel["altLabels"].get(r["id"], [])
        r["altLabels"] = alt
        r["broader"] = list(r.pop("_broader", [])) + rel["broader"].get(r["id"], [])
        r["narrower"], r["related"], r["conflictsWith"] = [], [], []
        r["status"] = "active"
        r["mergedInto"] = None
    for i in rel["altLabels"]:
        known(i, "altLabels")
    for child, parents in rel["broader"].items():
        known(child, "broader")
        for p in parents:
            known(p, "broader")
    for r in records:
        for p in r["broader"]:
            if p in by_id:
                by_id[p]["narrower"].append(r["id"])
    for a, b in rel["related"]:
        if known(a, "related") and known(b, "related"):
            by_id[a]["related"].append(b)
            by_id[b]["related"].append(a)
    for c in rel["conflictsWith"]:
        a, b = c["between"]
        if known(a, "conflictsWith") and known(b, "conflictsWith"):
            by_id[a]["conflictsWith"].append({"id": b, "why": c["why"]})
            by_id[b]["conflictsWith"].append({"id": a, "why": c["why"]})

    for old, m in rel["merges"].items():
        if not (known(old, "merges") and known(m["into"], "merges")):
            continue
        src, dst = by_id[old], by_id[m["into"]]
        src["status"] = "merged"
        src["mergedInto"] = dst["id"]
        src["editorNotes"] = f"Merged into {dst['id']}: {m['why']}" + (f" Earlier note: {src['editorNotes']}" if src["editorNotes"] else "")
        dst["altLabels"] += [src["plain"]] + src["altLabels"]
        for g in src["glossary"]:
            if g["glossaryId"] not in {x["glossaryId"] for x in dst["glossary"]}:
                dst["glossary"].append(g)
        for d in src["disagreements"]:
            dst["disagreements"].append({**d, "about": f"{d['about']} (from merged item {old})"})
        dst["related"] += [x for x in src["related"] if x != dst["id"]]
        dst.setdefault("mergedFrom", []).append(old)
        for key in ("broader", "narrower", "related", "conflictsWith"):
            src[key] = []

    # Cycle check on broader.
    def walk(i: str, seen: tuple) -> None:
        if i in seen:
            errors.append(f"broader cycle: {' -> '.join(seen + (i,))}")
            return
        for p in by_id.get(i, {}).get("broader", []):
            walk(p, seen + (i,))

    for r in records:
        walk(r["id"], ())
        seen, uniq = set(), []
        for a in r["altLabels"]:
            if a.lower() not in seen and a.lower() != r["plain"].lower():
                seen.add(a.lower())
                uniq.append(a)
        r["altLabels"] = uniq
        r["related"] = sorted(set(r["related"]))
    return records


def apply_facets(records: list[dict], facets: dict, code_check: dict, errors: list) -> None:
    """Mechanism, time of day and condition. Condition values carry checked ICD-11 codes,
    which are per item, unlike the wiki's per-subcategory codes."""
    vocab = facets["facets"]
    icd = code_check["icd11"]["codes"]
    for v in vocab["condition"]["values"].values():
        for c in v["icd11"]:
            if c not in icd:
                errors.append(f"facets.json: condition code {c} not in sources/code-check.json")
    by_id = {r["id"]: r for r in records}
    for i in facets["items"]:
        if i not in by_id:
            errors.append(f"facets.json: unknown id {i}")
    names = ["mechanism", "timeOfDay", "condition"]
    for r in records:
        if r["status"] == "merged":
            continue
        row = facets["items"].get(r["id"])
        if not row:
            errors.append(f"facets.json: no facets for {r['id']}")
            continue
        r["facets"] = {}
        for name, raw in zip(names, row):
            vals = [v for v in raw.split("|") if v]
            for v in vals:
                if v not in vocab[name]["values"]:
                    errors.append(f"facets.json: {r['id']}: unknown {name} value {v}")
            r["facets"][name] = vals
        r["facets"]["status"] = "drafted by Claude 2026-10-21, unreviewed"
        codes = []
        for cond in r["facets"]["condition"]:
            for c in vocab["condition"]["values"].get(cond, {}).get("icd11", []):
                if c in icd and c not in {x["code"] for x in codes}:
                    codes.append({"code": c, "title": icd[c]["currentTitle"], "via": cond})
        r["conditionCodes"] = codes


def apply_scores(records: list[dict], scores: dict, errors: list) -> None:
    by_id = {r["id"]: r for r in records}
    cap = scores["rules"]["evidenceCapWithoutCitation"]
    for i in scores["proposals"]:
        if i not in by_id:
            errors.append(f"scores.json: unknown id {i}")
    for r in records:
        if r["kind"] in ("myth",) or r["status"] == "merged":
            continue
        props = scores["proposals"].get(r["id"], {})
        cited = bool(r["evidence"]["citations"] or r["evidence"]["moreSources"])
        for scale in SCALES:
            t = r["tags"][scale]
            t.setdefault("wikiScores", {})
            t.setdefault("spread", None)
            t.setdefault("rationale", None)
            wiki_value, wiki_from = t["value"], t.get("from")
            t["wikiValue"] = wiki_value
            proposal = None
            if scale in props:
                v, why = props[scale]
                proposal = {"value": v, "reason": why or None}
            elif scale == "evidenceSupport" and wiki_value is not None and wiki_value > cap and not cited:
                proposal = {"value": cap, "reason": f"Capped at {cap}: the wiki rates it {wiki_value} but the dataset holds no citation for it."}
            if proposal:
                proposal["by"] = "Claude, 2026-10-21"
                t["proposal"] = proposal
                t["value"] = proposal["value"]
                t["from"] = "proposal"
                t["status"] = "proposed by Claude, unreviewed"
            else:
                t["from"] = f"wiki {wiki_from}" if wiki_from else None
                t["status"] = "wiki draft, unreviewed" if wiki_value is not None else "not scored"
            t["reviewed"] = False


def turtle_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"@en'


def write_skos(out: dict) -> None:
    """SKOS concept scheme: categories are top concepts, items hang under subcategories."""
    b = out["conceptBase"]
    L = [
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dct: <http://purl.org/dc/terms/> .",
        "@prefix hsa: <" + b + "vocab#> .",
        "",
        "# Generated by scripts/build.py. Draft; concept IRIs are placeholders until a public home is chosen.",
        "",
        f"<{b}> a skos:ConceptScheme ;",
        f"  dct:title {turtle_str(out['name'])} ;",
        f"  dct:license <{out['license']['url']}> ;",
        "  skos:hasTopConcept " + ", ".join(f"<{b}category/{c['id']}>" for c in out["categories"]) + " .",
        "",
    ]
    for c in out["categories"]:
        L += [f"<{b}category/{c['id']}> a skos:Concept ; skos:inScheme <{b}> ; skos:topConceptOf <{b}> ;",
              f"  skos:prefLabel {turtle_str(c['name'])} ;", f"  skos:notation \"{c['id']}\" ."]
        for s in c["subcategories"]:
            L += [f"<{b}category/{s['id']}> a skos:Concept ; skos:inScheme <{b}> ;",
                  f"  skos:prefLabel {turtle_str(s['name'])} ; skos:notation \"{s['id']}\" ;",
                  f"  skos:broader <{b}category/{c['id']}> ."]
        L.append("")
    for fname, f in out["facets"].items():
        L += [f"<{b}facet/{fname}> a skos:ConceptScheme ; dct:title {turtle_str(f['label'])} ."]
        for vid, v in f["values"].items():
            t = [f"<{b}facet/{fname}/{vid}> a skos:Concept", f"skos:inScheme <{b}facet/{fname}>",
                 f"skos:topConceptOf <{b}facet/{fname}>", f"skos:prefLabel {turtle_str(v['label'])}"]
            if v.get("definition"):
                t.append(f"skos:definition {turtle_str(v['definition'])}")
            t += [f"skos:closeMatch <http://id.who.int/icd/release/11/mms/{c}>" for c in v.get("icd11", [])]
            L.append(" ;\n  ".join(t) + " .")
        L.append("")
    url_of = lambda i: f"<{b}{i}>"
    for r in out["items"]:
        if r["kind"] == "myth":
            parent = None
        else:
            parent = f"<{b}category/{r['categoryPath'][-1]['id']}>"
        p = [f"{url_of(r['id'])} a skos:Concept", f"skos:inScheme <{b}>", f"skos:prefLabel {turtle_str(r['plain'])}", f"hsa:kind \"{r['kind']}\""]
        if r.get("wikiNumber"):
            p.append(f"skos:notation \"{r['wikiNumber']}\"")
        p += [f"skos:altLabel {turtle_str(a)}" for a in r["altLabels"]]
        if r["status"] == "merged":
            p += ["hsa:deprecated true", f"dct:isReplacedBy {url_of(r['mergedInto'])}"]
        else:
            broader = [url_of(x) for x in r["broader"]] or ([parent] if parent else [])
            p += [f"skos:broader {x}" for x in broader]
            p += [f"skos:related {url_of(x)}" for x in r["related"]]
            p += [f"hsa:conflictsWith {url_of(x['id'])}" for x in r["conflictsWith"]]
            p += [f"skos:closeMatch <{g['url']}>" for g in r["glossary"] if g.get("url")]
            p += [f"skos:closeMatch <{g['url']}>" for g in r["glossaryTerms"]]
            for fname, vals in r.get("facets", {}).items():
                if fname != "status":
                    p += [f"hsa:{fname} <{b}facet/{fname}/{v}>" for v in vals]
        if r["paragraph"].get("text"):
            p.append(f"skos:definition {turtle_str(r['paragraph']['text'])}")
        if r.get("editorNotes"):
            p.append(f"skos:editorialNote {turtle_str(r['editorNotes'])}")
        L.append(" ;\n  ".join(p) + " .")
        L.append("")
    (ROOT / "data" / "sleep-advice.skos.ttl").write_text("\n".join(L), encoding="utf-8")


def write_taxonomy_md(out: dict) -> None:
    """A readable tree of the taxonomy, generated so it can't drift from the data."""
    items = [r for r in out["items"] if r["status"] == "active"]
    by_id = {r["id"]: r for r in items}

    def score(r: dict) -> str:
        vals = []
        for s, label in (("reach", "R"), ("ease", "Ea"), ("impact", "I"), ("novelty", "N"), ("evidenceSupport", "Ev")):
            t = r["tags"][s]
            v = t["value"]
            mark = "*" if t.get("from") == "proposal" else ""
            vals.append(f"{label}{v if v is not None else '–'}{mark}")
        return " ".join(vals)

    def flags(r: dict) -> str:
        f = []
        n = len(r["evidence"]["citations"]) + len(r["evidence"]["moreSources"])
        f.append(f"{n} cited" if n else "no citations")
        if r["disagreements"]:
            f.append(f"⚖️ {len(r['disagreements'])} source disagreement{'s' if len(r['disagreements']) > 1 else ''}")
        for c in r["conflictsWith"]:
            f.append(f"❗ conflicts with `{c['id']}`")
        aud = [a for a in r["audience"] if a != "all-ages-and-cultures"]
        if aud:
            f.append("for: " + ", ".join(aud))
        return " · ".join(f)

    def line(r: dict, depth: int, sub_id: str) -> list[str]:
        pad = "  " * depth
        if r["kind"] == "group":
            num = "▸ "
        elif r["origin"] == "sam-wiki":
            num = f"{r['wikiNumber']} "
        else:
            num = "＋ "
        lines = [f"{pad}- **{num}{r['plain']}**  "]
        if r["altLabels"]:
            lines.append(f"{pad}  <sub>also: {' · '.join(r['altLabels'])}</sub>  ")
        meta = f"`{r['id']}`" if r["kind"] == "group" else f"`{r['id']}` · {score(r)} · {flags(r)}"
        fx = r.get("facets", {})
        if fx:
            lab = lambda f, v: out["facets"][f]["values"][v]["label"]
            meta += " · 🕒 " + ", ".join(lab("timeOfDay", v) for v in fx["timeOfDay"])
            meta += " · ⚙️ " + ", ".join(lab("mechanism", v) for v in fx["mechanism"])
            conds = [v for v in fx["condition"] if v != "general"]
            if conds:
                meta += " · 🩺 " + ", ".join(lab("condition", v) for v in conds)
        elsewhere = [p for p in r["broader"] if p in by_id and by_id[p]["categoryPath"][1]["id"] != sub_id]
        if elsewhere:
            meta += " · ↑ part of " + ", ".join(f"`{p}` ({by_id[p]['categoryPath'][1]['id']})" for p in elsewhere)
        lines.append(f"{pad}  <sub>{meta}</sub>")
        return lines

    def tree(root_ids: list[str], depth: int, out_lines: list[str], sub_id: str) -> None:
        # Children are nested only within their own subcategory; a child placed in
        # another subcategory is listed there, with a pointer back up.
        for i in root_ids:
            r = by_id[i]
            out_lines += line(r, depth, sub_id)
            kids = [k for k in r["narrower"] if k in by_id and by_id[k]["categoryPath"][1]["id"] == sub_id]
            tree(sorted(kids, key=order), depth + 1, out_lines, sub_id)

    def order(i: str):
        r = by_id[i]
        rank = {"group": 0, "advice": 1, "concept": 2}.get(r["kind"], 3)
        return (r["origin"] != "sam-wiki", [int(x) for x in (r["wikiNumber"] or "9.9.9").split(".")], rank, i)

    by_sub: dict[str, list] = {}
    for r in items:
        if r["kind"] == "myth":
            continue
        sub_id = r["categoryPath"][1]["id"]
        if not any(p in by_id and by_id[p]["categoryPath"][1]["id"] == sub_id for p in r["broader"]):
            by_sub.setdefault(sub_id, []).append(r["id"])
    proposals = sum(1 for r in items for t in r["tags"].values() if t.get("from") == "proposal")
    merged = [r for r in out["items"] if r["status"] == "merged"]
    md = [
        "# Sleep advice taxonomy",
        "",
        "<!-- Generated by scripts/build.py from data/sleep-advice.json. Do not edit by hand. -->",
        "",
        f"Version {out['version']}, last checked {out['lastChecked']}. Nothing here is reviewed yet.",
        f"{sum(1 for r in items if r['kind'] in ('advice', 'concept'))} advice items and "
        f"{sum(1 for r in items if r['kind'] == 'group')} grouping concept(s) in {len(out['categories'])} categories, plus "
        f"{sum(1 for r in items if r['kind'] == 'myth')} myths; {len(merged)} items merged into others. "
        "Full fields: [SCHEMA.md](SCHEMA.md); spreadsheet: [data/sleep-advice.csv](data/sleep-advice.csv); "
        "SKOS: [data/sleep-advice.skos.ttl](data/sleep-advice.skos.ttl).",
        "",
        "**How to read it.** Bold = preferred label (plain one-liner, unreviewed). Number = SAM wiki item; "
        "＋ = from the health-glossary sleep entries; ▸ = grouping concept. Indented items are narrower "
        "versions of the item above them. \"also\" = alternative labels (synonyms, source wording, other names). "
        "Tags 1–5: **R** reach, **Ea** ease, **I** impact, **N** novelty, **Ev** evidence support; "
        f"– = not scored; * = Claude's proposal ({proposals} values), otherwise the wiki's score. All scores need review.",
        "",
    ]
    for c in out["categories"]:
        ichi = ", ".join(f"{x['code']} {x['title']}" for x in c["ichi"])
        md += [f"## {c['id']}. {c['name']}", "", f"<sub>ICHI: {ichi} (codes exist; fit not reviewed)</sub>", ""]
        for s in c["subcategories"]:
            icd = ", ".join(f"{x['code']} {x['title']}" for x in s["icd11"])
            md += [f"### {s['id']} {s['name']}", "", f"<sub>ICD-11: {icd} (codes exist; fit not reviewed)</sub>", ""]
            tree(sorted(by_sub.get(s["id"], []), key=order), 0, md, s["id"])
            md.append("")
    md += ["## Myths", ""]
    for r in items:
        if r["kind"] == "myth":
            md += [f"- **{r['plain']}**  ", f"  <sub>`{r['id']}` · “{r['sourceWording']}” · {flags(r)}</sub>"]
    md += ["", "## Browse by facet", "",
           "Drafted by Claude, unreviewed. Mechanism is how the sources say the advice works, not proof that it does.", ""]
    for fname, f in out["facets"].items():
        md += [f"### {f['label']}", ""]
        for vid, v in f["values"].items():
            hits = [r["id"] for r in items if vid in r.get("facets", {}).get(fname, [])]
            codes = f" (ICD-11 {', '.join(v['icd11'])})" if v.get("icd11") else ""
            md.append(f"- **{v['label']}**{codes}: {len(hits)} · " + " ".join(f"`{h}`" for h in hits))
        md.append("")
    md += ["## Merged", ""]
    for r in merged:
        md.append(f"- `{r['id']}` → `{r['mergedInto']}` (“{r['sourceWording']}”)")
    md.append("")
    (ROOT / "TAXONOMY.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
