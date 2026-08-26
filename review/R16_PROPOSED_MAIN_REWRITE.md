# Public CAD Is Not Operational Ground Truth

## What Hurricane Ida Reveals About Measuring Police Responsiveness

### Abstract

Researchers often calculate police response times from public computer-aided dispatch (CAD) timestamps. This paper asks whether the released fields represent a stable measurement object. In New Orleans, they do not. Among 419,840 non-officer-initiated records created before 28 July 2021, none contains a valid arrival field without a dispatch field. That configuration appears abruptly on 28 July, while dispatch-field coverage in officer-initiated records falls from 100 percent on 27 July to 40 percent on 28 July and 1 percent on 29 July. Five weeks later, during Hurricane Ida, the arrival-only share among arrival-observed non-officer records reaches 43.4 percent on 31 August and 49.3 percent on 1 September, compared with 5–12 percent during the preceding week. The largest half-day field-state change is 53.2 percentage points, larger than all 151 post-change ordinary-week comparisons. A standardized analysis gives the same ranking but covers only 86.1 percent of event records and 77.0 percent of baseline records, so the full-count result is primary. The data document a discontinuity in the released record and an extreme Ida-era reconfiguration, not physical dispatch, police performance, or the mechanism generating the public fields.

## 1. Introduction

Public CAD data are attractive because they appear to describe a simple operational sequence: a call is created, an officer is dispatched, and an arrival is recorded. Researchers and public agencies often turn those timestamps into measures of response time. That interpretation is valid only if the public fields have stable meanings and coverage. A missing dispatch timestamp may reflect a missing operational stage, but it may also reflect a different workflow, later data entry, field retention, redaction, or export logic.

This paper studies the public record before using it as a performance measure. The object of interest is deliberately modest: whether the released dispatch and arrival fields are present, and how their joint pattern changes over time. These field-presence measures are reproducible from the public file. They are not response times, physical-event indicators, or measures of service quality.

Two empirical facts organize the paper. First, the New Orleans public file changes abruptly on 28 July 2021. Before that date, no non-officer-initiated record has a valid arrival field without a dispatch field. Beginning on 28 July, that configuration appears and persists. At the same time, dispatch fields almost disappear from officer-initiated records even though their arrival fields remain nearly complete. Second, Hurricane Ida produces an additional, temporary reconfiguration within this new regime. On 31 August and 1 September, nearly one-half of arrival-observed non-officer records lack a public dispatch field.

The Ida pattern is large relative to later ordinary weeks. Using every non-officer record in each half-day, the largest event-minus-prior-week change in a public field state is 53.2 percentage points. No post-change ordinary-week comparison is as large. A conditional multinomial bootstrap leaves Ida first in all 4,000 draws, although that exercise does not model time-series dependence. A composition-standardized comparison also ranks Ida first, but it retains incomplete common support and is therefore treated as secondary evidence.

The paper's contribution is about measurement, not about the causal effect of Ida. Public records show that the released measurement product changes before the hurricane and changes again during the event. They do not reveal whether the underlying cause was an operational workaround, an entry convention, a retention rule, or an export transformation. The implication is straightforward: a public CAD timestamp should not be treated automatically as an operational clock. Analysts must first establish the relevant denominator, field meaning, coverage, and lineage.

## 2. Related literature and contribution

A large economics and policing literature shows that response delays matter. Faster police arrival can improve crime clearance and reduce injuries, while traffic congestion, staffing, and queueing can slow first responders. These studies demonstrate the value of a valid response-time measure. The present paper asks the logically prior question: whether a public administrative export supplies a stable response clock in the first place.

The paper also relates to work on administrative measurement. Calls-for-service and police records are shaped by reporting, classification, discretion, verification, and data-processing rules. More generally, measurement error and misclassification can distort group comparisons and structural interpretation. The evidence here adds a time dimension: the joint presence of public CAD fields changes abruptly, so the mapping from activity to released data is not stable across the sample period.

Disaster and domestic-violence research provides substantive motivation. Hurricane exposure, displacement, psychological stress, partner conflict, and demand for services can move together. Police composition can affect reporting, and pandemic-era studies show that calls, reports, and underlying victimization need not move one-for-one. Those studies do not validate a particular CAD timestamp. Ida is used here as a stress test of administrative observability, not as a treatment whose effect on domestic-violence incidence is estimated.

