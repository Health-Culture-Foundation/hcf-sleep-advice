# Sleep medicine care by country

How doctors are told to treat sleep problems in different countries, which drugs
are allowed, who does what, and who pays. Plus: has anyone already compared this?

**Status: draft research, 21 October 2026. Nothing here has been checked by a person yet.**
**Read the write-up:** https://vivwebsolutions.github.io/hcf-sleep-advice/ (public GitHub Pages site, published from the `gh-pages` branch; source in [`site/`](site/). The repo itself stays private.)
Tracking issue: [#3](https://github.com/vivwebsolutions/hcf-sleep-advice/issues/3).
Context: [vivwebsolutions/health-glossary#30](https://github.com/vivwebsolutions/health-glossary/issues/30)
(Open Health Communication Declaration). Everyday sleep advice from AASM, ACP, ESRS,
NHS, CDC and NSF is in the separate lit search (`research/lit-search-2026-10/`, PR #2).

## Short answer

- **Nobody has published a thorough, current, cross-country comparison of sleep
  guidelines down to the level of individual drugs.** What exists are quality scores
  of guidelines (which don't compare what they say), small recommendation comparisons,
  or one-drug-class reviews. None is open data. ([details](#what-has-already-been-published))
- **Pathways and payment rules are an even bigger gap.** Only one multi-country survey
  of OSA care exists (European sleep centres, 2011 and 2022). For insomnia, nobody has
  compared who delivers CBT-I, who pays for it, or how long people wait.
- **The countries agree on one thing:** CBT-I (a short course of talking therapy for
  insomnia) comes first. Every guideline found says so. India's adds that long-term
  pills are acceptable when no therapist is available.
- **They disagree on almost every drug,** on how long pills may be taken (from "a few
  days to two weeks" to "as clinically indicated"), on melatonin (supplement, pharmacy
  product, prescription medicine or banned in supplements), and on how strict payers
  are about CPAP use.
- **Much of the guidance is old or closed.** The main US drug guideline is from 2017 and
  covers only one of the three new orexin drugs. France's insomnia guidance is from
  2006. The UK's main GP guide to insomnia (NICE CKS) can only be read from inside the UK
  and is licensed content that may not be mined.

## What's here

| File | What it is |
|---|---|
| [`comparison.json`](comparison.json) | **312 rows**, one per country × condition × recommendation. 243 guideline, 30 pathway, 39 coverage rows. 31 countries or bodies. |
| [`existing-comparisons.json`](existing-comparisons.json) | **49 published items** that compare guidelines, pathways or drug use across countries, with how thorough each is. |
| [`notes/`](notes/) | Each research area's findings note (main differences, surprises, blocked pages, open questions) and its raw rows. |
| [`notes/pmid-verification.txt`](notes/pmid-verification.txt) | Every PMID (155) re-checked against PubMed on 21 Oct 2026. |
| [`scripts/`](scripts/) | `merge.py` builds `comparison.json` from the notes; `enrich.py` then adds the code and standard-named fields from the hand-checked tables in [`scripts/codes/`](scripts/codes/); `drug_codes.py` rebuilds the drug table; `verify.py` re-checks PMIDs. |

### Row format (`comparison.json`)

| Field | Meaning |
|---|---|
| `layer` | `guideline` (what to do), `pathway` (who does it, in what order, where), `coverage` (what the payer pays for, and on what terms) |
| `country`, `jurisdiction` | Country, or `Europe`, `International`, `WHO`. `jurisdiction` names a region or programme (e.g. "Ontario Assistive Devices Program") |
| `body`, `guidelineTitle`, `guidelineYear`, `status` | Who said it, where, when, and whether it is current, under revision or stale (over 5 years without update) |
| `condition`, `decision` | e.g. `chronic insomnia` / `orexin antagonists`, `obstructive sleep apnea` / `CPAP adherence requirement` |
| `recommendation` | Close to the source wording; quotes are exact. Non-English sources quote the original plus a translation |
| `direction`, `strength` | recommend / suggest / suggest against / recommend against / no recommendation / regulatory fact; strength in the body's own grading |
| `drugs` | Drug names covered by the row |
| `citation` | authors, title, journal, year, PMID, DOI, URL |
| `freeToRead`, `freeUrl`, `whatWasRead` | Whether a reader can get it free, and whether we read the full text, abstract, web page or a secondary source |
| `conflictsOfInterest` | What the source states |
| `numbersToVerify` | Every number a person should check before it is used |
| `notes`, `researchFile` | Anything else worth knowing; which note in `notes/` the row came from |

**Added fields** (all optional; `null` means "not stated" or "not confirmed", never "no").
Names follow GRADE, HL7 EBMonFHIR and FHIR PlanDefinition, as proposed in
[`notes/formats.md`](notes/formats.md#recommendation-for-comparisonjson). `enrich.py`
fills them; it never changes the fields above.

| Field | Meaning | Maps to |
|---|---|---|
| `countryCode`, `regionCode` | ISO 3166-1 alpha-2 (`GB` for the UK) and ISO 3166-2 (`GB-ENG`, `GB-SCT`, `CA-ON`, `AU-QLD`). `null` for Europe, EU, International, WHO | `PlanDefinition.jurisdiction` |
| `conditionCodes` | `{icd11, icd11Title, icd11Uri}`: ICD-11 MMS code, WHO title and URI, checked in the WHO browser (2026-01 release): chronic insomnia `7A00`, OSA and pediatric OSA `7A41`, narcolepsy `7A20`, restless legs `7A80`. `null` for pediatric insomnia (7A00 or 7A01 depends on the row), circadian disorders (rows span 7A60-7A65) and other | `PlanDefinition.subject` |
| `drugCodes` | One `{name, atc, rxnorm}` per name in `drugs`. ATC (bare code only; WHOCC material, see below) from the WHO index; class names get an ATC group only when one group matches exactly (Z-drugs `N05CF`). RxNorm only for an exact single-ingredient match. Reasons and other codes per name: [`scripts/codes/drug-codes.json`](scripts/codes/drug-codes.json) | `ActivityDefinition.productCodeableConcept` |
| `strengthGrade` | `strong` / `conditional` only when the guideline uses GRADE (or GRADE's strong/weak words) and the row has one strength; `non-GRADE system` for NICE wording, letters, levels and other systems (never mapped to strong); `not graded` for rules, statements and consensus; `null` if the grade was not seen or the row mixes strengths | CPG `strengthOfRecommendation` |
| `certaintyOfEvidence` | high / moderate / low / very low, only when the row states one level for the whole row | CPG `qualityOfEvidence` |
| `gradingSystem` | Which system the `strength` text comes from, e.g. `GRADE`, `NICE wording (offer / consider)`, `ESRS 2023 letter grades` | `RecommendationJustification` rating system |
| `performer`, `setting` | Pathway and coverage rows: who carries out the decision (GP, sleep physician, dentist...) and where (primary care, sleep clinic, home, online...) | `action.participant`, `useContext` |
| `step`, `after` | Order in a stepped route: step number, and what must come (or fail) first | `action.relatedAction` |
| `target` | List of `{measure, comparator, value, unit}`: waiting-time standards, CPAP-use thresholds, licence review intervals. Every value is also in `numbersToVerify` | `PlanDefinition.goal.target` |
| `payer`, `program`, `ruleType` | Who pays, under which scheme, and what kind of rule: eligibility, adherence, prior authorisation, reimbursement, prescribing limit, prescriber requirement, regulatory status, restricted distribution | none (HCF's own) |

**Licences of the codes.** ATC codes are WHOCC material, excluded from the CC BY 4.0
licence (attribution: WHO Collaborating Centre for Drug Statistics Methodology, ATC/DDD
Index, https://atcddd.fhi.no/atc_ddd_index/). Its terms ban commercial copying and
"changing or manipulating the material", so only bare codes are stored (no ATC names,
hierarchy or DDDs), and **ATC must stay out of any open release, public repo or public
site until WHOCC replies**. ICD-11 codes are WHO material under CC BY-ND 3.0 IGO; its
licence asks that stored codes carry code, title and URI, which `conditionCodes` does.
See [LICENSE](../../LICENSE).

Strength mapping, row by row: [`scripts/codes/strength-map.json`](scripts/codes/strength-map.json).
Pathway and coverage fields, row by row: [`scripts/codes/pathway-coverage.json`](scripts/codes/pathway-coverage.json).

## Insomnia: country × key decisions

"CBT-I" = cognitive behavioural therapy for insomnia. "Z-drugs" = zolpidem, zopiclone,
eszopiclone, zaleplon. "Orexin drugs" = suvorexant, lemborexant, daridorexant.
Dashes mean the guideline we read didn't address it, or we didn't capture it.

| Country / body | Main guidance (year) | CBT-I first? | Time limit on benzodiazepines / Z-drugs | Orexin drugs | Trazodone / low-dose antidepressants | Melatonin for adults |
|---|---|---|---|---|---|---|
| **US**: AASM | Drugs 2017 (stale); behavioural 2021; CBT-I + drug 2026 | Yes (strong) | No week cap found | Suvorexant: weak for. Lemborexant, daridorexant: not graded | Trazodone: suggest against. Low-dose doxepin: weak for | Sold as a supplement. Suggest against for insomnia |
| **US**: VA/DoD | 2025 | Yes (strong) | — | Suggest all three | Trazodone: suggest against | Suggest against |
| **US**: ACP | 2016 (ACP lists it as inactive) | Yes (strong) | "Short-term", by shared decision | — | — | — |
| **UK**: NICE / BAP | TA922 daridorexant 2023; Sleepio 2022; TA77 Z-drugs 2004; BAP 2019. CKS not open | Yes | Licences: 4 weeks including taper. BAP: long-term "as clinically indicated" | Daridorexant if CBT-I tried or unavailable; review within 3 months | — | Prescription only. 2 mg slow-release, age 55+, up to 13 weeks. BAP: try first over 55 |
| **Ireland**: HSE | 2021 | — | "A few days to two weeks" | — | — | — |
| **Europe**: ESRS | 2023 | Yes (A), in person or digital | 4 weeks or less (A) | Up to 3 months (A) | Low-dose antidepressants short-term (B) | Fast-release: no (A). Slow-release, over 55, up to 3 months (B) |
| **Germany**: DGSM S3 | 2025 (read via a press summary) | Yes | As a rule 4 weeks max | No recommendation for long-term use, but the payer covers daridorexant past 4 weeks | Short-term only | Licensed 55+, no recommendation |
| **France**: HAS / ANSM | HAS 2006 (stale) + ANSM rule | Yes | 4 weeks including taper (law) | — | "Unproven" (2006) | Prescription medicine; low-dose supplements allowed |
| **Netherlands**: NHG | 2024 | Yes | No pills for persistent insomnia; one short course of 5–10 tablets for short-term insomnia | Not mentioned | Recommend against (amitriptyline, mirtazapine); strong against quetiapine | Recommend against |
| **Denmark** | 2019 | — | Usually 1–2 weeks at first | — | — | Banned in supplements |
| **Norway** | 2021 | — | "Maximum four weeks" | — | — | — |
| **Canada** | Ontario CEP tool 2017; deprescribing guideline 2018 | Yes | Offer tapering after more than 4 weeks | Approved; national drug assessment agency (CDA-AMC) says do not reimburse | Doxepin called safest in older adults (CEP) | Over the counter (Natural Health Product) |
| **Australia** | Joint position statement 2026 | Yes | 2–4 weeks | "Generally only" for chronic insomnia; not subsidised (PBS) | Advises against antidepressants | Pharmacist-only for 55+ (2 mg slow-release); up to 13 weeks |
| **New Zealand**: bpac | 2017 | Non-drug preferred | Max 4 weeks "but often less" | — | — | Pharmacy-only for all adults since Oct 2025 |
| **Brazil**: ABS | 2023 (heavy industry ties) | Yes | Zolpidem max 4 weeks. Benzodiazepines not recommended | All three recommended, though none confirmed on sale in Brazil | Trazodone and doxepin recommended | Not recommended. Supplement capped at 0.21 mg/day |
| **China**: CSRS | 2025 | Yes | — | Top tier, alongside short-acting Z-drugs | Third tier | Melatonin-type drugs second tier. Full herbal medicine section |
| **Japan** | Hypnotics guideline 2013 (stale) | Built around stopping pills | Payer cuts fees for 3+ hypnotics, or 12+ months of one benzodiazepine | Approved: suvorexant 2014, lemborexant 2020, daridorexant 2024 | — | Approved for children only |
| **South Korea** | 2020 | Yes (strong) | Regulator: up to 4 weeks | Suvorexant graded "Strong" though not used in Korea (likely error) | Trazodone: weak for | Fast-release: no. Slow-release 55+: consider |
| **India**: IPS | 2017 | Preferred | Long-term use allowed if CBT-I unavailable | — | — | Not a hypnotic |
| **WHO** | None | Only acute insomnia after trauma (2013): relaxation, sleep hygiene, no benzodiazepines | — | — | — | — |

## Sleep apnea (OSA): country × key decisions

AHI = breathing pauses per hour of sleep. HSAT = home sleep apnea test. PSG = overnight
lab study.

| Country | Home test or lab? | CPAP: what the payer demands | Oral appliance (mouth splint) | Tirzepatide / GLP-1 | Waiting-time standard |
|---|---|---|---|---|---|
| **US** | AASM 2017: PSG or HSAT for uncomplicated adults (strong) | Medicare: "≥4 hours per night on 70% of nights during a consecutive thirty (30) day period anytime during the first three (3) months" | AASM: if CPAP fails or not wanted. VA/DoD 2025: equal to CPAP for mild–moderate | FDA approved 20 Dec 2024. AASM: ungraded; "not as a replacement for PAP" | — |
| **UK**: NICE NG202 2021 | Home respiratory polygraphy first | No NHS adherence rule found. The driving licence agency (DVLA) enforces use for drivers | Second-line | No NICE OSA appraisal. OSA counts toward obesity-drug eligibility | 18 weeks to treatment; 6-week diagnostic pledge |
| **Germany** | Payer rule: home polygraphy first; PSG only if unclear. CPAP started in the lab over 2 nights | No hours rule found | Paid only after CPAP fails, though the guideline calls it first-line | — | — |
| **France** | Clinical guideline 2010 (stale). Payer rules lead | AHI ≥30 + 3 symptoms (or 15–29 with severe sleepiness or serious illness). At least 112 hours per 28 days | Must be considered first for AHI 15–29 | — | — |
| **Europe**: ERS / EU | ERS 2021: all non-CPAP advice conditional, low-quality evidence | EU law: drivers with OSA reviewed every 3 years (cars), yearly (lorries, buses) | Conditional | Not mentioned | — |
| **Canada**: CTS 2011 (stale) | Lab PSG is standard; home test if moderate–high pretest probability | Ontario pays 75% of the device; no adherence rule | — | — | Severe or safety-critical: 4 weeks; everyone: 6 months |
| **Australia** | GP refers; a specialist approves a home study without seeing the patient if STOP-Bang ≥3 (or OSA50 ≥5, or Berlin high risk) plus Epworth ≥8 | Medicare pays for studies, not devices. Queensland loan: 2-month trial averaging ≥4 h/night | — | — | — |
| **Brazil** | Home test for high-risk patients (2022) | Public system (SUS) has no OSA protocol; CPAP on no list | — | — | — |
| **Argentina** | Home polygraphy "comparable" to lab (Evidence A) | — | — | — | — |
| **China**: CTS 2025 | Lab PSG gold standard (1A); home test for moderate–severe uncomplicated cases | None found | — | Add-on for obese moderate–severe OSA (1A) | — |
| **Japan** | Coverage needs PSG findings | Payment stops only if use averaged under 1 h/day in every one of the last 3 months. AHI cut-offs may have dropped to 15/30 in 2026 (unverified) | — | — | — |
| **South Korea** | — | Since July 2018: ≥4 h on ≥70% of 30 nights in a row, within the first 90 days | — | — | — |
| **India**: INOSA 2014 (stale) | Home test only after a full sleep evaluation | Mostly out of pocket (unverified) | — | — | — |

## Other conditions

- **Restless legs: the sharpest split.** The US (AASM 2025) now *suggests against*
  standard use of dopamine agonists (pramipexole, ropinirole, rotigotine, levodopa),
  which can make symptoms worse over time. It recommends gabapentin-type drugs and IV iron.
  Europe's only formal guideline (EFNS/ENS/ESRS 2012) still rates dopamine agonists
  "Level A" and has not been updated. The World Sleep Society endorsed the US guideline
  only "with caveats" because of "regional disagreement". Italy (2026) has switched to the
  US position. No RLS guideline was found for Japan, Korea or China.
- **Narcolepsy:** the US and European 2021 guidelines agree (modafinil, pitolisant,
  sodium oxybate, solriamfetol all strong). The split is in who pays: NHS England uses
  solriamfetol only after modafinil and then a stimulant have failed (TA758, read
  directly), and sodium oxybate in children only as a third-line option. The EU limits
  modafinil to narcolepsy (2010), while AASM still recommends it for idiopathic hypersomnia.
- **Melatonin in children:** sold as a supplement in the US (AASM 2022 says see a
  clinician first). Prescription-only licensed products in the EU, Australia and Japan.
  Denmark (2023): "should never be the first choice" in otherwise healthy children.
- **Children's sleep apnea testing:** China won't diagnose without a lab study. Canada
  (2026) is the first to accept home tests (healthy children over 5, where lab studies
  aren't available). France (2023) needs no sleep study if there are two or more night
  symptoms.
- **Circadian rhythm disorders:** the only formal guideline is AASM 2015 (stale); all but
  one recommendation is weak.

## Pathways: who does what, in what order, and who pays

The guideline says *what*. The pathway and the payer often decide what actually happens.
69 rows in `comparison.json` have `layer: pathway` or `coverage`.

**Payers sometimes overrule guidelines:**
- Germany's S3 guideline makes no long-term recommendation for orexin drugs, but the
  national payer committee (G-BA, 2023) pays for daridorexant past the usual 4-week cap.
  The same guideline calls mouth splints a first-line option for OSA, but the payer covers
  them only after CPAP fails.
- In France and Japan, OSA care is shaped more by payment rules than by (old) clinical
  guidelines.
- Canada approved two orexin drugs, but its national drug assessment agency advises
  public plans not to pay for either.

**CPAP adherence rules range widely** (hours of use needed to keep coverage):
US Medicare and South Korea: ≥4 h on 70% of nights in a 30-day window, early on. France:
≥112 h per 28 days, checked continuously. Queensland: a 2-month trial averaging ≥4 h/night.
Japan: payment stops only below 1 h/day for 3 months in a row. England, Ontario: no
adherence rule for funding found.

**Insomnia stepped care and who pays for CBT-I:**
- Germany pays for three insomnia apps on prescription (DiGA): about €225–241, no
  co-payment.
- Scotland links people straight to free digital CBT-I (Sleepio) with no GP visit.
  England's access depends on the local NHS commissioner.
- Australia counts insomnia toward up to 10 subsidised psychology sessions a year
  (Medicare Better Access).
- US Medicare pays for FDA-cleared digital therapy (codes G0552–G0554) only alongside
  clinician-led care. The VA has trained its own therapists in CBT-I since about 2011–12.
- Canada: no public CBT-I coverage found.
- The Netherlands names guided online CBT-I as a step in its "lightest suitable form
  first" model.

**Who you see first for OSA:** in the Netherlands the GP refers and does no testing. In
Australia the GP screens and a specialist approves a home test without seeing the
patient. In the US any treating practitioner can order a test and CPAP, and an equipment
supplier delivers it.

**Waiting-time standards:** only Canada (CTS 2011) sets one for sleep: 4 weeks for
severe or safety-critical cases, 6 months for everyone. England's general 18-week rule
applies.

**Regional pathways we could not read:** Australian HealthPathways (login only), and
Canadian provincial pathways beyond Ontario.

## What has already been published

Full list with ratings: [`existing-comparisons.json`](existing-comparisons.json);
verdict note: [`notes/existing-comparisons.md`](notes/existing-comparisons.md).

| Kind | Best examples | How thorough |
|---|---|---|
| Quality scores of guidelines (AGREE II) | Insomnia: Zhu 2022, 26 guidelines. Adult OSA: Xu 2024, 44 guidelines. Sleep surgery: 22 guidelines, 8 countries | Score how well each guideline was *made*, not what it *says*. Mostly paywalled |
| Recommendation comparisons | Seow 2022, 10 insomnia guidelines: "diverged in the choice of first-line pharmacotherapy". Brandt 2024, 113 documents (25 on insomnia), free | Seow: small, paywalled, before the 2023 European update and the orexin drugs. Brandt: thorough but benzodiazepines/Z-drugs only, search ended Oct 2023, and most authors sit on a benzodiazepine-harm non-profit |
| OSA care pathways | Fietze 2011 and 2022: 26 European countries, 36 centres (one or two per country). Home testing used by 76% of centres in 2010, 89% in 2020 | The only multi-country pathway survey. Europe only, thin per country |
| CPAP payment rules | ATS 2023 policy statement, a few paragraphs | Partial |
| Drug use by country | Ma 2023 (67 countries, to 2018), Nordic registers, OECD older-adult indicator | Strong data, but never linked to what each country's guidelines say. No orexin drugs |
| CBT-I access | Thomas 2016: 88% of 752 behavioural sleep medicine providers worldwide were in the US | Old, and the only one |
| Melatonin rules | EU-level mentions only | No country table exists |
| RLS, narcolepsy | — | No cross-guideline comparison found |

**Verdict:** a real gap. Nothing published covers several countries *and* several
conditions *and* individual drugs, with pathways and payment rules, kept current, open
and machine-readable. Some insomnia overviews do exist, but most are written by authors
with ties to the maker of daridorexant (Idorsia). The items above can seed and
cross-check rows (Brandt 2024, Seow 2022, Fietze 2022, McNicholas 2025 on driving rules),
and should be credited.

## Is there a standard format for guidelines and pathways?

Full note: [`notes/formats.md`](notes/formats.md) (36 standards in [`notes/formats.json`](notes/formats.json)).

**Yes, several, but none was built for comparing countries.**

- **WHO SMART Guidelines** sets out five steps from a written guideline to software:
  L1 narrative, L2 "Digital Adaptation Kit" (workflows and decision tables), L3 a
  machine-readable FHIR version, L4 software, L5 AI-tuned. There are 10 kits (antenatal
  care, HIV, TB, immunisation and others). **None covers sleep or mental health.** An
  HCF row sits between L1 and L2.
- **HL7 FHIR** is the main modern health-data standard. Its guideline rulebook
  (CPG-on-FHIR, v2.0.0, trial use, 2024) has slots for a recommendation's direction,
  strength and quality of evidence, and a separate "pathway" type. The newer
  **EBMonFHIR** recommendation profiles are the closest match to an HCF row, but are
  still a draft (ballot, March 2025).
- **GRADE** supplies the words most guideline panels use: for or against, strong or
  conditional, and high to very low certainty. MAGICapp stores GRADE guidelines as
  structured data, but it is commercial.
- **Reporting checklists** (RIGHT, AGREE II, GIN) are not data formats, but they list
  the guideline-level facts worth recording: funding, conflicts of interest, updating.
- **Pathways:** clear definitions exist (European Pathway Association), and BPMN
  flowcharts can draw one country's route, but **there is no shared data format for
  pathways**. Map of Medicine, a commercial pathway library, was shut down in 2018 and
  its content went with it.
- **Payer rules:** no country-neutral format. The US has machine-readable Medicare
  coverage files and real-time payer standards (Da Vinci), US-only.
- **Codes:** ICD-11 for conditions (chronic insomnia 7A00); ATC for drugs (zolpidem
  N05CF02, suvorexant N05CJ01, daridorexant N05CJ03).

**Decision (reversible):** keep `comparison.json` as plain JSON, but add optional fields
named after GRADE / EBMonFHIR / FHIR terms: country codes, ICD-11 and ATC codes,
normalised strength and certainty, grading system, and, for pathway rows, who does it,
where, in what order, and any numeric target (e.g. hours of CPAP use). Mapping table:
[`notes/formats.md`](notes/formats.md#recommendation-for-comparisonjson). Don't
produce FHIR until a partner asks for it. Done on 22 Oct 2026 (see the added fields under Row format).

## Who owns the guidance doctors actually use

Full note: [`notes/agilio-closed-guidance.md`](notes/agilio-closed-guidance.md)
(17 resources in [`notes/agilio-closed-guidance.json`](notes/agilio-closed-guidance.json)).

**The UK's main GP guide (NICE Clinical Knowledge Summaries, CKS) is paid for by NICE
but owned by a private-equity-held company.**
- CKS began as PRODIGY, an NHS-funded project at Newcastle University in the 1990s.
  Since September 2012 NICE has paid Clarity Informatics to write it.
- Clarity was bought in April 2021 by Agilio Software, a UK healthcare software group.
  Agilio's founding investor sold it in February 2024 to funds advised by Five Arrows
  (Rothschild & Co) and TA Associates.
- The last contract was about £1.32 million for April 2023 to April 2026, with one bid
  received. The two official notices disagree slightly (£1,320,000 vs £1,323,000).
- Agilio's page says: "The content within CKS is the intellectual property of Agilio."
  NICE excludes CKS from its open licence. It is readable only from the UK, and
  scraping and mining are banned.
- Outside the UK the same content is sold by subscription ("Agilio Prodigy", and through
  the Royal Pharmaceutical Society's publishing arm). Its topic list includes insomnia,
  sleep apnea and restless legs.

**The BNF (the UK drug reference) works the same way.** It is owned by the Royal
Pharmaceutical Society, the BMJ and the Royal College of Paediatrics and Child Health.
NICE pays £15.16 million for 2021–2033 for UK access, awarded without competition
"due to IPR ownership".

**This is a pattern.** The guidance doctors actually use day to day is mostly paid or
login-only: UpToDate, BMJ Best Practice, DynaMed, Australia's Therapeutic Guidelines,
HealthPathways. Some governments buy national licences, which makes the content free to
use there but never open. Those licences can lapse: Norway dropped BMJ Best Practice on
1 April 2026 and deleted its translated patient leaflets the same day. Society guidelines
are more often free to read (Netherlands NHG, Germany AWMF, Japan Minds, NICE), but
machine reuse is increasingly restricted. AWMF reserves its texts against text mining and
AI. NICE's own licence covers the UK only and excludes AI use. Its API costs £60,000 a
year outside the UK.

**For the Declaration:** the public pays twice, once for the evidence and the experts,
then again to license the summary back. And people outside the paying country can't see
it at all. We found studies on paywalled specialty guidelines (dermatology: 34 of 226
behind a paywall), but **none on how closed GP-level guidance is.** That's another gap
HCF could fill.

## Conflicts of interest worth knowing

- The UK's BAP 2019 consensus declares no conflicts, but a co-author is listed with the
  maker of Sleepio on PubMed; the cost study behind NICE's Sleepio guidance also has a
  co-author from that company.
- Brazil 2023: many pharma ties on the panel, including daridorexant's Latin American
  partner.
- Japan's 2020 sleep apnea guideline: heavy panel ties to CPAP makers.
- AASM RLS 2025: the chair consulted for the maker of IV ferric carboxymaltose, which the
  guideline strongly recommends.
- The tirzepatide OSA trials (SURMOUNT-OSA) were funded by Lilly.
- European deprescribing consensus (Palagini 2025): authors report Idorsia ties; it
  favours daridorexant.

## Stale guidance (over 5 years without update)

AASM insomnia drugs (2017), AASM PAP (2019) and oral appliance (2015), ACP insomnia (2016)
and OSA (2013/2014, all listed by ACP as inactive), NICE TA77 Z-drugs (2004), BAP (2019),
HAS insomnia (2006), French OSA guideline (2010), Canada CTS OSA (2011), Japan hypnotics
(2013), India INOSA (2014), EFNS RLS (2012), AASM circadian (2015), AAP children's OSA
(2012), ERS children's OSA (2016/2017).

## Numbers to check before use

Every row lists its own in `numbersToVerify`. The ones most likely to be quoted:
- [ ] Medicare CPAP rule wording (LCD L33718) and Korea's 21-of-30-nights rule
- [ ] Japan FY2026 CPAP AHI cut-offs (15/30 vs 20/40). Read from a commercial annotated
      copy, not the ministry text
- [ ] France ≥112 h per 28 days CPAP rule and the March 2026 HAS proposals (not yet law?)
- [ ] Germany DiGA prices (€241.25 HelloBetter, €224.99 somnio, €236.00 somnovia)
- [ ] England 2017–18: 1.4M adults on benzodiazepines, 1.0M on Z-drugs (PHE 2019)
- [ ] Australia MBS STOP-Bang cut-off ≥3 (changed March 2021; many sources still say 4)
- [ ] Fietze: home testing in 76% → 89% of European centres
- [ ] OECD benzodiazepine figures (page blocked; not verified)
- [ ] All German 2025 insomnia wording (from a pharmacy-press summary)

## Gaps in this research

- **Not read, blocked:** NICE CKS (insomnia, RLS) and BNF/BNFc: UK-only, licensed, no
  mining allowed. German S3 2025 insomnia PDF: AWMF reserves it against text mining and
  AI use, so a person should copy the grades. Finland's Käypä hoito: the site was down.
  Japan's 2013 hypnotics guideline PDF: connection refused. Australian HealthPathways:
  login only.
- **Not found:** Swedish Läkemedelsverket insomnia advice, Dutch specialist OSA guideline,
  Danish insomnia guidance, Chile, Taiwan, Singapore, Hong Kong, Turkey, a Korean adult
  OSA guideline, a Chinese primary-care insomnia guideline, any Japanese/Korean/Chinese
  RLS guideline, a Japanese narcolepsy guideline.
- **Thin:** Italy, Spain and Switzerland (one row each, abstract only); Nordic OSA
  pathways; Medicaid; US GLP-1 coverage after 2025.
- **Mostly abstracts.** Full text was read for VA/DoD 2025, ESRS 2023, Korea 2020,
  China pediatric OSA 2020, AASM circadian 2015, ATS 2023/2024 and others noted per row.

## Open questions

- [ ] Should HCF publish this as a standalone open dataset ("sleep care by country"),
      separate from the everyday-advice dataset?
- [ ] Ask a UK clinician to read NICE CKS insomnia and RLS (exact course length,
      referral criteria, dopamine agonist position).
- [ ] Ask a German reader to copy the S3 2025 insomnia grades.
- [ ] Contact Brandt 2024 and Fietze 2022 authors about reusing their country data?
- [ ] Is the Korean 2020 "Strong" grade for suvorexant a table error?
- [ ] Has France made the March 2026 HAS CPAP proposals law?
- [ ] Has Australia's March 2026 scheduling meeting changed melatonin's status?
- [ ] Does the TGA list daridorexant?
- [ ] Add drug-use data (OECD, Nordic registers) next to each country's guidance?
- [ ] ATC licence: the WHOCC copyright notice bans "changing or manipulating the
      material". Is listing ATC codes in an openly licensed dataset allowed? Ask the
      WHO Collaborating Centre (Oslo) before an open-licence release.
- [ ] Several guidelines graded 1A-2C or "strong/weak" without the row naming GRADE
      (Canadian Thoracic Society 2011, Chinese Thoracic Society 2025, Korean 2020).
      They are recorded as `non-GRADE system` or with the system "not named". Check
      each guideline's methods section and upgrade to GRADE if it says so.

## Method

Seven research agents worked in parallel on 21 October 2026 (US; UK/Ireland; Europe;
Canada/Australia/NZ/Latin America; Asia/WHO; RLS/narcolepsy/circadian/children;
existing comparisons). Two more looked at standard formats and at who owns closed
guidance. Rules: no citation without a PMID or DOI that was looked up, or a page that was
read; numbers copied exactly; say what was read; record dates, status and conflicts of
interest; respect blocks and licence terms rather than work around them. All 117 PMIDs
in the data, plus 38 more cited in the notes, were re-checked against PubMed at the end and match; DOI-only citations were checked on
Crossref. This is a first pass by an AI and needs a person's review.
