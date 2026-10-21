# Guidelines and consensus statements: literature search summary

Area: `guidelines`. Searched 2026-10-21. 54 findings in `guidelines.json`.

## What was searched

- **PubMed** (NCBI E-utilities and the PubMed tool): AASM clinical practice guidelines (behavioural insomnia 2021, drug treatment of insomnia 2017, circadian rhythm disorders 2015), AASM/SRS adult sleep duration 2015, AASM pediatric sleep duration 2016, AASM position statement 2021, ACP insomnia 2016, ESRS European insomnia guideline 2017 and 2023, every PubMed record with "National Sleep Foundation" plus consensus/recommendations/panel in the title (13 records), Canadian 24-Hour Movement Guidelines (early years, children and youth, adults), the WHO under-5 guideline, AAP (school start times, safe infant sleep, media use), and meta-analyses of sleep hygiene education and of stimulus control.
- **Official web pages read directly:** CDC "About Sleep" (May 2024), NHLBI "Healthy Sleep Habits" (Mar 2022), NHS "Insomnia" (reviewed Mar 2024), AASM sleepeducation.org "Healthy Sleep Habits" (Aug 2020), the Sleep Health Foundation (Australia) "Sleep Hygiene" and "Napping" fact sheets, csepguidelines.ca (Canada), and the WHO 2019 news release.
- **Full text read:** AASM 2021 behavioural guideline (PMC), Brown 2022 light recommendations, Canadian early-years guideline, NSF screen consensus (Hartstein 2024), and passages of Irish 2015. Everything else is abstract only.
- **Open-access status** was checked in OpenAlex.

## Strongest findings by concept

- **cbt-for-insomnia (5):** Every clinical body names CBT-I as the first treatment for chronic insomnia:
  - AASM 2021 (STRONG)
  - ACP 2016 (strong, moderate-quality evidence)
  - ESRS 2017 (strong, high-quality evidence)
  - ESRS 2023 (grade A, in person or digital)
  - NHS
- **Stimulus control, sleep restriction and relaxation (4):** AASM 2021 gives each a CONDITIONAL recommendation as a stand-alone therapy. Its definition of stimulus control (five instructions) supports several of our lines: `bed-is-for-sleep`, `get-up-if-you-cant-sleep` and `get-up-at-the-same-time`.
- **get-enough-sleep-for-you (4-5):** All major bodies agree adults need at least 7 hours. They disagree on the upper limit (see below). In 2026, NSF "re-certified" its 2015 ranges: 74% of 133 meta-analyses were consistent with them and none contradicted them.
- **keep-a-regular-sleep-schedule (4):**
  - The NSF regularity consensus (2023) and the AASM 2021 position statement both say regular timing matters.
  - The Canadian guidelines and WHO build "consistent bed and wake-up times" into their recommendation for every age group.
- **Light (4):** Brown et al. 2022 is an expert consensus. It recommends:
  - daytime: at least 250 lux melanopic EDI
  - evening, from at least 3 hours before bedtime: at most 10 lux
  - bedroom while asleep: at most 1 lux

  Caveat: these are melanopic EDI values, not ordinary lux, and several authors declared lighting-industry interests.

## New advice found (conceptId NEW)

1. **Sleep hygiene alone is not a treatment for chronic insomnia.**
   - AASM 2021 makes a CONDITIONAL recommendation *against* using it as a single therapy.
   - Two meta-analyses show it helps a little but is clearly worse than CBT-I:
     - Chung 2018: an 8% gap in sleep efficiency.
     - Ruan 2025: ISI mean difference 3.8 in favour of CBT-I; 85.71% of trials at high risk of bias.
   - Suggested line: "Sleep tips alone rarely fix long-lasting insomnia; if poor sleep goes on for months, ask about CBT-I."
   - This matters for how the whole dataset is framed, because most of our concepts are sleep hygiene tips.
2. **Polyphasic sleep is not recommended** (NSF 2021).
3. **Infant safe sleep** (AAP 2022): babies sleep on their backs, on a firm surface that isn't tilted, in the parents' room but not their bed. There is currently no concept for this.
4. **Later school start times / permanent standard time** (NSF 2026, AAP 2014). This is policy rather than personal advice, so it is context only.

## Where official bodies disagree (numbers matter)

