# US: chronic insomnia and OSA in adults (slug: us)

76 rows in `us.json`: 68 guideline/regulatory, 5 coverage, 3 pathway. Every PMID was checked with E-utilities esummary: 27998379, 33164742, 41975142 (+ review 41986788), 27136449, 28162150, 30736887, 26094920, 34351848, 38912654, 24061345, 25089864, 22505869, 24412462. The VA/DoD 2019 synopsis is PMID 32066145 (checked, but superseded, so it has no row).

## Main findings
- **US bodies disagree on drugs.**
  - AASM 2017 weakly suggests 8 drugs: suvorexant, eszopiclone, zaleplon, zolpidem, triazolam, temazepam, ramelteon and low-dose doxepin. It weakly advises against 6: trazodone, tiagabine, diphenhydramine, melatonin, tryptophan and valerian.
  - VA/DoD 2025 suggests orexin antagonists (daridorexant, lemborexant, suvorexant), Z-drugs and doxepin. It suggests against benzodiazepines, trazodone, diphenhydramine and antipsychotics, and finds ramelteon "insufficient evidence".
  - So temazepam, triazolam and ramelteon get opposite or weaker verdicts depending on the body.
- **The AASM drug guideline is stale (2017) and is not being updated.** It covers no lemborexant or daridorexant. The AASM "Guidelines in Development" page (updated June 2026) lists no drug update. AASM's new guideline (April 2026) is about combining treatments: it suggests CBT-I plus a drug over a drug alone, and suggests against CBT-I plus a drug over CBT-I alone. Both are conditional with low certainty. Note that JCSM now publishes with Springer DOIs.
- **All three insomnia bodies agree:** CBT-I comes first (AASM strong, ACP strong, VA/DoD strong), and sleep hygiene alone is not a treatment.
- **ACP's insomnia guideline (2016) and OSA guidelines (2013, 2014) are listed as inactive** on ACP's own "Inactive ACP Guidelines" page. ACP treats anything 5 or more years old as no longer active. I found no update from 2024 to 2026.
- **OSA:**
  - AASM 2017 says a lab study (PSG) or a home test can diagnose uncomplicated adults (strong). A focused update is in development.
  - ACP 2014 accepted home testing only "when polysomnography is not available".
  - VA/DoD 2025 puts mandibular advancement devices level with PAP as first line for mild to moderate OSA (Event Index <30). AASM and ACP put them second.
  - VA/DoD also suggests up to 2 weeks of eszopiclone to help people get used to CPAP (unusual), and HGNS referral for people with AHI ≥15 who fail PAP.
- **Tirzepatide:**
  - FDA approved Zepbound on 20 Dec 2024 for moderate to severe OSA in adults with obesity.
  - The SURMOUNT-OSA trials (NEJM 2024, PMID 38912654) were funded by Lilly.
  - AASM has no graded guideline on it, only a statement and a 2026 fact sheet ("not as a replacement for PAP").
  - VA/DoD 2025 mentions it in its narrative, but it changed none of the recommendations.
- **Regulatory facts (all from pages I read):**
  - FDA added a boxed warning to Z-drugs for complex sleep behaviors (30 Apr 2019) and made a prior episode a contraindication.
  - FDA updated the boxed warning for all benzodiazepines (23 Sep 2020).
  - Melatonin is a dietary supplement (NCCIH page). FDA cannot approve supplements before they go on sale.
  - DEA lists daridorexant, lemborexant, suvorexant, the Z-drugs, temazepam and triazolam as Schedule IV.
- **Coverage and pathway:**
  - Medicare NCD 240.4: CPAP is covered for a 12-week trial if AHI is ≥15, or 5–14 with symptoms or comorbidity.
  - The adherence rule is in DME MAC LCD L33718, not in the NCD: "use of PAP ≥4 hours per night on 70% of nights during a consecutive thirty (30) day period anytime during the first three (3) months", with re-evaluation "no sooner than the 31st day but no later than the 91st day".
  - NCD 240.4.1 has covered home tests since 2009.
  - Any treating practitioner can order the sleep test and the PAP device. A DME supplier delivers the device and teaches its use.
  - Medicare DMHT codes G0552–G0554 pay for FDA-cleared digital therapy only alongside clinician-led behavioral care.
  - The VA has run a national CBT-I training program for non-sleep-specialist therapists since about 2011–2012.

## Surprises
- The US's main specialty drug guideline is 9 years old and silent on two of the three marketed orexin antagonists. VA/DoD is the only US body that grades them.
- ACP formally retired its own sleep guidelines (listed as inactive) and has not replaced them.
- The Medicare "4 h / 70%" rule comes from a DME contractor LCD, not the national NCD.

## Blocked or not read
- jcsm.aasm.org returned 404 for the DOI pages. The PMC HTML was CAPTCHA-blocked for curl but readable through the fetch tool.
- The 2026 combination guideline full text and conflict-of-interest statement: Springer PDF not downloadable by script (https://link.springer.com/content/pdf/10.1007/s44470-025-00038-8.pdf). Lead should open it in Chrome to get the COI.
- Not found: a primary CMS document on Part D coverage of Zepbound for OSA. That row relies on news reports.

## Open questions
- [ ] Is there a Medicare national policy for in-person CBT-I? I found none. It appears to be billed through general psychotherapy codes (not verified). Medicaid coverage by state was not researched.
- [ ] Are FDA-cleared insomnia apps (SleepioRx, Somryst) classified under 21 CFR 882.5801? This comes from a secondary source.
- [ ] What is the current LCD L33718 revision? R11 (effective 1 Jan 2024) was the latest in the history I saw.
- [ ] Has US GLP-1 coverage changed in 2025–2026 (federal pricing deals, Medicare obesity coverage)? Not researched.
- [ ] Should the AASM "Medical Therapy of OSA" practice parameter (2006, Morgenthaler) get a row? Not read.
- [ ] The VA/DoD 2019 version's drug list is not captured. The 2025 categories mark recs 9 and 10 as "New-replaced".