Finally, partial-identification methods provide the appropriate language when public records do not reveal a unique latent process. The paper does not propose a new general partial-identification estimator. It uses that discipline to distinguish quantities directly observed in the public file from quantities that are selected, bounded, or unavailable without additional evidence.

Relative to these literatures, the paper makes three contributions. It documents a date-localized change in the public CAD measurement regime; it shows that Ida produces an additional extreme but temporary reconfiguration within the later regime; and it translates those facts into practical requirements for measuring response time and reported-DV performance.

## 3. Data and public field measures

The analysis uses the official New Orleans Calls for Service files for 2020–2026. The main analysis is restricted to records coded `SelfInitiated=N`, referred to as non-officer-initiated records. Officer-initiated records are analyzed separately because their public dispatch-field convention changes sharply in July 2021.

For each record, the dispatch field is present when `TimeDispatch` is nonblank. The arrival field is valid when `TimeArrive` parses and is no earlier than `TimeCreate`. These two indicators produce four public configurations: neither field, dispatch only, arrival only, and both fields. “Arrival only” describes the released record; it does not mean that an officer physically arrived without being dispatched.

Three descriptive series summarize the public file: the share of records with a dispatch field, the share with a valid arrival field, and the share of arrival-observed records in the arrival-only configuration. Calls are grouped by creation date; dispatch and arrival fields are read from the eventual released record.

## 4. A public-data regime change on 28 July 2021

The arrival-only configuration is completely absent from non-officer-initiated records before 28 July 2021. Across 419,840 records created from January 2020 through 27 July 2021, its count is exactly zero. It appears abruptly on 28 July and remains present thereafter.

A direct audit of the official July 2021 compressed CSV confirms that this is not an artifact of the aggregate pipeline. On 27 July, no non-officer record is arrival only and every officer-initiated record contains both fields. On 28 July, 34 of 620 non-officer records are arrival only, while officer dispatch-field coverage falls to 40 percent. On 29 July, 69 of 666 non-officer records are arrival only, while only 5 of 504 officer records retain a dispatch field. Officer arrival fields remain complete.

The simultaneous movement across the two initiation streams is important. Officer-initiated records have an officer by construction, yet their public dispatch fields almost disappear while their arrival fields remain complete. The missing public dispatch field therefore cannot be read mechanically as the absence of an officer or of all operational activity. The discrepancy lies somewhere between activity and released representation.

The change persists. Dispatch-field coverage among non-officer records is about 90 percent in 2020, then declines after July 2021 and reaches 65.4 percent in 2024. In the comparable non-officer denominator, coverage is 66.0 percent in 2025 and 66.8 percent in the 2026 snapshot. The lower all-row rate of about 41.8 percent pools these records with officer-initiated records, whose dispatch fields are almost always absent under the later convention.

## 5. Hurricane Ida within the new regime

Hurricane Ida made landfall on 29 August 2021, five weeks after the public-file transition. During the preceding week, the arrival-only share among arrival-observed records ranges from 5.1 to 11.7 percent. It rises to 13.2 percent on 29 August, 22.9 percent on 30 August, 43.4 percent on 31 August, and 49.3 percent on 1 September. It falls to 16.4 percent on 2 September and continues toward its pre-event range over the following days. Dispatch-field coverage moves in the opposite direction, reaching 47.3 percent on 31 August and 40.9 percent on 1 September.

These movements are large, but their interpretation must remain administrative. The figures index calls by creation date and read fields from the eventual released record. They do not show a live system snapshot, nor do they establish that a unit physically arrived without dispatch. They show that records created during the event were ultimately released in a different field configuration.

## 6. How unusual was Ida?

For each five-day window, the analysis compares ten twelve-hour cells with the same half-days one week earlier. Within each cell it computes changes in the three independent public configurations. The summary statistic is the largest absolute change across the thirty cell-by-state comparisons. A value of 0.532 means that the largest public-state share changed by 53.2 percentage points.

The primary reference comparison uses 151 ordinary windows for which both the event and baseline periods occur after 28 July 2021. Specified emergency and holiday windows remain excluded. This post-change set was defined after the July transition was identified, so it is a transparent descriptive sensitivity rather than a preregistered test.