| Topic | Positions |
|---|---|
| Adult upper limit | AASM/SRS: "7 or more hours", with more than 9 possibly fine for young adults, people recovering from sleep debt or people who are ill. NSF and Canada: 7-9 h. AASM's own patient page: "at least 7-8 hours". CDC mixes them by age: 18-60 "7 or more", 61-64 "7-9", 65+ "7-8". |
| Older adults | NSF and Canada: 7-8 h for 65+. AASM/SRS: no separate band. |
| Children 6-12 | AASM/CDC: 9-12 h. NSF: 9-11 h. Canada: 9-11 h (ages 5-13). |
| Infants 4-11/12 months | AASM, WHO, Canada: 12-16 h. NSF: 12-15 h. |
| Adolescents | AASM, NSF, Canada: 8-10 h. AAP school start time policy: 8.5-9.5 h. |
| Naps | NHLBI: no more than 20 min, earlier in the afternoon. Sleep Health Foundation: 15-30 min, about 2-3pm. NHS (insomnia page): "do not nap during the day". AASM stimulus control: "refrain from daytime napping". The difference probably comes from audience: no naps for people with insomnia, short naps for everyone else. |
| Caffeine cut-off | NHS: at least 6 h before bed. NHLBI: effects "can last up to 8 hours". CDC/AASM: none "in the afternoon or evening". SHF: "3 to 7 hours", or no caffeine after lunch for people with sleep problems. None of these bodies cites a trial for its cut-off. |
| Screens before bed | CDC/AASM: off at least 30 min before bed. SHF: 1-2 h, and keep them out of the bedroom. NHLBI: quiet hour before bed. NHS: not "right before" bed. The NSF consensus (Hartstein 2024) agreed screens harm sleep in children and teens, but reached **no consensus for adults** and **no consensus that screen light** (as opposed to content) harms sleep at any age. |
| Exercise timing | NHS: no exercise within 4 h of bed. NHLBI and SHF: avoid it in about the last hour. |
| Weekend catch-up | NSF 2023 reached consensus that weekend catch-up sleep "may be beneficial" when weekday sleep is short. NHLBI says to keep the weekend difference to "no more than about an hour". Our myth line ("doesn't fully make up") should not suggest catch-up sleep is worthless. |
| Getting up when you can't sleep | AASM: after 20 min. SHF: after 20-30 min. AASM 2021 clinical guideline: no minute figure. |
| Seeing a doctor | NHS: trouble sleeping "for months" (chronic = 3 months or more). Our line says "more than a few weeks". |
| Melatonin | AASM 2017 suggests not using it for chronic insomnia (WEAK). ESRS 2023 does not recommend fast-release melatonin, but allows prolonged-release melatonin for up to 3 months in people 55 and over. AASM 2015 endorses timed melatonin for delayed sleep phase. None of these addresses jet lag. |
| Light / exercise for insomnia | ESRS moved from "needs further evaluation" (2017) to "may be useful as adjunct to CBT-I" (2023). |
| Light therapy for a late body clock | AASM 2015 endorses it for children and adolescents with delayed sleep phase. For adults, the endorsed option is timed melatonin. |

## Gaps

- **No NSF caffeine consensus statement found in PubMed** (searched NSF-titled records). The caffeine findings rely on public pages and Irish 2015, which is a narrative review.
- **Not read beyond the abstract (blocked or not open access):**
  - ESRS 2023 full text: Wiley bot check, so its exact sleep hygiene wording is unverified.
  - NSF screen "practical suggestions" (Grandner 2025, PMID 40701900): no abstract, not open access.
  - Full text of the AASM pediatric statement. Its ranges were read from the CDC page that cites it.
  - British Association for Psychopharmacology 2019 (PMID 31271339) and VA/DoD 2019 (PMID 32066145): the abstracts carry no specific recommendations, so they were not recorded as findings.
- **Nothing found in any guideline** for:
  - breathing techniques (4-7-8, box breathing, etc.)
  - weighted blankets, scents, binaural beats or pink noise
  - mouth taping, magnesium, kiwi or tart cherry, socks
  - cognitive shuffling or gratitude lists
  - blue-blocking glasses, red night lights
  - delaying the first coffee

  Bodies are silent on these, so evidence must come from trials and reviews.
- **No body gives a bedroom temperature number** (all say "cool").
- **Light therapy for adults with a late body clock:** not explicitly endorsed in AASM 2015.

## Numbers to verify before publishing

- AASM pediatric ranges: check against the JCSM full text (PMID 27250809).
- CDC page date (May 15, 2024) and NHLBI page date (Mar 24, 2022): public pages change, so re-check before citing.
- Brown 2022 values are melanopic EDI. Do not present them as ordinary room lux.
