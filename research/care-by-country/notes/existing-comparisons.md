# Existing cross-country comparisons of sleep care: is this a gap?

Slug: existing-comparisons. 49 rows in `existing-comparisons.json` (47 PubMed items, every PMID checked with E-utilities esummary on 2026-10-21, plus 2 agency reports). Mostly read as abstracts. Full text read for: Watanabe 2026 and the ATS 2023 PAP policy statement.

## Verdict on guidelines: a real gap, with some prior work

Nobody has published a thorough, current comparison of sleep-medicine guidelines across countries and conditions that goes down to the level of individual drugs. Three kinds of work come close. None of them does that job.

1. **Quality appraisals (AGREE II and RIGHT).** These exist for insomnia (Zhu 2022: 26 guidelines) and adult OSA (Xu 2024: 44 guidelines), plus sleep surgery and CAM/TCM subsets. They score how well each guideline was made. They do not compare what the guidelines recommend. All are paywalled except the CAM ones. None publishes its data in a form a program can read.
2. **Recommendation comparisons.** These are small or cover one drug class.
   - Seow 2022: 10 insomnia guidelines. It found guidelines "diverged in the choice of first-line pharmacotherapy" and that dose and duration advice "varied and were nonspecific". It is paywalled and predates the 2023 European update, orexin antagonists, and the 2025 deprescribing guidelines.
   - Brandt 2024 (EClinicalMedicine, free): 113 documents, 25 of them on insomnia, from every region. This is the most thorough item found. It covers benzodiazepines and Z-drugs only, prescribing and deprescribing. The most common duration cap was under four weeks, and tapering advice differed substantially. The search ran to October 2023. Most authors sit on the board or advisory group of a benzodiazepine-harm non-profit.
3. **Other conditions.**
   - RLS: no cross-guideline comparison found. The nearest are McWilliams 2024 (iron guidelines: 9 of 58 mention RLS) and a Latin-America commentary.
   - Narcolepsy: no comparison found. Only the EAN 2021 and AASM 2021 guidelines themselves.
   - Pediatric OSA: one scoping review on screening children with obesity (16 of 30 obesity guidelines include OSA screening, with no consistent method).
   - Older adults and primary care: no cross-guideline appraisal found. The Polish 2023 and Canadian guidelines exist individually.

**What is missing:** one source that covers several countries and several conditions at the level of individual decisions (CBT-I first, each drug class, duration limits, HSAT, CPAP rules, GLP-1, RLS drugs, narcolepsy drugs, melatonin status). It would need to be open, kept current, and machine-readable, with each recommendation's wording, grade, date and conflict-of-interest notes on its own row. Nothing like this was found.

## Verdict on care pathways: a bigger gap (Kalman's hunch holds)

- **OSA.** The only multi-country pathway survey is Fietze 2011, repeated in 2022 (26 European countries, 36 centres). One or two centres answered for each country. Its key numbers: home sleep apnea testing used by 76% of centres in 2010 and 89% in 2020; PSG as the only test fell from 24% to 12%; telemedicine is used in follow-up by 73%. Smaller pieces add to this:
  - ESADA surveys on multi-night testing, GLP-1 use, and oral-appliance access.
  - A Canada vs Australia patient survey: diagnostic test within 3 months for 59% of Canadians vs 76% of Australians.
  - A survey of 15 sub-Saharan African countries: CPAP available in 8 of 15, with partial insurance cover in only 3.
  - An EU survey on driving-licence rules (thorough, but one narrow topic).
- **Payer rules.** The only comparison is a few paragraphs in the ATS 2023 policy statement. Australia, England and Canada set no adherence requirement for CPAP coverage. US CMS requires 4 hours a night on 70% of nights. Japan requires an in-lab PSG and visits every 1 to 3 months.
- **Insomnia.** Not found anywhere: who delivers CBT-I in each country, whether it is reimbursed, waiting times, how stepped care is set up, or how digital CBT-I is paid for. Somnio is covered under Germany's DiGA scheme, Sleepio has NICE guidance (2022), and Somryst has FDA clearance in the US. No paper puts these side by side. On insomnia there are only expert-opinion pieces, most written by authors with ties to Idorsia (Ellis 2023, Palagini 2025, Soyka 2023), and the US-only Thomas 2016 count: 88% of 752 behavioral sleep medicine providers worldwide were in the US.
- **Waiting times by country.** Only the Canada vs Australia paper has them.

## Prescribing data (strong) vs. guidance (weak)

How much of these drugs each country uses is well measured:
- 67 countries' sales data (Ma 2023, ends 2018).
- Nordic registers: 17 vs 93 DDD per 1,000 people per day in 2020.
- PROTECT-EU, SHELTER and the Baltic studies.
- The OECD older-adult indicator. Its page was blocked; figures are unverified.
- INCB S-DDD tables (not read).

None of these ties use to what each country's guidelines say, and none covers orexin antagonists. Linking use to guidance is an obvious contribution HCF could make.

## Melatonin regulation

The patchwork is confirmed but nobody has tabulated it. Vanhee 2025 says EU status is prescription or OTC "depending on the country", with country-specific limits for supplements. Skrzelowski 2021 says the US is the least regulated. No country-by-country table was found.

## How HCF could fill the gap

Publish the care-by-country dataset as the missing artifact:
- one row per country × condition × decision;
- wording copied from the source, the body's own grade, date and status, and COI;
- pathway fields: who diagnoses, HSAT allowed, CPAP adherence rule for coverage, CBT-I reimbursed, dCBT-I route, melatonin status;
- links to use data (OECD, Nordic and Baltic registers).

Several published items can seed or cross-check rows: Brandt 2024's data chart, Seow 2022's recommendation matrix, Fietze 2022's country answers, and McNicholas 2025's driving-rule table. Credit them and say where HCF goes further: more conditions, kept current, open, machine-readable.

## Blocked / not read
- OECD Health at a Glance 2023/2025 pages returned HTTP 403. Figures in the JSON come from a search summary and are marked NOT VERIFIED.
- The INCB technical-report URL tried returned 404. The current PDF is not located.
- Paywalled, abstract only: Zhu 2022, Seow 2022, Xu 2024, Mandavia 2020, Fietze 2011, Karkala 2026.

## Open questions
- [ ] Get the Seow 2022 and Zhu 2022 full texts to list exactly which guidelines and countries they covered.
- [ ] Read the Fietze 2022 full text (OpenAlex says it is free) for per-country reimbursement answers.
- [ ] Find out whether the JCSM "Global practice of sleep medicine" series has more country articles. Only Iran surfaced by title.
- [ ] Check the World Sleep Society or ESRS for any unpublished service surveys. None was found in PubMed.
