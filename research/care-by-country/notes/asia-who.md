# Asia + WHO: adult insomnia and OSA guidelines, drug approvals, coverage

Slug: asia-who. 44 rows in `asia-who.json`: China 13, Japan 10, South Korea 7, WHO 6, India 5, Taiwan 1, Saudi Arabia 1, Singapore 1.
Layers: 37 guideline (drug-approval rows count as "guideline" with direction "regulatory fact"), 4 coverage, 3 pathway.
All PMIDs were checked with NCBI E-utilities (esummary/efetch).

## Main differences
- **China 2025 insomnia guideline (CSRS):** CBT-I comes first. The top drug tier puts orexin antagonists (DORAs) alongside short- and intermediate-acting Z-drugs/BZRAs. Next come other BZRAs or melatonin agonists, then sedating antidepressants (doxepin, mirtazapine, trazodone).
  - Unlike any Western, Japanese or Korean guideline, it has a full traditional Chinese medicine section: herbal formulas matched to the patient's "pattern".
  - It gives strong recommendations to rTMS and light therapy.
  - China also has a parallel CMA Neurology adult insomnia guideline (2017), which was not read.
- **China 2025 OSA guideline (Chinese Thoracic Society, published March 2026):** 18 graded recommendations.
  - Home testing is for moderate-to-severe uncomplicated OSA only.
  - Pressure titration is recommended before starting CPAP.
  - Fixed CPAP is the default "due to lower cost".
  - Tirzepatide gets a 1A grade as an add-on for obese moderate-to-severe OSA.
  - Solriamfetol or modafinil is recommended for leftover sleepiness.
  - Benzodiazepines are recommended against in OSA with insomnia (COMISA).
  - In resource-limited primary care, diagnosis from oximetry plus history is allowed.
- **Korea 2020 insomnia guideline:** adapted from AASM/ESRS. CBT-I gets a strong recommendation. Most drugs get weak "consider" wording, including trazodone (AASM says no) and triazolam.
  - Suvorexant is graded *Strong*, yet the same text says it is "not yet utilized in Korea". This looks like a table error.
  - Prolonged-release melatonin is supported for people aged 55+.
- **India IPS 2017:** prefers CBT-I but openly allows long-term hypnotics when CBT-I is unavailable, because trained therapists are scarce. This is the only guideline in this set that does so.
  - The INOSA 2014 OSA guideline (government-backed) is stale and has an ESS typo ("<10" should be ">10").
- **Japan:** the hypnotics guideline (2013) is built around stopping hypnotics, but it predates orexin antagonists. It is stale.
  - Payer rules, not guidelines, do most of the steering: fee cuts for 3+ hypnotics (from 2012) and for 12+ months of the same benzodiazepine (from 2018).
  - Published claims studies say the long-term-prescribing policies had little or no measurable effect.

## Coverage and pathway facts
- **Japan CPAP:**
  - FY2026 (令和8年度) rules appear to have cut the AHI cut-offs from 20 to 15, and from 40 to 30 for the symptoms-only route. This comes from an annotated copy of the notice plus a Chuikyo proposal; check it against the MHLW text.
  - Payment stops only if use averaged under 1 hour a day in all of the last 3 months. That is much looser than the Korean or US 4 h / 70% rule.
  - A remote-monitoring add-on has existed since FY2018 (up to 2 months between visits).
  - Patient cost is about ¥5,000 a month at 30% copay.
- **Korea NHIS:** covers PSG and CPAP rental from 1 July 2018. To keep coverage, the patient must use CPAP ≥4 h a night on ≥70% of 30 consecutive nights (21 days) within the first 90 days. The patient pays about 14 USD a month, against 1,627-2,033 USD to buy a device.
- **China and India:** no national CPAP reimbursement rule was found. India appears to be mostly out of pocket (not verified).

## Drug approvals
- **Suvorexant:** Japan approved it on 26 Sep 2014 and launched it in Nov 2014, the first launch anywhere. **The brief's "world first approval" is wrong:** the FDA approved it first, on 13 Aug 2014.
- **Lemborexant:** Japan, Jan 2020; China, May 2025 (the first orexin antagonist in China); Korea, 23 Jun 2026 (MFDS).
- **Daridorexant:** Japan, Sep 2024 (Nxera/Shionogi); China NMPA, 17 Jun 2025, "not classified as a controlled psychotropic"; Korea filed, approval expected 2027.
- **Melatonin:** Japan has approved it only for children (Melatobel, 2020, neurodevelopmental disorders), not for adults. Korea has prolonged-release melatonin 2 mg. India sells 3 mg tablets; the IPS calls it a chronobiotic, not a hypnotic.
- **Taiwan:** TFDA (April 2020) banned Z-drugs for patients with a history of complex sleep behaviours.

## WHO (absences are findings)
- No WHO guideline on adult chronic insomnia or on OSA.
- mhGAP has 11 topics and none is sleep.
- The only WHO treatment recommendation is the 2013 stress guideline, for acute insomnia after trauma: relaxation and sleep hygiene, and no benzodiazepines (standard strength for adults, strong for children).
- The EML (24th list, 2025) has no hypnotics. Diazepam is listed for anxiety, limited in 2023 to short-term emergency use.
- The 2019 under-5 guideline gives sleep hours by age.
- ICD-11 has a separate Chapter 7 for sleep-wake disorders (7A00 chronic insomnia, 7A41 OSA).

## Not found (explicit absences)
- A Korean general adult OSA/PAP guideline (only a 2023 nasal-surgery guideline).
- A Taiwanese insomnia or OSA guideline.
- A Singapore ACE insomnia guidance.
- Hong Kong and Turkey guidelines (quick PubMed searches found nothing).
- A Saudi guideline (only a 2019 Delphi toward one).
- The Chinese CMA primary-care (基层) insomnia guideline.
- An NMPA suvorexant approval.

## Blocked URLs (open in Chrome)
- https://www.jssr.jp/data/pdf/suiminyaku-guideline.pdf (Japanese 2013 hypnotics guideline; connection refused by curl and WebFetch, maybe geo-blocked)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4793547/ and https://www.ncbi.nlm.nih.gov/books/NBK159725/ (NCBI reCAPTCHA; used Europe PMC and the JAMA table instead)
- https://iris.who.int/bitstream/handle/10665/311664/9789241550536-eng.pdf (WHO under-5 PDF returned HTML)
- ICD-11 browser (icd.who.int) needs JavaScript; the API needs a token
- Respir Investig full text for the Japanese SAS 2020 guideline (ScienceDirect, not tried; only the abstract was read)
- nk.jiho.jp (paywalled; MHLW 2018 benzodiazepine 12-month Q&A)

## Open questions
- [ ] Check the Japan FY2026 CPAP AHI cut-offs (15 / 30) in the MHLW 告示/通知. Does the home-test route still exist?
- [ ] Read the Japan SAS 2020 full text for CPAP, oral appliance and home-test grades.
- [ ] Read the Japanese 2013 hypnotics guideline (blocked) for tapering steps and grades.
- [ ] Is suvorexant "Strong" in the Korean 2020 guideline a table error?
- [ ] Check the China CSRS 2025 drug tiers against the original guideline. The text was taken from a two-column PDF of an interpretation article.
- [ ] Prescription vs over-the-counter status of melatonin in India; Japan personal-import rules.
- [ ] Insomnia wording in the WHO mhGAP 2023 "conditions related to stress" module (was the 2013 wording kept?).
