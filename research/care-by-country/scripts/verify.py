"""Re-verify every PMID in comparison.json and existing-comparisons.json against PubMed esummary.

usage: python3 -I verify.py RESEARCH_DIR REPORT_PATH
"""
import difflib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

d = Path(sys.argv[1])
rows = json.loads((d / "comparison.json").read_text())
comp = json.loads((d / "existing-comparisons.json").read_text())

cited = []  # (where, pmid, title, year, doi)
for r in rows:
    c = r.get("citation") or {}
    if c.get("pmid"):
        cited.append((r["id"], str(c["pmid"]).strip(), c.get("title") or "", c.get("year"), c.get("doi")))
for i, c in enumerate(comp):
    if c.get("pmid"):
        cited.append((f"existing-comparisons[{i}]", str(c["pmid"]).strip(), c.get("title") or "", c.get("year"), c.get("doi")))

pmids = sorted({p for _, p, *_ in cited})
summ = {}
for i in range(0, len(pmids), 100):
    batch = ",".join(pmids[i:i + 100])
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={batch}&retmode=json"
    with urllib.request.urlopen(url, timeout=60) as resp:
        res = json.load(resp)["result"]
    for p in res.get("uids", []):
        summ[p] = res[p]
    time.sleep(0.4)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"<[^>]+>", "", s.lower()))


report, bad = [], 0
for where, p, title, year, doi in cited:
    s = summ.get(p)
    if not s or "error" in s:
        report.append(f"MISSING  {p}  {where}  cited title: {title[:80]}")
        bad += 1
        continue
    pt = s.get("title", "")
    ratio = difflib.SequenceMatcher(None, norm(title), norm(pt)).ratio() if title else 0
    pyear = (s.get("pubdate") or "")[:4]
    pdoi = next((a["value"] for a in s.get("articleids", []) if a["idtype"] == "doi"), "")
    flags = []
    if ratio < 0.6:
        flags.append(f"title {ratio:.2f}")
    if year and pyear and str(year) != pyear and abs(int(str(year)[:4]) - int(pyear)) > 1:
        flags.append(f"year {year} vs {pyear}")
    if doi and pdoi and doi.lower().strip() != pdoi.lower():
        flags.append(f"doi {doi} vs {pdoi}")
    status = "CHECK" if flags else "OK"
    if flags:
        bad += 1
    report.append(f"{status:7}  {p}  {where}  {'; '.join(flags)}\n         cited:  {title[:110]}\n         pubmed: {pt[:110]} ({pyear}) {pdoi}")

Path(sys.argv[2]).write_text("\n".join(report) + "\n")
print(f"{len(cited)} citations, {len(pmids)} unique PMIDs, {len(summ)} found, {bad} need checking")
