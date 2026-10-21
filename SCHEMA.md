# Sleep advice dataset: schema

`data/sleep-advice.json` is the full dataset. `data/sleep-advice.csv` is a flat
copy for spreadsheets (one row per item, lists joined with `; `).
`data/sleep-advice.skos.ttl` is the same concepts as a SKOS concept scheme
(Turtle). `data/glossary-mapping.csv` lists every health-glossary sleep entry
and the advice items it maps to. `TAXONOMY.md` is a readable tree, generated
from the data.

## The model: a concept scheme, not a flat list

Each item is a **concept** in the sense of
[SKOS](https://www.w3.org/TR/skos-reference/), the W3C standard for
thesauri and taxonomies:

- one **preferred label** (`plain`, the one-liner), and any number of
  **alternative labels** (`altLabels`: synonyms, the source's own wording,
  clinical names, glossary term names);
- **broader / narrower** links, so a specific technique (box breathing) sits
  under a general one (relaxation techniques) even across categories;
- **related** links, and **conflictsWith** for advice that pulls the other way;
- category and subcategory are themselves concepts (top of the tree).

Duplicates are **merged, not deleted**: the merged item keeps its ID with
`status: "merged"` and `mergedInto`, and its wording becomes an alternative
label on the surviving concept. Links to old IDs keep working.

On top of the hierarchy, three **facets** cut across categories (see `facets`
below). That makes it a small ontology: the same item can be found by
what it is (category), how it is said to work (mechanism), when you do it
(time of day) and who it is especially for (condition).

Everything is a **draft**. Each field says where it came from and whether a
person has checked it. Nothing in the dataset should be read as reviewed
until its status says so.

## Top level

| Field | Meaning |
|---|---|
| `name`, `version`, `description` | Dataset identity. `0.x` while it is a draft. |
| `conceptBase` | Base IRI for concepts (`https://health-culture.org/sleep-advice/`). A placeholder: nothing resolves there yet. |
| `license` | CC BY 4.0, attribution "Health Culture Foundation". |
| `lastChecked` | Date the whole build was last checked. |
| `scales` | What each 1–5 tag means (below). |
| `audienceTags` | The audience vocabulary and what each tag means. |
| `sources` | The three inputs: SAM wiki, health-glossary drafts, tagging taxonomy v1.2. |
| `categories` | The wiki's 4 categories and 14 subcategories, with their ICHI and ICD-11 codes. |
| `items` | The advice, concepts and myths. |

## Item

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable slug. Never reused or renamed, even if the wording changes. Also the last part of the concept IRI (`conceptBase` + id). |
| `status` | `active` \| `merged` | Merged items stay in the file so their IDs keep resolving. |
| `mergedInto` | string \| null | For merged items: the concept that replaced it. Survivors list `mergedFrom`. |
| `kind` | `advice` \| `concept` \| `group` \| `myth` | A concept is background the advice relies on (e.g. body temperature low point). A group is an editorial heading that gathers related advice (e.g. stimulus control). A myth is a common belief the wiki corrects. |
| `altLabels` | list | Alternative labels: synonyms, source wording, clinical names, glossary term names, and the wording of merged items. |
| `broader` / `narrower` | list of ids | Hierarchy within the advice. `narrower` is computed. Items with no `broader` hang directly under their subcategory. |
| `related` | list of ids | Associated advice, both directions. |
| `conflictsWith` | list | `{id, why}`: advice that pulls the opposite way. Both directions. |
| `origin` | `sam-wiki` \| `health-glossary` | Which input the item first came from. |
| `wikiNumber` | string \| null | The wiki's number (`1.3.1`, `M4`). Kept for traceability, not as an ID: numbers change when the taxonomy is rearranged. |
| `categoryPath` | list | Category, then subcategory, from the wiki taxonomy. |
| `placement` | string | `wiki taxonomy`; or listed in the wiki's "New Sleep Advices" (numbered but not yet placed); or `proposed` for glossary-only items placed by Claude. |
| `sourceWording` | string | The wording in the source, unchanged. |
| `plain` | string | **Layer 1.** One plain line a reader can act on. Drafted by Claude, unreviewed (`plainStatus`). |
| `paragraph` | object | **Layer 2.** `text`, `from`, `status`. Wiki items use the wiki's short practical tip; glossary items use the glossary's AI-drafted definition. `null` text means it still needs writing. |
| `evidence` | object | **Layer 3.** See below. |
| `tags` | object | The five 1–5 scales. See below. |
| `audience` | list | Audience tags. `all-ages-and-cultures` is the default; others narrow it. |
| `audienceNote` | string \| null | Who it may not fit, and why. |
| `disagreements` | list | Where sources disagree. See below. |
| `facets` | object | `mechanism`, `timeOfDay`, `condition` (lists of facet values) and `status`. See below. |
| `conditionCodes` | list | ICD-11 codes reached through `facets.condition`, per item: `{code, title, via}`. More precise than `codes`, which the wiki set per subcategory. |
| `codes` | object | `ichi`, `icd11` (each `{code, title, wikiTitle, exists, titleOutdatedInWiki}`), `verified`, `checkedOn`, `note`. |
| `glossary` | list | Matching health-glossary sleep **advice** entries: `glossaryId`, `term`, `relation`, `status`, `url` (null if the entry has no term page yet). |
| `glossaryTerms` | list | Matching published glossary **terms** (e.g. Sleep Hygiene, Jet Lag Syndrome), with URL. |
| `relatedAdvice` | list | Myths only: wiki numbers of the advice it relates to. |
| `editorNotes` | string \| null | Internal notes: duplicates, gaps, score conflicts, things to check. |
| `plainStatus` | string | Review status of `plain`. |
| `tested` | object | `withReaders`: has this wording been tested with real readers? All `false`. |
| `changeLog` | list | When the guidance or wording changes: `{date, what, why, source}`. Empty in 0.1. |
| `license` | string | `CC-BY-4.0`. |
| `lastChecked` | date | When this item was last checked. |

### `evidence`

| Field | Meaning |
|---|---|
| `summary` | The wiki's "Scientific support" text, unchanged. Not checked against its citations. |
| `status` | `wiki text with citations`, `wiki text, no citations`, `no write-up in the wiki`, or (glossary items) see `reviewNote`. |
| `citations` | Every reference the wiki write-up links to: `wikiRef` (its number in the wiki's reference list), `citation`, `url`, `doi`, `freeToRead`, `accessCheckedBy`, `readUrl`. |
| `moreSources` | Sources added in the editorial layer (e.g. the NSF 2024 consensus for screens), with what was actually read (`whatWasChecked`). |
| `reviewNote` | Glossary items only: the glossary's review note, including NOT VERIFIED flags. |

`freeToRead` comes from `scripts/check_access.py`: OpenAlex open-access status
for DOIs; PubMed Central, NCBI Bookshelf and `.gov` pages count as free; other
web pages are marked free but "not checked for paywall". `false` means OpenAlex
reports the article as closed; `readUrl`, when present, is a free copy.

### `tags`

Five scales from the Advice Tagging Taxonomy v1.2, renamed per Kalman's
feedback, all running 1 (low) to 5 (high):

| Dataset name | Wiki name | 1 | 5 |
|---|---|---|---|
| `reach` | Commonality ("popularity" was rejected) | rare | universal |
| `ease` | Practicality / Ease of implementation | impractical | effortless |
| `impact` | Impact | minimal | game-changer |
| `novelty` | Novelty | obvious | feels like a secret |
| `evidenceSupport` | Scientific red flags, **flipped** (6 − red flag) | red flag | strongly supported |

Low `reach` is not a mark against advice. Niche advice that works, or that
works for one audience, is exactly what the dataset should surface.

Each scale is an object:

| Field | Meaning |
|---|---|
| `value` | The current best score: Claude's proposal if there is one, else the wiki's. Use this for charts. |
| `from` | `proposal`, or which wiki table the value came from (`wiki itemPage`, `wiki summaryTable`, `wiki classificationTable`). |
| `wikiValue` | The wiki's score (item page first, then summary table, then classification table). |
| `wikiScores` | All three wiki scores where present. The wiki scored items three times and the sets often disagree. |
| `spread` | Max − min of `wikiScores`. |
| `rationale` | The wiki's one-line reason, when the item page gives one. |
| `proposal` | `{value, reason, by}`: Claude's first-pass score (2026-10-21). |
| `status` | `proposed by Claude, unreviewed`, `wiki draft, unreviewed`, or `not scored`. |
| `reviewed` | `false` everywhere. Set `true` when a person has reviewed the score. |

Proposals were made in `editorial/scores.json` by these rules:

- Where the wiki's three scores disagree, one value was picked, with the reason.
- Reach, ease, impact and novelty were proposed for every unscored advice item.
  These are judgement calls.
- `evidenceSupport` is capped at 3 when the dataset holds no citation for the
  item: a strong evidence score should be backed by something a reader can check.
- `evidenceSupport` is never proposed for an unscored item, because that would
  mean inventing evidence. These stay `null`.
- Myths are not scored.

### `disagreements`

```json
{
  "about": "Caffeine cutoff",
  "positions": [
    {"source": "nhlbi-guide", "says": "Effects can last up to 8 hours (p. 28); no clock time."},
    {"source": "breus-youtube", "says": "2 p.m.; half-life 6-8 hours."}
  ]
}
```

`source` is a key in `editorial/sources.json`, or `wiki` for the SAM wiki
itself. Only positions a named source states are recorded; a disagreement is
not a verdict.

### `codes`

ICHI codes are set per wiki category and ICD-11 codes per subcategory, so
every item in a subcategory carries the same codes. Every code was looked up
in the WHO browsers on 2026-10-21 (`sources/code-check.json`):

- All 8 ICD-11 codes exist (ICD-11 MMS 2025-01). The wiki's titles for 7A60
  and 7A61 are outdated: they are now "Delayed sleep-wake phase disorder" and
  "Advanced sleep-wake phase disorder". `title` holds the current title,
  `wikiTitle` the wiki's.
- All 7 ICHI codes exist in WHO's ICHI maintenance platform (a
  work-in-progress version, not a formal release).
- **Fit is not reviewed.** ICD-11 codes name disorders, so on general advice
  they mean "relevant to", not "treats". ICHI also has ATK.PN.ZZ "Advising
  about sleep functions", which may fit an advice list better than the
  wiki's "Education" code.

`verified` is `"code exists; fit not reviewed"` for wiki items and `false` for
items without codes.

### `facets`

Vocabularies are defined in the top-level `facets` object (`editorial/facets.json`).
Assignments were drafted by Claude on 2026-10-21 and are unreviewed.

| Facet | Values |
|---|---|
| `mechanism`: how the sources say it works (not proof that it does) | body-clock, light-at-night, sleep-pressure, body-temperature, arousal, learned-association, substances, digestion-and-fluids, sleep-environment, breathing-and-airway, time-displacement, monitoring-and-care |
| `timeOfDay`: when you do it | on-waking, daytime, afternoon, evening, bedtime, during-the-night, any-time, ahead-of-time |
| `condition`: who it is especially relevant for | general, insomnia (7A00, 7A0Z), sleep-apnea (7A41), reflux (DA22), late-body-clock (7A60), jet-lag (7A65), shift-work (7A64), anxiety (6B00) |

All condition codes were looked up in the ICD-11 browser (`sources/code-check.json`).
In SKOS, each facet is its own concept scheme and items link to values with
`hsa:mechanism`, `hsa:timeOfDay` and `hsa:condition`.

### `glossary.relation`

| Value | Meaning |
|---|---|
| `same` | Same advice. A candidate for merging. |
| `overlaps` | Partly the same; each says something the other doesn't. |
| `narrower` | The glossary entry is a specific version of this item (e.g. Box Breathing under relaxation techniques). |
| `conflicts` | The two give opposite advice. |

## How it's built

```
Google Doc (SAM wiki) --export--> wiki.md (not committed)
  scripts/extract_sam_wiki.py  ->  sources/sam-wiki/extract.json
  scripts/check_access.py      ->  sources/citation-access.json
health-glossary data/ai/sleep  ->  sources/health-glossary/sleep-entries.json (snapshot)
WHO ICD-11 / ICHI browsers   ->  sources/code-check.json (looked up by hand)
editorial/items.json, sources.json, relations.json, scores.json (hand-edited)
  scripts/build.py             ->  data/sleep-advice.json, .csv, .skos.ttl,
                                   glossary-mapping.csv, TAXONOMY.md
```

`build.py` fails if a wiki item or glossary entry is left unmapped, if the
editorial layer names a source, tag, glossary ID or concept that doesn't
exist, or if `broader` links form a cycle.

To change wording or audiences, edit `editorial/items.json`. Synonyms,
hierarchy, merges and conflicts live in `editorial/relations.json`; score
proposals in `editorial/scores.json`. To change
the taxonomy, edit the wiki and re-run the extractor. Don't edit `data/` by
hand.
