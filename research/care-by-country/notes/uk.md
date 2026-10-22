# UK (and Ireland): findings

36 rows in `uk.json`: 24 guideline, 6 pathway, 6 coverage. 22 insomnia, 11 OSA, 1 narcolepsy, 1 RLS, 1 waiting times.

## Main points
- **England has no full NICE clinical guideline on insomnia.** The national layer is pieced together from four sources: CKS (blocked, not read), TA77 (2004, last reviewed 2010, stale but still live), TA922 (daridorexant, 2023) and HTG624/MTG70 (Sleepio, 2022). The BAP 2019 consensus fills the clinical gaps, and NICE itself cites it as the pathway.
- **Time limits disagree.**
  - The UK licences (zopiclone, zolpidem, temazepam) say no more than 4 weeks, including the taper.
  - Ireland's HSE says "a few days to two weeks".
  - BAP 2019 says evidence "does not suggest there is an unfavourable risk/benefit transition at 3–4 weeks", and allows long-term use "as clinically indicated".
  - NICE TA922 approves daridorexant for long-term use, with a review within 3 months.
- **TA922 restricts daridorexant to people for whom CBT-I has failed or isn't available.** The drug costs £1.40/day, and the NHS must fund it within 3 months. Scotland's SMC (Apr 2024) applies the same restriction.
- **Melatonin is prescription-only in the UK** (Circadin SmPC). It is licensed for people aged 55 or over, at 2 mg for up to 13 weeks. BAP says to try it first when a hypnotic is needed in the over-55s (grade B).
- **MHRA added stronger addiction, dependence and withdrawal warnings in Jan 2026** for Z-drugs, benzodiazepines and gabapentinoids. Prescribers should agree a plan for stopping before starting treatment.
- **PHE 2019 figures (England, 2017-18):** 1.4M adults were dispensed benzodiazepines and 1.0M Z-drugs. 120k and 100k respectively had prescriptions continuously from 2015 to 2018.
- **OSA (NG202, 2021):**
  - Diagnosis: home respiratory polygraphy first, oximetry if polygraphy is hard to get, polysomnography only as a fallback.
  - CPAP: fixed-level is the default, with auto-CPAP the exception. CPAP is offered for moderate/severe OSA, and for mild OSA with symptoms.
  - Mouth splint (MAS) is second-line. Tonsillectomy if BMI is under 35.
  - Hypoglossal nerve stimulation is still "special arrangements only" (IPG598, 2017, now HTG455).
  - NICE did not recommend pitolisant or solriamfetol for leftover sleepiness in OSA (TA776/777).
- **Tirzepatide:** NICE has no OSA-indication appraisal (as of Oct 2026). OSA is instead one of 5 conditions that count toward eligibility in NHS England's phased tirzepatide-for-obesity rollout (TA1026).
- **CPAP adherence is enforced through driving licences, not funding.** The DVLA requires treatment adherence before relicensing drivers with moderate/severe OSA, reviewed every 3 years for car drivers and annually for bus/lorry drivers. I found no NHS rule that makes CPAP funding depend on adherence, unlike Medicare in the US.
- **Pathways:**
  - Scotland: NHS inform links straight to free Sleepio, no GP needed.
  - England: access to Sleepio depends on local commissioning.
  - England waits: legal right to consultant-led treatment within 18 weeks; diagnostic tests within 6 weeks (pledge).
  - NG202 lists who gets priority sleep-service assessment (vocational drivers, safety-critical jobs, unstable heart disease, pregnancy, before major surgery, NAION) but sets no time target.
- **Narcolepsy:** there is no NICE clinical guideline. TA758 makes solriamfetol third-line, after modafinil and then dexamfetamine or methylphenidate.
- **Ireland:** the only national document found is the HSE MMP BZRA guidance (v1.1, 2021). I found no Irish OSA or insomnia clinical guideline.

## Surprises / conflicts of interest
- BAP 2019 declares no conflicts of interest. But co-author Colin Espie is listed with a Big Health (maker of Sleepio) affiliation on PubMed (PMID 34246110). Also, the cost study behind NICE's Sleepio guidance (Sampson 2022, PMID 34862166) has a Big Health co-author. Worth flagging.
- TA77 is 22 years old and still the national Z-drug appraisal. It says to pick the cheapest of zolpidem, zopiclone and the short-acting benzodiazepines.

## Blocked (lead to open from a UK IP / Chrome)
- https://cks.nice.org.uk/topics/insomnia/management/managing-insomnia/ (UK-only, 403). Needed for exact hypnotic course length, melatonin wording and referral criteria.
- https://cks.nice.org.uk/topics/restless-legs-syndrome/ (UK-only, 403)
- https://bnf.nice.org.uk/treatment-summaries/hypnotics-and-anxiolytics/ (UK-only, 403). Has the CSM benzodiazepine advice and melatonin legal status.
- https://www.england.nhs.uk/statistics/statistical-work-areas/diagnostics-waiting-times-and-activity/ (bot-blocked, 202). Needed to confirm sleep studies are in DM01.
- NHS Talking Therapies manual (england.nhs.uk): not read, so its position on insomnia is unknown.
- Original HSE BZRA page now returns 404. I read the PDF from the drugsandalcohol.ie repository copy instead.

## Open questions
- [ ] CKS insomnia exact wording (a secondary source says 3–7 day Z-drug course; not verified)
- [ ] Are sleep studies one of the DM01 6-week diagnostic tests?
- [ ] Year Sleepio became free nationally in Scotland
- [ ] Who funds mouth splints (MAS) on the NHS (dental vs sleep service)
- [ ] Royal College of Psychiatrists' role in the 2019 PHE review (not checked)
