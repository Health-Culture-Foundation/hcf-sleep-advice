# Standard formats for guidelines, pathways and coverage: what exists, and what HCF should map to

Research date: 2026-10-21. The full list of 36 standards, each with its source, status, licence and "what was read", is in `formats.json`.

## Short answer

Yes, standards exist, but none of them was built for comparing countries. They fall into four groups:

1. **Formats that turn a guideline into software**: WHO SMART Guidelines, HL7 FHIR Clinical Practice Guidelines (CPG-on-FHIR), and the older languages such as Arden, GLIF and PROforma. They describe *what a computer should do for one patient*.
2. **Formats for evidence and recommendations**: GRADE, MAGICapp, the GRADEpro/Cochrane Summary of Findings JSON, and EBMonFHIR. They describe *what was recommended, how strongly, and on what evidence*. This is the group closest to an HCF row.
3. **Reporting checklists**: RIGHT, AGREE II, AGREE-REX, GIN and COGS. They are not data formats, but they tell you which guideline-level facts are worth recording, such as funding, conflicts of interest and update plans.
4. **Terminologies**: ICD-11, SNOMED CT, ATC and RxNorm. These give shared codes for conditions and drugs.

Pathway and coverage standards are weaker. Pathways have a definition (from the European Pathway Association) and some drawing notations (BPMN), but no shared data format. Coverage formats are US-only: the CMS coverage database, and the Da Vinci standards, which are real-time payer plumbing rather than something you can publish.

**Recommendation:** keep `comparison.json` as plain JSON. Add about ten optional fields named after **EBMonFHIR Recommendation / FHIR PlanDefinition** terms. Use **GRADE** words for strength and certainty, **ICD-11** codes for conditions and **ATC** codes for drugs. Don't emit FHIR yet. A script can export later if anyone asks. The mapping table is at the end.

---

## 1. WHO SMART Guidelines (L1 to L5)

"SMART" stands for Standards-based, Machine-readable, Adaptive, Requirements-based, Testable. It is WHO's step-by-step route from a printed guideline to software.

The layer wording below comes from Wikipedia and healthmanagement.org, both quoting Mehl et al. 2021 (secondary sources). The Lancet paper itself was blocked (HTTP 403).

| Layer | Name | What it is (quoted) |
|---|---|---|
| L1 | Narrative | "Evidence-based recommendations in descriptive format primarily intended for human readability" |
| L2 | Operational (DAK) | "Software-neutral documentation of requirements": workflows, data elements and decision tables, collected in a **Digital Adaptation Kit** |
| L3 | Machine-readable | "Structured software-neutral specifications with coding, terminology and interoperability standards" (a FHIR implementation guide) |
| L4 | Executable | "Software that deliver the requirements through execution of static algorithms" |
| L5 | Dynamic | "Executable dynamic algorithms that are optimized with advanced analytics and training" |

**Topics with DAKs** (from the smart.who.int index, November 2025): antenatal care, family planning, postnatal care, birth defects surveillance, HIV, TB, child health in humanitarian emergencies, immunizations, self-monitoring of blood pressure in pregnancy, and infectious disease surveillance volume 1. Community health is in development.

**Sleep or mental health:** none. Neither appears in the published or upcoming lists.

**What it means for HCF:** an HCF row is an L1 fact made structured, sitting between L1 and L2. L1 also asks developers to register and uniquely identify recommendations, which supports HCF's stable row `id`s.

