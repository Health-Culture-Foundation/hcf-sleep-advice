# Literature search: substances, food, exercise, temperature, the bedroom and the body

Area: `substances-body-environment` · Searched 2026-10-21 · 74 findings from 72 papers in `substances-body-environment.json`

## What I searched

I searched PubMed through NCBI E-utilities, using relevance-sorted queries for each topic in the brief. Most queries were restricted to systematic reviews and meta-analyses, plus named papers: Gardiner 2023, Drake 2013, Stutz 2019, Frimpong 2021, Haghayegh 2019 and Ekholm 2020. Open access was checked through OpenAlex (`open_access.is_oa`) and PMC ids. Every PMID, DOI, PMCID, year and first author was checked against PubMed esummary after the JSON was written.

What I read: abstracts only, except the ACG 2022 GERD guideline. For that one I read the recommendation list in the PMC full text. Numbers are copied from the abstracts.

There are more findings than the suggested 15-40 because the area has seven sub-topics. Small or weak studies are kept only where nothing better exists, and they are marked with low support scores.

## Strongest findings by concept

| Concept | Best source(s) | Suggested support | Comment |
|---|---|---|---|
| caffeine-cutoff | Gardiner 2023 MA (24 studies); Drake 2013 RCT | 4 | Coffee ≥ **8.8 h** before bed. A pre-workout dose (217.5 mg) needs ≥ 13.2 h. Drake: 400 mg even **6 h** before bed still disturbed sleep. |
| caffeine-and-big-meals-early | Chang 2025 MA; Clark 2017 SR; ACG 2022 guideline; two small dinner-timing RCTs | 4 for caffeine, 2-3 for meals | Caffeine part is solid. The meal part rests on the ACG reflux recommendation ("avoid meals within 2-3 hours of bedtime", conditional, low evidence) and two small RCTs that disagree (Duan 2021 vs Enomoto 2026). |
| myth-alcohol-helps-sleep | Gardiner 2025 MA (27 studies); Ebrahim 2013 | 4 | About 2 drinks already cut REM. Falling asleep faster was only seen at about 5 drinks. |
| no-alcohol-close-to-bedtime | Pietilä 2018 (4,098 people, HRV) | 3 | Dose-dependent loss of overnight recovery, even at low intake. No study gives a timing cutoff ("3 hours" is not evidence-based). |
| cannabis-and-sleep | Cochrane 2026 (9 RCTs); Velzeboer 2025 MA; Althoff 2024; AASM 2018 | 4 | Medical cannabis: little to no meaningful benefit for insomnia, more adverse events. Use within 3 h of sleep is linked to more night waking. Withdrawal disturbs sleep. Not a treatment for apnea. |
| exercise-regularly | Xie 2021 MA; Wang 2025 NMA (86 RCTs); Tian 2024 umbrella | 5 | All exercise types help. Optimum around 920 MET-min/week (U-shaped). |
| no-hard-workouts-right-before-bed | Stutz 2019 MA; Frimpong 2021 MA | 4 | Evening exercise is fine overall. Possible harm only from **vigorous exercise ending ≤ 1 h before bed**. HIIT 2-4 h before bed did not disrupt sleep. |
| warm-bath-or-shower-before-bed | Haghayegh 2019 MA | 4 | 40-42.5 °C, **1-2 h before bed**, as little as 10 min shortens sleep onset. Matches the current line. |
| keep-the-bedroom-cool-and-dark (temperature part) | Chevance 2024 SR; Baniassadi 2023; Okamoto-Mizuno 2012 | 4 | Heat clearly worsens sleep. Older adults slept best at **20-25 °C**, which is warmer than popular "60-67 °F" advice. |
| check-for-sleep-apnea | AASM 2017 guideline; USPSTF 2022 | 5 | People with symptoms should be tested (questionnaires don't count as diagnosis). USPSTF: "I" statement for screening people **without** symptoms, so it does not conflict with the line. |
| raise-the-head-of-the-bed / left-side-for-reflux | ACG 2022; Schuitenmaker 2022 SR + RCT; Simadibrata 2023 | 3-4 | ACG suggests head-of-bed elevation for night-time reflux (conditional, low). Left-side sleeping: sham-controlled RCT, 44% vs 24% success. Head-of-bed elevation for apnea: small uncontrolled studies only (support 2). |
| try-calming-scents | Shen 2026 MA (lavender, 11 RCTs); Her 2021; Xu 2024 | 2 | Positive pooled effects, but low quality and hard to blind. Biggest effects come with massage, which confounds the scent. |
| try-a-weighted-blanket | Ekholm 2020 RCT; Eron 2020; Dawson 2024 | 2-3 | One good RCT (psychiatric outpatients, d = 1.90). Reviews call the evidence thin. |
| mouth-taping | Rhee 2025 SR (the 2025 review in the brief); Alshehri 2026; Meksukree 2025 RCT | 2 | Possible harm with a blocked nose. Benefit shown only for CPAP users under supervision. Current hedge is right. |

## New advice found (conceptId NEW)

1. **Nicotine:** "Avoid nicotine (smoking or vaping), especially in the evening; it is linked to lighter, shorter sleep." Sources: Catoire 2021 MA (polysomnography: less slow-wave sleep, more waking), Amiri 2020 (RR 1.47 for later sleep problems), Sulthana 2025 (e-cigarettes, OR 1.38 for short sleep). No current concept covers nicotine. The evidence is observational. I found no study of evening nicotine timing specifically.
2. **Positional therapy for sleep apnea:** "If your snoring or apnea is worse on your back, sleeping on your side may help; ask your clinician." Source: Cochrane 2019 (AHI −7.38/h vs control; CPAP works better). This could also sit as a note under `check-for-sleep-apnea`.

## Disagreements and things to fix in the plain lines

- **Caffeine cutoff clock time.** 6 h (Drake) is a minimum, not a safe point. Gardiner's 8.8 h for one coffee means about 1-2 p.m. for a 10-11 p.m. bedtime, so "early afternoon" is right and a 4 p.m. cutoff is too late. A dose-scaled line works better: "the bigger the dose, the earlier you stop". Clark 2017 adds that sensitivity varies with age and genes.
- **Pink noise.** A 2026 RCT (Basner, *Sleep*) found all-night pink noise **reduced REM sleep**, while earplugs blocked nearly all effects of traffic-type noise. The 2022 systematic review favours pink noise only by vote count. Suggest lowering `try-pink-noise` and the support for `mask-noise-with-steady-sound` (Riedy 2021: very low quality evidence). Lean on earplugs in `keep-the-bedroom-quiet`.
- **Bedroom temperature number.** If a number is quoted anywhere, 20-25 °C (older adults, at home) conflicts with the common 60-67 °F (15.6-19.4 °C). Number to check before it ships.
- **Strength training time of day.** No evidence supports "afternoon or early evening". Hu 2026 found no time-of-day advantage for sleep, and Kovacevic 2018 supports strength training without saying when. Suggest rewording to "any time that suits you, but not a hard session right before bed".
- **"Finish hard workouts a couple of hours before bed."** The evidence supports about 1 h for vigorous exercise (Stutz) and finds 2-4 h fine (Frimpong). The current line is a little cautious but safe.
- **Late dinner.** Duan 2021 (1 night, n = 20) found no harm. Enomoto 2026 (4 nights, n = 13 women) found worse sleep continuity. The strongest support for "no big meal 2-3 h before bed" is for people with **reflux** (ACG).
- **High-carb snack.** Afaghi 2007's high-GI benefit came from a meal **4 h before bed**. The same meal 1 h before bed was worse. The carbohydrate meta-analysis is mixed. `small-snack-before-bed` should not imply carbs help sleep.
- **Earplugs vs eye masks.** In ICU patients, eye masks helped and earplugs alone did not (Fang 2021). In healthy adults with traffic noise, earplugs worked (Basner 2026). ICU evidence is marked with a caveat throughout.

## Gaps (nothing good found)

- **delay-first-coffee** (waiting 90 min after waking): no trial or review found. Searches on caffeine timing after waking, cortisol awakening response and sleep inertia turned up only sleep-inertia studies, which are not relevant. Treat this as unsupported popular advice.
- **3-2-1-rule:** no study tests the combined rule. Pieces only: the ACG 2-3 h meal advice (reflux), nocturia reviews (less fluid in the evening), and no alcohol timing data.
- **frozen-water-bottle:** no study. Cooling bedding showed no sleep benefit in healthy adults in normal conditions (Pasquier 2025). The heatwave guidance (Altena 2023) may contain practical cooling tips in its full text (not read).
- **gentle-stretching-before-bed:** trials test yoga programmes, not a few minutes of stretching at bedtime.
- **wear-socks-to-bed:** only one 6-person study (Ko 2018).
- **nose-breathing-exercises:** nothing direct. Alshehri 2026 shows nasal obstruction worsens apnea, which supports keeping the nose clear but not breathing exercises.
- **Mattress and pillow:** "medium-firm" appears consistently. Pillow design did not change sleep quality in people with neck pain. Funding of the underlying mattress trials was not assessed.

## Numbers to verify before they ship

- 8.8 h / 13.2 h caffeine cutoffs and the doses behind them (Gardiner 2023)
- "~2 drinks" = 0.50 g/kg and "~5 drinks" = 0.85 g/kg (the paper's own conversions)
- 20-25 °C bedroom range (older adults only)
- 920 MET-min/week. "≈230 min of moderate activity" is my arithmetic, not the paper's.
- 40-42.5 °C water, 1-2 h before bed, ≥10 min (Haghayegh 2019)

## Conflicts of interest noted

- Pietilä 2018: authors employed by Firstbeat (HRV devices) and Nokia.
- Schuitenmaker 2022 SR: industry funding and fees declared by two authors.
- Schade 2020 (pink-noise study, not included): sleep-tech company grants.
- Not visible in the abstract, check in the full text: Lopresti 2026 (magnesium), Ekholm 2020 (weighted blanket), Schuitenmaker 2022 RCT (device), Oelke 2017 (nocturia consensus).
