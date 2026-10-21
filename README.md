# HCF Sleep Advice

An open list of sleep advice: what to do, in plain words, with the evidence
behind it, who it fits, and where trusted sources disagree.

**Status: draft (0.1).** Private for now. The plan is to move it to a Health
Culture Foundation GitHub organization and make it public once it has been
reviewed. Nothing here has been checked by a person yet.

## What's in it

**Browse the taxonomy: [TAXONOMY.md](TAXONOMY.md)** (category tree with every item's plain wording, tags and flags).

`data/sleep-advice.json` (and `.csv`) has 87 items:

- **62 advice items** from the Sleep Awareness Month wiki's taxonomy
  (4 categories, 14 subcategories), with the wiki's write-ups, citations and
  scores.
- **20 items** that exist only as sleep entries in the
  [health-glossary](https://github.com/vivwebsolutions/health-glossary)
  (NHLBI, Dr. Michael Breus, Andrew Huberman), placed in the wiki's categories.
- **5 myths** from the wiki's "Busting sleep myths" tab.

Each item has three layers of wording (one line, a paragraph, the evidence),
five 1–5 tags (reach, ease, impact, novelty, evidence support), audience
tags, where sources disagree, ICHI/ICD-11 codes (unverified), and links to
matching glossary terms. See [SCHEMA.md](SCHEMA.md).

`data/glossary-mapping.csv` maps all 41 glossary sleep entries to advice items.

## Why

This is the first worked example for the Open Health Communication
Declaration (vivwebsolutions/hcf-guides#6): health advice should be open,
tested, layered and quick to update. The "screens before bed" item
(`screens-before-bed`) shows why: the wiki rates it strongly supported for
everyone, while the National Sleep Foundation's 2024 consensus only found
harm for children and teens.

## Build

```sh
python3 -I scripts/extract_sam_wiki.py path/to/sam-wiki-export.md   # when the wiki changes
python3 -I scripts/check_access.py                                  # refresh free-to-read status
python3 -I scripts/build.py
```

Python 3.10+, standard library only.

## License

Data (`data/`, `editorial/`, `sources/sam-wiki/`): [CC BY 4.0](LICENSE),
attribution "Health Culture Foundation". Cited works keep their own licenses;
the dataset links to them and does not reproduce them. Glossary entries based
on Breus and Huberman videos are written in our own words.

Scripts (`scripts/`): MIT.
