# R16.0 readability and publishability review

## Editorial verdict

I reviewed the exact `review/r16.0` branch at commit `3b8fbacd1934933cdd7e2507f68ad7699de0c3be`. It is explicitly a narrative rewrite that preserves the validated R15.1 numerical results rather than introducing a new empirical specification.

My recommendation is now:

| Purpose | Verdict |
|---|---|
| Send to Professor Beland | **Pass, after a few minor presentational edits** |
| Standalone working paper | **Minor revision** |
| Publishable empirical result | **Yes, as a measurement/data-quality contribution** |
| Conventional economics field-journal article | **Not yet without an additional empirical extension** |

The original R13 referee review examined the main text, appendix, LaTeX sources, and full reproduction tree and recommended major revision.  R16 is a genuine resolution of that recommendation, not another cosmetic edit.

---

# 1. Can Professor Beland understand the paper quickly?

## Yes

R16 now has a clear four-step argument:

1. The public CAD field convention changes abruptly on July 28, 2021.
2. Hurricane Ida produces another temporary change within the new convention.
3. The Ida change is larger than all 151 later ordinary-week comparisons.
4. The released data do not identify physical response or the institutional mechanism.

That sequence appears consistently in the main paper, the one-page status note, README, and reviewer reading guide.

A professor reading only the following elements would now understand the project:

- the abstract;
- the four-state definition table;
- the July 27–29 transition table;
- the daily Ida figure;
- the two-row comparison table;
- the conclusion.

That is a major improvement over R15.1, where the reader had to understand the reference design, support rule, bootstrap, secondary statistics, LP, and timing placebo before forming a stable mental picture of the empirical event.

## The ordering is now correct

The main paper proceeds in the right intellectual order:

- research question;
- relevant literature;
- data and plain-language field configurations;
- July public-file transition;
- daily Ida pattern;
- comparison with ordinary weeks;
- possible explanations and remaining uncertainty;
- measurement implications;
- limitations;
- conclusion.

In particular, R16 shows the daily Ida pattern **before** explaining the ranking design. That was the most important structural repair.

## The paper no longer depends on the technical archive

The professor-facing supplement now follows the same empirical sequence as the main paper, while LP details, identified-set proofs, formal verification, and other legacy machinery remain in a separate archive.

The release verifier also enforces:

- a 10–14 page main paper;
- a 12–18 page empirical supplement;
- exactly two main-paper figures;
- no more than two equations;
- an abstract below 190 words;
- a conclusion below 250 words;
- exclusion of the legacy archive from the professor-facing combined PDF.

That is the correct package architecture.

---

# 2. Writing-style assessment

## What now works well

### Plain-language field categories

The paper defines:

- neither field;
- dispatch only;
- arrival only;
- both fields.

It then explicitly warns that “arrival only” describes the released row and does not prove physical arrival without dispatch.

This is substantially easier to understand than asking readers to retain $J_{00},J_{10},J_{01},J_{11}$ throughout the paper.

### The July transition is concrete

The paper no longer merely says that a “regime changed.” It shows:

- zero arrival-only non-officer records on July 27;
- 34 on July 28;
- 69 on July 29;
- officer dispatch-field coverage falling from 100% to 40% to 1%.

The simultaneous officer-stream change makes the measurement problem intuitive even for a reader who knows nothing about the earlier project.

### The Ida result is expressed in interpretable units

The paper explains that 0.532 means a **53.2-percentage-point change** in the largest half-day public-field share. It then compares that with a 31.0-point maximum among the 151 post-change references.

That is much better than leading with a rank fraction or a constrained-program score.

### The primary and secondary analyses are visibly separated

The full-count post-change comparison is now primary. The standardized analysis is explicitly secondary because its common-support coverage is incomplete.

This gives the reader one result to remember rather than several co-equal designs.

### The conclusion is disciplined

The conclusion states what is identified:

- timing and magnitude of changes in the released record;

and what is not:

- the underlying operational sequence;
- the institutional mechanism;
- police performance.

That boundary is concise and no longer overwhelmed by formal identification terminology.

---

# 3. Remaining readability improvements

These are minor. I would not commission another full rewrite.

## 3.1 Replace the most difficult recurring phrase

The phrase

> “arrival-only share among arrival-observed non-officer records”

