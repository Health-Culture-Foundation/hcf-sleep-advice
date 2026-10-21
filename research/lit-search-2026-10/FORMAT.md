# Output format for literature-search agents

Write two files in this folder, named after your area (e.g. `body-clock-light`):

1. `<area>.json`: a JSON array of findings:

```json
{
  "conceptId": "screens-before-bed",          // id from concepts.md, or "NEW"
  "newAdvice": null,                          // if conceptId is NEW: one plain line, e.g. "Keep naps under 20 minutes."
  "question": "Does avoiding screens before bed improve sleep in adults?",
  "studyType": "guideline | consensus | systematic review | meta-analysis | RCT | cohort | other",
  "population": "adults 18-65 / adolescents / older adults / insomnia patients ...",
  "direction": "supports | against | mixed | no effect | harm",
  "keyResult": "Paraphrase of what the abstract reports, with the numbers exactly as reported.",
  "citation": {"authors": "Hartstein LE, et al.", "year": 2024, "title": "...", "journal": "Sleep Health",
               "doi": "10.1016/...", "pmid": "38806392", "pmcid": "PMC..."},
  "freeToRead": true,                          // PMC copy, open access per OpenAlex, or free government page
  "freeUrl": "https://pmc.ncbi.nlm.nih.gov/articles/PMC.../",
  "whatWasRead": "abstract | full text | guideline page",
  "suggestedEvidenceSupport": 1-5,             // 5 = strongly supported; your judgement from this source
  "disagreement": "Optional: how this differs from another source or from the current plain line.",
  "notes": "Caveats: small sample, industry funding, conflict of interest, population limits."
}
```

2. `<area>.md`: a short summary for humans: what you searched, the strongest findings per concept, new advice found, disagreements, and gaps (concepts where you found nothing good).

## Rules
- **Never invent a citation.** Every finding needs a PMID or DOI you looked up and confirmed (PubMed tools, NCBI E-utilities, or OpenAlex). Report only what you actually read; usually that is the abstract, so say so.
- Prefer, in order: guidelines and consensus statements, systematic reviews and meta-analyses, then large RCTs. Prefer 2015 or later, but include older landmark guidelines.
- Prefer free-to-read sources, and check `freeToRead` (PMC id, or OpenAlex `open_access.is_oa`: https://api.openalex.org/works/doi:<doi>).
- Copy numbers exactly as the source states them. Don't paraphrase a number into a different number.
- Record conflicts of interest the abstract declares.
- Note when evidence comes only from one population (e.g. only adolescents, only insomnia patients).
- Aim for quality over quantity: 15–40 findings is fine.
- Do not edit any other files in the repository, and do not commit.
