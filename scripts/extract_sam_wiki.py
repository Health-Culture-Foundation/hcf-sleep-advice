"""Extract the sleep advice taxonomy from a text export of the SAM wiki.

Input: a Markdown/text export of the Google Doc "SAM Wiki: Navigating Sleep
Advice" (doc id 1B2E0eQHCcXnMW_1Qkj0X3uAy9KSmX2AXZ8mEtj7bpzE). The export is
not committed: the doc also holds survey drafts and third-party survey results
that are not ours to republish. Only the taxonomy parts are extracted.

    python3 -I scripts/extract_sam_wiki.py path/to/wiki.md

Writes sources/sam-wiki/extract.json. Re-run when the wiki changes, then
run scripts/build.py.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sources" / "sam-wiki" / "extract.json"

ITEM_RE = re.compile(r"^\s*-\s+(\d\.\d\.\d)\.?\s+(.*\S)\s*$")
SUB_RE = re.compile(r"^#### (\d\.\d)\. (.+)$")
CAT_RE = re.compile(r"^### (\d)\\?\. (.+)$")
ICD_RE = re.compile(r"\b([0-9A-Z]{2}[0-9A-Z]{2}(?:\.[0-9A-Z]+)?)\b:?\s*(.+)")
LINK_RE = re.compile(r"\[(\d+)\]\((\S+?)\)")
SCALE_WORDS = {
    "SCIENTIFIC SUPPORT": "redFlags",
    "COMMONALITY": "commonality",
    "EASE OF IMPLEMENTATION": "ease",
    "IMPACT": "impact",
    "NOVELTY": "novelty",
}


def clean(s: str) -> str:
    s = s.replace("\\*", "*").replace("\\[", "[").replace("\\]", "]")
    s = re.sub(r"\*+", "", s)
    s = s.replace("→", "").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def norm(s: str) -> str:
    s = re.sub(r"\([^)]*\)", "", clean(s).lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def cites(text: str) -> list[dict]:
    seen, out = set(), []
    for n, url in LINK_RE.findall(text):
        if n not in seen:
            seen.add(n)
            out.append({"ref": int(n), "url": url})
    return out


def strip_links(text: str) -> str:
    return clean(LINK_RE.sub(lambda m: f"[{m.group(1)}]", text))


def section(lines: list[str], start: int, end: int) -> list[str]:
    return lines[start:end]


def find(lines: list[str], pattern: str, start: int = 0) -> int:
    rx = re.compile(pattern)
    for i in range(start, len(lines)):
        if rx.search(lines[i]):
            return i
    raise SystemExit(f"not found: {pattern}")


def parse_taxonomy(lines: list[str]) -> tuple[list, dict]:
    start = find(lines, r"^## \*\*ICHI & ICD-11 Aligned Taxonomy of Sleep Advice\*\*$")
    end = find(lines, r"TABLES/SUMMARY", start)
    cats, items = [], {}
    cat = sub = None
    mode = None
    for raw in lines[start:end]:
        line = raw.rstrip()
        if m := CAT_RE.match(line):
            cat = {"id": m.group(1), "name": clean(m.group(2)), "ichi": [], "subcategories": []}
            cats.append(cat)
            mode = None
            continue
        if m := SUB_RE.match(line):
            sub = {"id": m.group(1), "name": clean(m.group(2)), "icd11": [], "items": []}
            cat["subcategories"].append(sub)
            mode = None
            continue
        if "ICHI Code:" in line:
            body = clean(line.split("ICHI Code:", 1)[1])
            codes = re.findall(r"\b(AT[A-Z]\.[A-Z]{2}\.[A-Z]{2})\b \(([^)]+)\)", body)
            cat["ichi"] = [{"code": c, "title": t} for c, t in codes]
            cat["ichiNote"] = body
            continue
        if "Relevant ICD-11" in line:
            mode = "icd"
            continue
        if mode == "icd":
            text = clean(line.lstrip(" -"))
            if text and (m := ICD_RE.match(text)):
                sub["icd11"].append({"code": m.group(1), "title": m.group(2).strip(" :")})
            continue
        if m := ITEM_RE.match(line):
            iid, text = m.group(1), clean(m.group(2))
            sub["items"].append(iid)
            items[iid] = {"id": iid, "text": text, "category": cat["id"], "subcategory": sub["id"]}
    return cats, items


def parse_summary_tables(lines: list[str], items: dict) -> None:
    """The 'TABLES/SUMMARY' block: 5=best on every column, incl. scientific support."""
    start = find(lines, r"TABLES/SUMMARY")
    end = find(lines, r"PUBLIC HEALTH PERSPECTIVES", start)
    by_text = {norm(v["text"]): k for k, v in items.items()}
    for raw in lines[start:end]:
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) != 6 or not cells[1].isdigit():
            continue
        key = norm(cells[0])
        iid = by_text.get(key) or next(
            (k for t, k in by_text.items() if key[:28] and (t.startswith(key[:28]) or key.startswith(t[:28]))),
            None,
        )
        if not iid:
            print(f"summary row not matched: {cells[0]}", file=sys.stderr)
            continue
        c, e, i, n, s = (int(x) for x in cells[1:])
        items[iid]["summaryTable"] = {"commonality": c, "ease": e, "impact": i, "novelty": n, "evidenceSupport": s}


def parse_classification_tables(lines: list[str], items: dict) -> None:
    """The 'SLEEP ADVICE CODING' block: each scale's table puts item ids in rating columns."""
    start = find(lines, r"^# \*\*SLEEP ADVICE CODING\*\*")
    end = find(lines, r"^# \*\*SCATTERPLOT\*\*", start)
    scale = None
    names = {
        "Commonality Classification": "commonality",
        "Ease of Implementation Classification": "ease",
        "Impact Classification": "impact",
        "Novelty Classification": "novelty",
        "Scientific Support Classification": "evidenceSupport",
    }
    for raw in lines[start:end]:
        for label, key in names.items():
            if label in raw:
                scale = key
        if not scale or not raw.startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) != 5:
            continue
        for rating, cell in enumerate(cells, start=1):
            if m := re.match(r"(\d\.\d\.\d)\.", cell):
                items[m.group(1)].setdefault("classificationTables", {})[scale] = rating


