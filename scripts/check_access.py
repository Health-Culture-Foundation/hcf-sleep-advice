"""Record whether each cited source is free to read.

DOIs are looked up in OpenAlex (open_access.is_oa). PubMed Central, NCBI
Bookshelf and .gov pages are free by definition. Other web pages are marked
'web page (not checked)'. Results are cached in sources/citation-access.json
so the build does not hit the network; re-run to refresh.

    python3 -I scripts/check_access.py
"""

import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sources" / "citation-access.json"
DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s<>]+)", re.I)


def doi_of(url: str | None) -> str | None:
    if not url:
        return None
    m = DOI_RE.search(urllib.parse.unquote(url))
    return m.group(1).rstrip(".").lower() if m else None


def openalex(doi: str) -> dict:
    url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/")
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            oa = json.load(r).get("open_access", {})
        return {"free": bool(oa.get("is_oa")), "how": f"OpenAlex: {oa.get('oa_status')}", "readUrl": oa.get("oa_url")}
    except Exception as e:  # noqa: BLE001 - record and move on
        return {"free": None, "how": f"OpenAlex lookup failed: {e.__class__.__name__}"}


def classify(url: str | None) -> dict:
    if not url:
        return {"free": None, "how": "no link"}
    if doi := doi_of(url):
        return {"doi": doi, **openalex(doi)}
    host = urllib.parse.urlparse(url).netloc.lower()
    if "ncbi.nlm.nih.gov" in host:
        return {"free": True, "how": "PubMed Central / NCBI Bookshelf"}
    if host.endswith(".gov"):
        return {"free": True, "how": "US government web page"}
    return {"free": True, "how": "web page (not checked for paywall)"}


def main() -> None:
    wiki = json.loads((ROOT / "sources/sam-wiki/extract.json").read_text())
    extra = json.loads((ROOT / "editorial/sources.json").read_text())["sources"]
    out = {"checked": date.today().isoformat(), "wikiReferences": {}, "editorialSources": {}}
    for n, ref in wiki["references"].items():
        out["wikiReferences"][n] = {"url": ref["url"], **classify(ref["url"])}
        time.sleep(0.1)
    for key, src in extra.items():
        url = f"https://doi.org/{src['doi']}" if src.get("doi") else src.get("url")
        out["editorialSources"][key] = {"url": src.get("url"), **classify(url)}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    free = sum(1 for v in out["wikiReferences"].values() if v.get("free"))
    print(f"{free}/{len(out['wikiReferences'])} wiki references free to read -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