is exact but cognitively heavy. It appears in the abstract, introduction, data section, and Ida discussion.

Define a simple term once:

> **Public missing-dispatch share:** among records with a valid arrival field, the share whose public dispatch field is missing.

Then write:

> “The public missing-dispatch share rose to 43.4% on August 31 and 49.3% on September 1.”

This is easier to process than repeatedly nesting three conditions inside one noun phrase.

The figure legend could similarly say:

> “Dispatch field missing among arrival-observed records”

rather than:

> “Arrival-only among arrival-observed.”

## 3.2 Make the abstract slightly less technical

The abstract is already much better and remains below the automated 190-word ceiling.  But it still combines:

- the July break;
- officer-stream change;
- Ida daily numbers;
- the 151-window comparison;
- standardized coverage;
- interpretation limits.

For Professor Beland this is acceptable. For external circulation, I would remove the standardized-analysis sentence from the abstract and leave that qualification for the methods/results section.

A cleaner abstract would be:

> Public CAD timestamps are often used to measure police response time, but that use requires stable field definitions and coverage. In New Orleans, the released record changed abruptly on July 28, 2021. Before that date, none of 419,840 non-officer-initiated records contained an arrival timestamp without a dispatch timestamp. Within two days, that configuration became common, while dispatch-field coverage in officer-initiated records fell from 100% to 1%. Five weeks later, Hurricane Ida produced a temporary additional shift: among records with an arrival timestamp, the share missing a dispatch timestamp reached 43.4% on August 31 and 49.3% on September 1. The largest half-day change was 53.2 percentage points, exceeding all 151 later ordinary-week comparisons. These results document instability in the released measurement product, not physical police response or performance. Public CAD should be used as an operational clock only after field meaning, coverage, and provenance are validated.

## 3.3 Change the first sentence

Current:

> “Researchers calculate police response times from public computer-aided dispatch timestamps.”

Better:

> “Researchers and public agencies often calculate police response times from public computer-aided dispatch timestamps.”

The current sentence sounds universal. “Often” is both more accurate and more natural.

## 3.4 Reduce one layer of repetition in the introduction

The first two introductory paragraphs both explain that public fields are not necessarily operational events. The final introductory paragraph returns to the same point.

This is not a serious problem, but approximately 70–100 words could be removed by combining the first two paragraphs. The paper would reach the July 28 result faster.

## 3.5 Add authorship and standalone-document information

The title page still has an empty author field.

That is acceptable for an internal anonymized package, but not for a genuinely standalone professor paper. At minimum, add:

- author name;
- affiliation;
- “Discussion draft” or “Draft for discussion”;
- a short data-and-code availability statement;
- a repository link or citation;
- acknowledgments where appropriate.

This is the most visible sign that the PDF remains a package artifact rather than a finished working paper.

A short endnote would be sufficient:

> Replication materials, source bindings, and the empirical supplement are available in the accompanying public repository.

Journals focused on policy-data interactions commonly expect an explicit data-availability statement and stable access to replication materials.

## 3.6 Use percentage points consistently

The main comparison table already uses “53.2 pp” and “31.0 pp,” which is good.

In prose, present the intuitive value first:

> “The largest change is 53.2 percentage points ($M=0.532$).”

Do not make the reader translate 0.532 before learning what it means.

---

# 4. Is the empirical result publishable?

## The result itself: yes

The strongest empirical fact is not merely that Ida was unusual. It is the combination of:

- an exact pre-July zero across 419,840 non-officer records;
- an abrupt July 28 transition;
- a simultaneous change in the officer-initiated stream;
- persistence through later years;
- a second, temporary Ida-era reconfiguration;
- raw-source and aggregate parity;
- complete reproducibility.

The original independent referee report already concluded that the core fact was “real, reproducible, and worth publishing.”  R16 now gives that fact a publishable narrative.

There is also clear precedent for publishing research on measurement error in police calls-for-service data. Simpson and Orosco’s PLOS ONE article studies differences between dispatcher and officer classifications and explicitly frames them as measurement-error problems in calls-for-service records.

## The current manuscript: publishable in the right category

R16 is now a plausible submission as a:

- data-quality or administrative-measurement research article;
- police-data methods note;
- public-data governance paper;
- practitioner-facing policing research article.

For example, *Data & Policy* explicitly publishes work on interactions between data systems, policy, and governance, including responsible use of policy data.