Ida's full-count statistic is 0.532. The largest reference value is 0.310. Thus Ida is larger than all 151 post-change ordinary-week comparisons. A conditional window-wise multinomial bootstrap independently perturbs Ida and the reference windows. Ida ranks first in all 4,000 draws, with a 95-percent interval of 0.475–0.601 for its statistic. Because the procedure does not preserve serial or cross-window dependence, it is best read as a robustness check against ordinary categorical-count variation, not as formal time-series inference.

A second estimator standardizes across common call-type, hour, and schema strata. It also ranks Ida first: the maximum standardized contrast is 0.507, compared with 0.328 for the largest of 153 stage-era references. However, the standardized analysis covers only 86.1 percent of event records and 77.0 percent of baseline records. Ida would fail the 0.90 support rule applied to candidate reference windows. The standardized result is therefore secondary.

The week after Ida has a large statistic of 0.478 because its baseline is Ida itself; it captures recovery rather than an independent shock. Hurricane Francine, a later-regime hurricane in September 2024, has a much smaller statistic of 0.110. Ida is therefore not merely a generic consequence of comparing any hurricane week with the preceding week.

## 7. What do the data suggest—and what remains unknown?

The officer-initiated stream provides the most concrete clue. The public definition describes these items as generated by officers in the field. Before 28 July 2021, their dispatch and arrival fields are almost universally present. After the break, arrival remains nearly universal while dispatch falls to approximately 1 percent. The arrival-only configuration is therefore a normal public form for officer-initiated activity under the later regime.

During Ida, non-officer records move toward the same public configuration. One plausible pathway is that some calls normally represented with a dispatch field were entered, retained, or exported through a workflow that omitted it. That possibility is consistent with a record-production change, but it is not identified. Internal call-origin provenance, event-entry histories, unit-assignment histories, and export logs would be required to distinguish reclassification, operational workarounds, back-filling, and export omission.

The late Ida movement also occurs within recorded final-disposition categories. On the afternoon and evening of 31 August, the public dispatch-field share among arrival-observed records falls by 49.5 percentage points. A change in the observed disposition mix would have increased the share by about 1.2 points; within-disposition changes account for approximately −50.7 points. The following morning produces nearly the same decomposition. The observed final-disposition mix therefore does not explain the aggregate decline.

Official metadata define the public field labels and identify the data provider. Public chronology rules out two proposed technology explanations: the Carbyne APEX cutover occurred in June 2022, and the Hexagon OnCall Records project was never launched. No public versioned changelog or internal-to-public reconciliation was available, and no agency confirmation of the July change was obtained. The strongest supported conclusion is a discontinuity in the released record, not a named institutional mechanism.

## 8. Implications for response-time and reported-DV research

Public CAD directly supports field-completeness measures on a declared denominator. A duration calculated among records with both endpoints is a selected-record statistic when endpoints are missing. Queueing and capacity are not observed from endpoint presence alone. A reported-DV analysis additionally requires a validated classification rule, transparent treatment of unresolved records, endpoint coverage, and lineage to the relevant downstream stage.

Reported CAD calls are not equivalent to underlying domestic-violence incidence or complete help-seeking. Ida motivates this measurement work, but the current system-level analysis does not estimate a DV effect.

## 9. Limitations

The analysis uses eventual public records rather than internal event histories. The July change is verified in the official source bytes, but its institutional cause is not observed. The post-change comparison set was defined after the break was identified and excludes specified emergency and holiday contexts. Reference windows overlap, and the bootstrap does not preserve all time-series dependence. Public `SelfInitiated=N` is not equivalent to “911 only.” Weather, holidays, mobility, evacuation, reporting behavior, call composition, suppression, and other contemporaneous conditions can affect the observed record.

These limitations restrict interpretation but do not erase the descriptive result. The released field configuration changes abruptly in July 2021, changes further during Ida, and follows different conventions across initiation streams.

## 10. Conclusion

Public CAD files are valuable administrative records, but their timestamps are not operational ground truth by definition. In New Orleans, a new arrival-only configuration appears suddenly on 28 July 2021, accompanied by an almost complete disappearance of dispatch fields from officer-initiated records. Five weeks later, Hurricane Ida produces an additional two-day reconfiguration that is larger than every post-change ordinary-week comparison.

The public evidence identifies the timing and magnitude of changes in the released record. It does not identify the underlying operational sequence or the institutional mechanism that produced those fields. Analysts should therefore treat public CAD timestamps as administrative measures until their meanings, coverage, and lineage have been validated for the specific performance question.