def parse_item_pages(lines: list[str], items: dict) -> None:
    start = find(lines, r"^# .*1\. SLEEP HYGIENE")
    end = find(lines, r"^# New Sleep Advices", start)
    heads = [
        (i, m.group(1), m.group(2))
        for i in range(start, end)
        if (m := re.match(r"^### \*\*\*(\d\.\d\.\d)\.? (.+?)\*\*\*\s*$", lines[i]))
    ]
    for n, (i, iid, title) in enumerate(heads):
        stop = heads[n + 1][0] if n + 1 < len(heads) else end
        block = lines[i + 1 : stop]
        page = {"title": clean(title), "scores": {}, "rationale": {}}
        # OVERVIEW table
        pending = None
        for raw in block:
            if raw.startswith("#### SCIENTIFIC SUPPORT"):
                break
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            label = clean(cells[0]).upper()
            if label in SCALE_WORDS and (m := re.match(r"(\d)", clean(cells[1]))):
                pending = SCALE_WORDS[label]
                page["scores"][pending] = int(m.group(1))
                page.setdefault("scoreLabels", {})[pending] = clean(cells[1])
            elif label.startswith("RATIONALE") and pending:
                page["rationale"][pending] = clean(cells[0].split(":", 1)[1])
            elif label == "PRACTICAL TIP":
                page["practicalTipShort"] = clean(cells[1])
        # Prose sections
        current, buf = None, {}
        for raw in block:
            if m := re.match(r"^#### (OVERVIEW|SCIENTIFIC SUPPORT|BACKGROUND|PRACTICAL TIP)\s*$", raw.strip()):
                current = m.group(1)
                buf[current] = []
                continue
            if raw.startswith("## ") or raw.startswith("# "):
                current = None
            if current and current != "OVERVIEW":
                buf[current].append(raw.replace("#### →", "→"))
        for key, field in (("SCIENTIFIC SUPPORT", "scientificSupport"), ("BACKGROUND", "background"), ("PRACTICAL TIP", "practicalTip")):
            text = "\n".join(buf.get(key, [])).strip()
            paras = [strip_links(p) for p in re.split(r"\n\s*\n", text) if clean(p)]
            if paras:
                page[field] = {"text": "\n\n".join(paras), "citations": cites(text)}
        if page["scores"] or any(k in page for k in ("scientificSupport", "background", "practicalTip")):
            items[iid]["page"] = page
        else:
            items[iid]["pageEmpty"] = True  # heading and blank template only