*Policing: A Journal of Policy and Practice* explicitly seeks accessible, practitioner-relevant work connecting police researchers, analysts, policymakers, and law-enforcement leaders. Its author guidance emphasizes getting to the point, minimizing elaborate methodological detail, and presenting data in accessible tables and figures—the direction R16 has now taken.

I would therefore describe the publication status as:

> **Near-publishable as a focused measurement or research-note contribution, after minor manuscript completion and one stronger “why this matters” analysis.**

## It is not yet a conventional economics contribution at the level of the closest response-time papers

The closest economics studies do more than document administrative instability:

- Blanes i Vidal and Kirchmaier estimate a causal effect of response time on crime clearance using geographic discontinuities and rich police data.
- Brent and Beland link traffic and incident records to estimate how congestion affects emergency response and damages.
- DeAngelo, Toger, and Weisburd study police response time and injury outcomes.

R16 does not identify:

- a causal effect;
- a service-performance parameter;
- a validated response clock;
- a generating mechanism;
- a victim or crime outcome.

That is not a defect for a measurement paper. It does mean that the current manuscript would be difficult to place as a full economics field-journal article unless it acquires an additional economic estimand or external validation.

---

# 5. The highest-value empirical extension

The next extension should **not** be another mathematical framework.

It should quantify the consequence of ignoring the measurement break.

For each period, report:

| Period | Both endpoints present | Dispatch missing among arrival-observed | Naïve dispatch-to-arrival median among complete rows |
|---|---:|---:|---:|
| Before July 28 | … | 0% | … |
| August before Ida | … | … | … |
| Ida | … | … | … |
| Post-Ida | … | … | … |
| 2024–2026 | … | … | … |

The point would not be to claim that the conditional duration is true response time. It would show directly that:

1. the population on which a naïve response-time statistic is calculated changes sharply;
2. complete-case response-time estimates condition on an increasingly selected subset;
3. comparisons across the July 2021 boundary may combine different measurement regimes.

That would convert the paper’s warning from:

> “The public fields are unstable”

into:

> “Here is how the instability changes the response-time statistic that researchers and agencies would otherwise report.”

That single extension would materially improve publication prospects in economics, public administration, and policing.

---

# 6. What would further raise the publication ceiling?

## Agency or system validation

The paper appropriately states that no agency confirmation was available.

Even a limited response from OPCD, NOPD, or the City identifying:

- a workflow change;
- a software/export change;
- a data-retention convention;
- or an inability to reconstruct the change

would strengthen the paper.

## Replication in a second public CAD system

A second city is not necessary for a research note, but it would transform the contribution from a New Orleans case study into evidence that public CAD clocks can undergo undocumented regime changes more generally.

## A decision consequence

Show how the measurement issue affects:

- an estimated response-time trend;
- a performance threshold;
- a staffing conclusion;
- a disaster comparison;
- or a reported-DV response measure.

That would give the paper a more direct policy and economic payoff.

---

# Final recommendation

## For Professor Beland

**Sendable now.**

Before sending, I would make only three surgical edits:

1. add author, affiliation, draft status, and a data/code statement;
2. define “public missing-dispatch share” and use it instead of the longer recurring phrase;
3. shorten the abstract by removing the standardized-support sentence.

Professor Beland should now be able to understand the project from the abstract, two figures, and the comparison table without consulting the technical archive.

## For public working-paper circulation

**Minor revision.**

The narrative, structure, terminology, and evidentiary hierarchy are now strong enough. The remaining work is manuscript completion, not another rewrite.

## On publishability

**The empirical result is publishable.**

The strongest realistic framing is:

> A date-localized change in the public CAD measurement regime, followed by an extreme Ida-era reconfiguration, demonstrates that released CAD timestamps cannot be treated as stable operational clocks without validation.

That can support a good measurement, policing, public-administration, or data-policy article.

For a conventional economics paper, add a direct analysis showing how the regime change distorts a commonly used response-time or performance statistic, ideally supplemented by agency validation or a second-city replication.

I reviewed the exact branch source, supplement structure, status note, package metadata, and verification rules. The binary PDF could not be raster-rendered page by page in this environment, so the visual assessment is based on the LaTeX structure and the package’s enforced page, figure, equation, and PDF-composition checks rather than screenshots.
