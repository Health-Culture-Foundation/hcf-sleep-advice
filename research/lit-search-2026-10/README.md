# Literature search, October 2026

Five Claude agents searched one area each on 2026-10-21. Each followed [FORMAT.md](FORMAT.md): every finding has a PMID or DOI the agent looked up, a free-to-read check, and a note on what was read (mostly abstracts). Official web pages (CDC, NHLBI, NHS, AASM patient site, Sleep Health Foundation, WHO, Canada) are cited by URL.

| Area | Findings | Summary |
|---|---|---|
| Guidelines and consensus | 54 | [guidelines.md](guidelines.md) |
| Body clock and light | 40 | [body-clock-light.md](body-clock-light.md) |
| Mind and behavior | 53 | [mind-behavior.md](mind-behavior.md) |
| Substances, body, bedroom | 74 | [substances-body-environment.md](substances-body-environment.md) |
| Myths, audiences, gaps | 57 | [myths-audiences-gaps.md](myths-audiences-gaps.md) |

**Check after the agents finished:** all 206 PMIDs resolved in PubMed, with matching first author, year and DOI. Three trivial mismatches: two truncated titles and a WHO book record with an empty title.

**How it feeds the dataset:** `scripts/build.py` attaches each finding to its concept (`evidence.literature`), proposes `evidenceSupport` from the guideline- and review-level findings, and turns the 40 "NEW" findings into 18 new concepts (`origin: "literature"`).

## Headlines
- **Sleep hygiene tips alone don't treat chronic insomnia.** AASM 2021 advises against sleep hygiene as the only treatment; CBT-I is first-line in every guideline. Most concepts in this dataset are sleep hygiene tips, so the dataset now says this in `tips-alone-dont-fix-insomnia`.
- **Plain lines rewritten** (old wording kept in `plainBefore`): rest-even-if-awake, light-therapy-for-a-late-body-clock, no-hard-workouts-right-before-bed, try-pink-noise, dont-sleep-in-much-on-weekends.
- **Lower evidence than the wiki claimed:** screens before bed (5 → 3), mouth taping (4 → 2), pink noise (4 → 2), 4-7-8 breathing (4 → 2; the only study measured heart rate, not sleep), cognitive shuffling (4 → 2; conference abstracts only).
- **Official numbers disagree:** naps (≤20 min NHLBI, 15–30 min Sleep Health Foundation, none for insomnia NHS); caffeine (6 h NHS, 3–7 h SHF, 8.8 h per Gardiner 2023 meta-analysis); devices off (30 min CDC/AASM, 1–2 h SHF); exercise (not within 4 h NHS, about 1 h NHLBI/SHF/Stutz 2019); adult sleep (7 or more AASM, 7–9 NSF).

## Before quoting anything
- Abstract-level reading only for most findings; check full text before publishing numbers.
- Brown 2022 light thresholds are melanopic EDI, not ordinary lux; several authors declared lighting-industry interests.
- Arab 2024 prints an impossible confidence interval; it was left out.
- AASM pediatric sleep ranges were read via the CDC page; check the original.
- The European insomnia guideline 2023 full text was bot-blocked; its sleep hygiene wording is unverified.
- Conflicts of interest: Espie (Sleepio/Big Health) on digital CBT-I and HABIT; Huberman senior author on the cyclic sighing trial (Balban 2023); Gradisar (Sleep Cycle) on Bauducco 2024.