def parse_new_advices(lines: list[str]) -> list[str]:
    start = find(lines, r"^# New Sleep Advices")
    end = find(lines, r"BUSTING SLEEP MYTHS", start)
    return [m.group(1) for raw in lines[start:end] if (m := re.match(r"^(\d\.\d\.\d)\. ", raw.strip()))]


def parse_myths(lines: list[str]) -> list[dict]:
    start = find(lines, r"BUSTING SLEEP MYTHS")
    end = find(lines, r"TOOLS TO HELP WITH SLEEP", start)
    myths, cur = [], None
    for raw in lines[start:end]:
        if m := re.match(r"^### \**Myth: (.+?)\**\s*$", raw.strip()):
            cur = {"myth": clean(m.group(1)), "lines": []}
            myths.append(cur)
        elif cur is not None:
            cur["lines"].append(raw)
    out = []
    for n, m in enumerate(myths, start=1):
        text = "\n".join(m["lines"])
        truth = re.search(r"Truth:\s*(.+)", text)
        paras = [strip_links(p) for p in re.split(r"\n\s*\n", text) if clean(p)]
        out.append(
            {
                "id": f"M{n}",
                "myth": m["myth"],
                "truth": strip_links(truth.group(1)) if truth else "",
                "text": "\n\n".join(p for p in paras if not p.startswith("- Truth") and not p.startswith("Truth")),
                "citations": cites(text),
            }
        )
    return out


def parse_references(lines: list[str]) -> dict:
    start = find(lines, r"^## References:")
    end = find(lines, r"^# Tab 11", start)
    refs = {}
    for raw in lines[start:end]:
        if m := re.match(r"^#### (\d+):\s*(.+)$", raw.strip()):
            body = m.group(2)
            url = re.search(r"<(\S+?)>", body)
            refs[m.group(1)] = {
                "n": int(m.group(1)),
                "citation": clean(re.sub(r"<\S+?>", "", body)),
                "url": url.group(1) if url else None,
            }
    return refs


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    lines = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
    cats, items = parse_taxonomy(lines)
    parse_summary_tables(lines, items)
    parse_classification_tables(lines, items)
    parse_item_pages(lines, items)
    new = parse_new_advices(lines)
    for iid in new:
        items[iid]["listedUnderNewSleepAdvices"] = True
    out = {
        "source": {
            "title": "SAM Wiki: Navigating Sleep Advice",
            "url": "https://docs.google.com/document/d/1B2E0eQHCcXnMW_1Qkj0X3uAy9KSmX2AXZ8mEtj7bpzE",
            "owner": "Health Culture Foundation (Sleep Awareness Month team)",
        },
        "categories": cats,
        "items": [items[k] for k in sorted(items, key=lambda s: [int(x) for x in s.split(".")])],
        "newSleepAdvices": new,
        "myths": parse_myths(lines),
        "references": parse_references(lines),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_pages = sum(1 for i in out["items"] if "page" in i)
    print(f"{len(cats)} categories, {sum(len(c['subcategories']) for c in cats)} subcategories, "
          f"{len(out['items'])} items ({n_pages} with write-ups), {len(out['myths'])} myths, "
          f"{len(out['references'])} references -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