- Citation: Mehl G, Tunçalp Ö, Ratanaprayul N, et al. *WHO SMART guidelines: optimising country-level use of guideline recommendations in the digital age.* Lancet Digit Health 2021;3(4):e213-e216. PMID 33610488, doi:[10.1016/S2589-7500(21)00038-8](https://doi.org/10.1016/S2589-7500(21)00038-8). Read: PubMed record only (no abstract); Europe PMC lists it as CC BY.
- Pages read: [who.int SMART page](https://www.who.int/teams/digital-health-and-innovation/smart-guidelines), [smart.who.int](https://smart.who.int/), [IG starter kit](https://smart.who.int/ig-starter-kit/), [Wikipedia](https://en.wikipedia.org/wiki/WHO_SMART_guidelines) (secondary), [healthmanagement.org](https://www.healthmanagement.org/s/smart-guidelines-for-national-digital-health-systems) (secondary).

## 2. HL7 FHIR Clinical Practice Guidelines IG and EBMonFHIR

**FHIR** (Fast Healthcare Interoperability Resources) is the main modern standard for health data. Each record type is called a "resource". An **IG** (implementation guide) is a rulebook for using FHIR for one purpose.

**CPG-on-FHIR** ([hl7.org/fhir/uv/cpg](https://hl7.org/fhir/uv/cpg/)): version 2.0.0 STU2, dated 2024-11-26, built on FHIR R4. STU means "standard for trial use", so it is not yet final.

- A **recommendation** is a `PlanDefinition` profile called `CPGRecommendationDefinition` (type `eca-rule`). It has extensions for `strengthOfRecommendation`, `directionOfRecommendation` ("for or against") and `qualityOfEvidence`. Citations go in `relatedArtifact`. ([profile page](https://hl7.org/fhir/uv/cpg/StructureDefinition-cpg-recommendationdefinition.html))
- A **pathway** is `CPGPathwayDefinition`: "A pathway provides groupings of strategies to provide a longitudinal view of the guideline." ([profile page](https://hl7.org/fhir/uv/cpg/StructureDefinition-cpg-pathwaydefinition.html))
- **ActivityDefinition** describes a single action, such as "prescribe X". **Library** holds logic written in **CQL** (Clinical Quality Language, a readable rule language).
- **PlanDefinition** itself ([R5 page](https://hl7.org/fhir/R5/plandefinition.html)) is at Maturity Level 4, Trial Use. Useful elements:
  - `type`: order-set, clinical-protocol, eca-rule or workflow-definition
  - `action.participant`: who does it
  - `goal.target`: for example, a waiting-time target
  - `relatedArtifact`: citations
  - `useContext`
  - In R5, `jurisdiction` and `topic` are marked deprecated.
- **Evidence** ([R5 page](https://hl7.org/fhir/R5/evidence.html)) is at Maturity Level 1, Trial Use. It holds study results and a machine-readable certainty rating. **EvidenceVariable** defines the population, exposure and outcome.

**EBMonFHIR** (Evidence Based Medicine on FHIR, [artifacts list](https://hl7.org/fhir/uv/ebm/2025May/artifacts.html)) is still a ballot, not a standard: 1.0.0-ballot2, dated 2025-03-28. Its profiles are marked "Draft", Maturity Level 1. It has profiles for:

- `Guideline` and `Recommendation`: documents (Composition)
- `RecommendationPlan`: the action (PlanDefinition)
- `RecommendationJustification`: "the rationale, evidence, and judgments supporting a recommendation", with components for strength of recommendation, direction, net effect and judgments
- `CertaintyOfEvidence`

This is the closest existing schema to an HCF row.

- Citation: Soares A, Schilling LM, Richardson J, et al. *Making Science Computable Using Evidence-Based Medicine on Fast Healthcare Interoperability Resources: Standards Development Project.* J Med Internet Res 2024;26:e54265. PMID 38916936, doi:[10.2196/54265](https://doi.org/10.2196/54265). Read: abstract.
- Conflict of interest: the lead author (Alper) owns Computable Publishing LLC, and two co-authors are its employees.

## 3. Recommendation and evidence formats, and reporting standards

**GRADE Evidence to Decision (EtD).** A structured table that guideline panels use to move from evidence to a recommendation. GRADE recommendations have:

- a **direction**: for or against
- a **strength**: strong or conditional (also called weak)
- a **certainty of evidence**: high, moderate, low or very low

This is the vocabulary HCF should normalise to. Note that the list of EtD criteria and the four certainty levels come from general knowledge; I did not read them in this session.

- Alonso-Coello P, et al. BMJ 2016;353:i2016. PMID 27353417, doi:[10.1136/bmj.i2016](https://doi.org/10.1136/bmj.i2016). Part 2, on clinical guidelines: PMID 27365494, doi:[10.1136/bmj.i2089](https://doi.org/10.1136/bmj.i2089). Read: PubMed records only.

**MAGICapp** ([magicevidence.org/magicapp](https://magicevidence.org/magicapp/)). A web platform for writing GRADE guidelines as structured data, run by a non-profit foundation.

- The product page describes a "robust, structured data model", an API, publishing one recommendation at a time, and an audit trail.
- It is built for **living guidelines**: guidelines updated one recommendation at a time as new evidence arrives.
- Users include WHO and the Stroke Foundation (Australia).
- Licence: commercial, an 8-week free trial followed by "Negotiations".
- I found no FHIR export.
- In a trial of 181 physicians, 72% preferred MAGIC's layered format (short recommendation, then rationale, then evidence). Brandt L, et al. BMJ Open 2017;7:e011569. PMID 28188149, doi:[10.1136/bmjopen-2016-011569](https://doi.org/10.1136/bmjopen-2016-011569). Read: abstract. The authors declare MAGIC and GRADE membership.

**GRADEpro and the Cochrane Summary of Findings JSON schema.**

- GRADEpro exports evidence tables as JSON-LD ([MAGICapp help page](https://help.magicapp.org/support/solutions/articles/201000064235-upload-a-pico-using-a-gdt-gradepro-file)).
- Cochrane publishes a [JSON schema](https://assets.cochrane.org/schema/v1/sof/summary-of-findings.schema.json), described as a "Common representation of GRADE 'Summary of Findings' or 'Evidence Profile' tables for exchange between tools". Its top-level fields are ci-level, population, setting, intervention, comparator and outcomes.
- Worth using if HCF ever stores evidence tables. Not needed now.

**GIN (Guidelines International Network).**

- Its 2012 key components for trustworthy guidelines are: panel composition, decision process, conflicts of interest, objective, methods, evidence review, basis of recommendations, rating of evidence and recommendations, review, updating and funding. Qaseem A, et al. Ann Intern Med 2012. PMID 22473437, doi:[10.7326/0003-4819-156-7-201204030-00009](https://doi.org/10.7326/0003-4819-156-7-201204030-00009). Read: abstract.
- The [International Guidelines Library](https://g-i-n.net/library/international-guidelines-library) is a free registry (powered by EBSCO) with CSV and RIS export. It is useful for finding guidelines, but it does not hold recommendation-level data.

**RIGHT statement.** A 22-item reporting checklist:

| Section | Items |
|---|---|
| Basic information | 1-4 |
| Background | 5-9 |
| Evidence | 10-12 |
| Recommendations | 13-15 |
| Review and quality assurance | 16-17 |
| Funding, and declaration and management of interests | 18-19 |
| Other | 20-22 |

Chen Y, et al. Ann Intern Med 2017;166:128-132. PMID 27893062, doi:[10.7326/M16-1565](https://doi.org/10.7326/M16-1565). Read: abstract. [right-statement.org](https://www.right-statement.org/)

**AGREE II and AGREE-REX.** Tools for scoring guideline quality.

- **AGREE II** has 23 items. Brouwers MC, et al. J Clin Epidemiol 2010. PMID 20656455, doi:[10.1016/j.jclinepi.2010.07.001](https://doi.org/10.1016/j.jclinepi.2010.07.001).
- **AGREE-REX** scores the recommendations themselves. Across 161 guidelines the mean score was 4.23 out of 7. The lowest scores were for policy values (3.44), local applicability (3.56) and resources (3.49). Florez ID, et al. Implement Sci 2020;15:79. PMID 32948216, doi:[10.1186/s13012-020-01036-5](https://doi.org/10.1186/s13012-020-01036-5). Read: abstract.
- Those weak spots, local fit and resources, are what HCF's pathway and coverage layers describe.
- [agreetrust.org](https://www.agreetrust.org/)

**COGS** (2003). An 18-topic reporting checklist that RIGHT has replaced in practice. Shiffman RN, et al. Ann Intern Med 2003. PMID 13679327, doi:[10.7326/0003-4819-139-6-200309160-00013](https://doi.org/10.7326/0003-4819-139-6-200309160-00013). Read: abstract.

**GEM (Guideline Elements Model, ASTM E2210).** An XML document model with more than 100 elements. Recommendations are split into "conditionals" (if) and "imperatives" (do).

- A 2011 review found the GEM Cutter tool had been downloaded 563 times. Critics said GEM files are "not usually executable".
- Shiffman RN, et al. JAMIA 2000. PMID 10984468, doi:[10.1136/jamia.2000.0070488](https://doi.org/10.1136/jamia.2000.0070488).
- Hajizadeh N, et al. AMIA 2011. PMID 22195106 (no DOI).
- The ASTM page returned HTTP 403, so the current ASTM status is unverified.

**NICE syndication API** ([page](https://www.nice.org.uk/about/what-we-do/nice-syndication-api)).

- Delivers current NICE guidance as HTML, Atom, or NICE-specific JSON and XML.
- Only organisations can apply, and they need cyber-security certification.
- Free inside the UK. Outside the UK: £550 for an international test licence, £60,000 a year for a worldwide service licence.
- Using NICE content "to train, fine-tune or weight Generative AI or large language models is not permitted."
- The recommendations are not exposed as structured fields; they come as formatted documents.
- For HCF: link to NICE pages and quote briefly. Don't bulk-ingest.

**Not found or not researched:**

- I found no published "Guideline Recommendation ontology" in PubMed.
- I did not look into Semantic MEDLINE (a tool that extracts facts from abstracts). It is not a guideline format.

## 4. Older computer-interpretable guideline languages

- **Arden Syntax**: still alive but niche. ANSI/HL7 Arden V2.10-2014 was reaffirmed as version 2.10-2019 ([HL7 StandUps](https://standups.hl7.org/2019/07/31/publication-of-health-level-seven-arden-syntax-for-medical-logic-systems-version-2-10-2019/)). Researchers reported "Arden Syntax on FHIR" compilers in 2023 and 2024 (PMIDs 37387055, 39575797; titles only). It encodes single if-then alerts. Samwald M, et al. J Biomed Inform 2012. PMID 22342733, doi:[10.1016/j.jbi.2012.02.001](https://doi.org/10.1016/j.jbi.2012.02.001).
- **GLIF3**: research model from 2004, at three levels (flowchart, computable, implementable). PMID 15196480, doi:[10.1016/j.jbi.2004.04.002](https://doi.org/10.1016/j.jbi.2004.04.002).
- **PROforma**: from 2003, commercialised as Arezzo. PMID 12807812, doi:[10.1197/jamia.M1264](https://doi.org/10.1197/jamia.M1264). The [Deontics](https://deontics.com/) site now sells "Intelligent Treatment Pathways" but does not mention PROforma.
- **SAGE**: project overview from 2007. PMID 17600098, doi:[10.1197/jamia.M2399](https://doi.org/10.1197/jamia.M2399).
- **Asbru, GUIDE, EON, PRODIGY**: compared with GLIF and PROforma in Peleg 2003 (PMID 12509357, doi:[10.1197/jamia.m1135](https://doi.org/10.1197/jamia.m1135)). Some participants then pursued standardisation "under the auspices of HL7". Peleg 2013 reviews the whole field (PMID 23806274, doi:[10.1016/j.jbi.2013.06.009](https://doi.org/10.1016/j.jbi.2013.06.009)). Asbru still appears in research up to 2024 (PMID 38768161).
- **Verdict:** these are research history. Their live successor is HL7 CQL plus FHIR CPG. None suits a comparison dataset.

## 5. Clinical pathway formats

- **Definitions** (use these to decide whether a row is a "pathway"):
  - The [European Pathway Association](https://e-p-a.org/care-pathways/) defines a care pathway as "a complex intervention for the mutual decision making and organisation of care processes" for "a well-defined group of patients during a well-defined period".
  - Lawal 2016's four criteria for Cochrane reviews: a structured multidisciplinary plan; translates guidelines into local structures; steps with time-frames or criteria-based progression; standardises care for one population. Lawal AK, et al. BMC Med 2016;14:35. PMID 26904977, doi:[10.1186/s12916-016-0580-z](https://doi.org/10.1186/s12916-016-0580-z).
- **BPMN, CMMN and DMN** (OMG standards for, respectively, flowcharts, flexible case management and decision tables). Promoted through **BPM+ Health**, which [bpm-plus.org](https://www.bpm-plus.org/) says is moving into HL7 as the "HL7 BPM Community" (no date given). BPMN is easy to draw but needs extensions for timing-heavy care. Iglesias N, et al. JMIR 2022. PMID 36107480, doi:[10.2196/29927](https://doi.org/10.2196/29927). Good for drawing one country's route as a diagram; overkill for storing rows.
- **openEHR Task Planning**: the [specification](https://specifications.openehr.org/releases/PROC/latest/task_planning.html) is marked **RETIRED** (PROC Release-1.7.0). Don't use it.
- **HealthPathways** ([healthpathways.info](https://www.healthpathways.info/)). Run with Streamliners NZ in Australia, New Zealand, Canada, England and Wales: "50+ health systems" and "30M+" people. It started in Canterbury, NZ, in 2008 (Goddard-Nash A, et al. Aust Health Rev 2020. PMID 32693906, doi:[10.1071/AH19214](https://doi.org/10.1071/AH19214)). Content is web pages, not a data format. Copy the facts, not the text.
- **Map of Medicine**: withdrawn. Pulse+IT (4 June 2018) reported that referral and sidebar tools were withdrawn from sale on 31 March and that the pathway map would cease on 30 June ([article](https://www.pulseit.news/?p=18729); paywalled after two paragraphs). Earlier, the RCP stopped contributing pathways ([RCP release](https://www.rcp.ac.uk/news-and-media/news-and-opinion/changes-to-map-of-medicine-and-royal-college-of-physicians-collaboration/), dated 15 July 2015). Lesson: **archive every pathway URL** (for example on the Wayback Machine).
- **CDS Hooks** ([cds-hooks.hl7.org](https://cds-hooks.hl7.org/)). An API for decision-support pop-ups inside electronic records: hooks such as patient-view and order-sign, which return "cards". STU 2.0.1; a normative ballot of 3.0.0 is dated 2025-12-15. It is plumbing, not content.

## 6. Coverage and payer rules

- **CMS Medicare Coverage Database** ([downloads](https://www.cms.gov/medicare-coverage-database/downloads/downloads.aspx), [Coverage API](https://api.coverage.cms.gov/)).
  - National and local coverage determinations, and articles, as ZIPs (MS Access and CSV with embedded HTML), updated weekly on Thursdays, plus a REST API.
  - CPT codes inside are AMA-licensed for personal, non-commercial use only.
  - For HCF: cite the NCD or LCD number and date. Don't copy CPT descriptions.
- **Da Vinci CRD** (Coverage Requirements Discovery, [IG](https://hl7.org/fhir/us/davinci-crd/), v2.2.1 STU 2.2, 2026-03-27). Lets a clinician's system ask the payer, through CDS Hooks, what that payer requires for an order.
- **Da Vinci DTR** (Documentation Templates and Rules, [IG](https://hl7.org/fhir/us/davinci-dtr/), v2.2.0 STU 2.2, 2026-03-27). "Specifies how payer rules can be executed in a provider context", using FHIR Questionnaires and CQL.
- Both are US-only and work in real time, so they are not publishable rule sets.
- **No country-neutral coverage format exists.** HCF's coverage layer will have to stay its own design. That is fine; record payer, programme, rule and source.

## 7. Terminology: which codes to use

| What | Use | Why | Licence |
|---|---|---|---|
| Conditions | **ICD-11** (primary) | Global and free, with a dedicated sleep-wake chapter (chapter 7). Chronic insomnia **7A00**, short-term insomnia **7A01** (Spiegelhalder K, et al. Nervenarzt 2025, PMID 40965652, doi:[10.1007/s00115-025-01859-x](https://doi.org/10.1007/s00115-025-01859-x), full text read). OSA **7A41** seen only in secondary web results; verify. | CC BY-ND 3.0 IGO ([WHO ICD page](https://www.who.int/standards/classifications/classification-of-diseases)). Codes can be cited. |
| Conditions (optional) | SNOMED CT | Most detailed; used inside FHIR | Free in member countries; licence through MLDS elsewhere ([snomed.org](https://www.snomed.org/get-snomed)). Keep optional. |
| Drugs | **ATC** (primary) | Used worldwide outside the US | Checked: zopiclone N05CF01, zolpidem N05CF02, zaleplon N05CF03, eszopiclone N05CF04, suvorexant N05CJ01, lemborexant N05CJ02, daridorexant N05CJ03 ([index](https://atcddd.fhi.no/atc_ddd_index/), updated 2026-01-20). The copyright notice requires attribution and bans commercial copying and changes. Probably fine for a non-commercial dataset that cites the source, but **confirm before an open-licence release**. |
| Drugs (optional) | RxNorm | US rows and US drug data | Free ([NLM](https://www.nlm.nih.gov/research/umls/rxnorm/index.html)). Checked: zolpidem RxCUI 39993, suvorexant RxCUI 1547099. |

---

## Recommendation for `comparison.json`

**Decision (reversible):** keep plain JSON, one row per country × condition × recommendation, as now. Add optional fields whose **names and allowed values follow GRADE, EBMonFHIR and FHIR PlanDefinition**. Don't adopt full FHIR now: it adds about 5 nested objects per row, and EBMonFHIR is still a ballot.

The existing `strength` text stays, verbatim, because bodies grade differently (for example "Recomendación A", "NICE: offer", "Level A"). The new normalised fields sit beside it.

| HCF field (existing / *new*) | Maps to | Notes |
|---|---|---|
| `id` | `PlanDefinition.id` / `Composition.identifier` | Keep stable. This is SMART L1's "uniquely identify recommendations". |
| `layer` = guideline | EBMonFHIR `Recommendation` + `RecommendationPlan` (PlanDefinition `type` = eca-rule) | |
| `layer` = pathway | CPG `CPGPathwayDefinition` (PlanDefinition `type` = clinical-protocol or workflow-definition) | Test with the Lawal 2016 / E-P-A definition |
| `layer` = coverage | No standard. Closest is CMS NCD/LCD id; Da Vinci CRD is US real-time only | Keep HCF's own fields |
| `country` + `jurisdiction`; *`countryCode`* (ISO 3166-1 alpha-2), *`regionCode`* (ISO 3166-2) | `PlanDefinition.jurisdiction` (R4) / `useContext` (R5) | Add the codes; keep the readable name |
| `body` | `PlanDefinition.publisher` | |
| `guidelineTitle`, `guidelineYear`; *`guidelineDate`*, *`lastReviewed`* | EBMonFHIR `Guideline` (Composition) `title`, `date` | |
| `status` (current / stale / withdrawn ...) | `PlanDefinition.status`: active / retired / unknown | Keep HCF's wording; add *`fhirStatus`* if you export |
| `condition`; *`conditionCodes`* `{icd11, snomed}` | `PlanDefinition.subject` / `useContext` focus / `EvidenceVariable` (population) | ICD-11 required, SNOMED optional |
| `decision` | `PlanDefinition.topic` (deprecated in R5) / `action.code` | HCF's comparison key; keep it |
| `recommendation` | `action.description` / Recommendation section text | Verbatim, short quote |
| `direction` | CPG `directionOfRecommendation`; EBMonFHIR `RecommendationJustification` direction component | Normalise to: for / against / none, and keep the current five-value text |
| `strength` (as graded); *`strengthGrade`*: strong / conditional / not graded / non-GRADE system | CPG `strengthOfRecommendation`; EBMonFHIR strength-of-recommendation component | Fill `strengthGrade` only when the body uses GRADE or states an equivalent; otherwise "non-GRADE system" |
| *`certaintyOfEvidence`*: high / moderate / low / very low / not stated | CPG `qualityOfEvidence`; EBMonFHIR `CertaintyOfEvidence` | Copy what the guideline states; never infer |
| *`gradingSystem`* (e.g. "GRADE", "SIGN", "NICE wording", "Oxford CEBM") | `RecommendationJustification` rating system | Lets readers compare like with like |
| `drugs`; *`drugCodes`* `[{name, atc, rxnorm}]` | `ActivityDefinition.productCodeableConcept` | ATC required when the drug has one; RxNorm optional |
| *`performer`* (GP, sleep physician, dentist, psychologist, nurse) | `PlanDefinition.action.participant` | Pathway rows: "who prescribes CPAP" |
| *`setting`* (primary care, sleep clinic, home, online) | `useContext` (venue) | Pathway rows |
| *`step`* / *`after`* (order in a stepped-care route) | `action.relatedAction` | Pathway rows: self-help → CBT-I → drug |
| *`target`* `{measure, value, unit}` | `PlanDefinition.goal.target` | Waiting-time standards, CPAP adherence thresholds (e.g. hours per night) |
| *`payer`*, *`program`*, *`ruleType`* (eligibility / adherence / prior authorisation / reimbursement) | No equivalent; CMS NCD/LCD id in `citation.url` | Coverage rows |
| `citation` `{authors, title, journal, year, pmid, doi, url}` | `PlanDefinition.relatedArtifact` (type citation) / FHIR `Citation` | Already fine |
| `freeToRead`, `freeUrl`; *`archiveUrl`* | `relatedArtifact.document.url` | Add `archiveUrl` (Map of Medicine lesson) |
| `conflictsOfInterest`; *`funding`* | RIGHT items 18-19; GIN components | Guideline-level; could move to a separate `guidelines` list later |
| `whatWasRead`, `numbersToVerify`, `notes`, `researchFile` | No FHIR equivalent (closest: `Provenance`, `ArtifactAssessment` comment) | HCF-only research trail; keep |

**Later, optional:** factor guideline-level facts (title, year, status, COI, funding, grading system) into a `guidelines` array that rows reference by `guidelineId`. This matches EBMonFHIR's Guideline → Recommendation split and removes repetition across the 312 rows. A small script could then export a FHIR Bundle (PlanDefinition + Composition) if a partner wants FHIR.

## Open questions

- [ ] Ask the WHO Collaborating Centre (Oslo) whether listing ATC codes in an openly licensed dataset is allowed. Its notice bans "changing or manipulating the material".
- [ ] Verify ICD-11 code 7A41 (OSA) and other sleep codes in the WHO ICD-11 browser. The API needs a registered token, so I didn't use it.
- [ ] Should HCF fill `strengthGrade` for non-GRADE systems (for example map "Level A" to strong)? The default here is no: record "non-GRADE system".
- [ ] Open the Lancet SMART paper in Chrome and confirm the L1-L5 wording (the page returned 403).

## Blocked

- https://www.thelancet.com/journals/landig/article/PIIS2589-7500(21)00038-8/fulltext (403)
- https://www.astm.org/e2210-12r24.html (403)
- https://pmc.ncbi.nlm.nih.gov/articles/pmid/33610488/ (bot check)
- https://www.pulseit.news/?p=18729 (paywall after two paragraphs)
