# Vaultline | Investigating Suspicious Cloud Access

**Yarin Greenberg · SOC Analyst Portfolio · CyberGo by Mamram**

**~50,000 logs · 4 investigators · Splunk & SPL · 73-day suspicious activity window**

How do you investigate suspicious activity when valid accounts are involved and normal business activity continues alongside it?

Vaultline is a team-based SOC investigation of a simulated cloud-data incident. We analyzed approximately **50,000 log records**, correlated activity across multiple sources, and assembled an evidence-based account of anomalous data retrieval and potential persistence.

The training scenario was inspired by the **2022 LastPass cyberattack**. The findings and metrics below belong to the **Vaultline exercise**, not to LastPass's actual systems or incident data.

## Explore the full investigation

- [Full investigation report](docs/investigation-report.md): entities, timeline, analysis, impact, confidence, and recommendations.
- [Full 26-slide presentation](docs/presentation.md): English briefing with speaker guidance and team handoffs.
- [Evidence register](evidence/README.md) and [timeline CSV](evidence/timeline.csv): source-reported evidence, not raw logs.
- [SPL query pack](queries/README.md): original report queries and reviewed adaptations, with expected findings and limitations.
- [Source reconciliation](docs/source-reconciliation.md): corrections and remaining evidence gaps.
- [Original source files](original-files/README.md): supplied report, HTML deck, and Hebrew presentation script.
- [Verification guide](docs/verification.md): local checks, arithmetic, source hashes, and reproducibility boundaries.

```text
vaultline-soc-investigation/
  README.md
  docs/                 Full report, full presentation, reconciliation, verification
  evidence/             Evidence register, timeline, reported metrics, scenario entities
  queries/              Source SPL and reviewed query adaptations
  original-files/       Supplied report, HTML presentation, Hebrew script
  scripts/              Package and arithmetic verification
```

This is a portfolio reconstruction from the supplied investigation report and presentation. The approximately 50,000-log exercise dataset is not included. No raw logs were generated, and queries were not executed against a SIEM while preparing this package. “Confirmed” refers to findings reported by the investigation team. The English documents reconcile known inconsistencies; the original sources retain their historical wording.

## Investigation snapshot

| Area | What the investigation established |
|---|---|
| Dataset scope | Approximately **50,000 log records** |
| Main investigation platform | **Splunk**, using **SPL** |
| Accounts central to the findings | A DevOps user and an archive-replication service account |
| Suspicious activity window | **73 days**, from September 9 to November 21, 2026 in the scenario timeline |
| Anomalous retrieval activity | **271 retrieval events**, totaling **11.00 GiB** |
| Data scope | **24 customer namespaces** and one internal configuration object |
| Persistence concern | A new service-account access key with no matching revocation found in the available data |
| Main unresolved questions | Initial access, operator identity, and whether access continued beyond the observation window |

The dataset size describes the overall exercise. The 271 retrievals are a specific subset of activity identified during the investigation; they are not the total number of logs or necessarily distinct files.

## My contribution

I focused on **Identity & Access**, tracing the behavior of the user and service account across the incident:

- Established behavioral baselines and identified changes in source, timing, target objects, and access patterns.
- Correlated **VPN authentication**, **cloud activity**, and **Windows logon events** to test the sequence of events.
- Reconciled Windows timestamps reported in **UTC+3** with sources reported in **UTC**.
- Examined the service account's transition from internal replication to external retrieval activity.
- Compared access-key creation against a legitimate key-rotation pattern to assess potential persistence.
- Presented the identity and access chapter, explaining the evidence, alternative explanations, and limits of the conclusions.

## Three findings that shaped the case

### Normal activity continued alongside the anomaly

The DevOps account's small, regular morning configuration-file retrievals continued after a new evening pattern appeared. That second pattern involved repeated customer-data retrievals from a different external source.

This was a significant **behavioral deviation**, but concurrent patterns alone did not establish that two different people were operating the account.

### The VPN connection could not explain the first observed cloud activity

Cloud retrievals began approximately **40 minutes before** the associated successful VPN connection. Comparing timestamps across sources prevented us from labeling that connection as the initial entry point.

The initial access mechanism remained **unknown**.

### Key creation raised a persistence concern

The service account acquired a new access key during the suspicious activity window. A comparison account showed a paired revoke-and-create lifecycle, while no matching revocation was found for the suspicious key in the available data.

The creation event was established. Whether the key remained usable after the dataset ended was not.

## Evidence and workflow

The investigation considered **Cloud Audit, VPN, Windows Event, File Audit, Backup, Web, and Proxy logs**, together with **identity and asset context**. Each source answered a different question; no individual log source explained the entire incident.

1. **Establish context:** identify account roles, asset criticality, expected activity, and timestamp conventions.
2. **Compare behavior:** separate routine replication and configuration access from anomalous customer-data retrieval.
3. **Correlate events:** connect accounts, hosts, operations, and timestamps across relevant sources.
4. **Measure scope:** calculate retrieval counts and volume while keeping baseline traffic separate.
5. **Test explanations:** investigate authentication, account changes, and possible execution mechanisms; record gaps and negative results.
6. **Communicate findings:** assemble a shared report and coordinated briefing with findings, impact, supported technique mappings, and response recommendations.

## How we worked as a team

We organized the investigation and presentation into four connected areas:

| Team member | Focus |
|---|---|
| **Imri** | Case lead, case framing, overall assessment, and recommendations |
| **Yarin — me** | Identity & Access, behavioral baselines, authentication correlation, and timeline |
| **Alon** | Data & Impact, retrieval scope, and impact assessment |
| **Idan** | Intel & Context, technique mapping, hypotheses, and confidence |

These areas came together in a **shared investigation report** and a **coordinated presentation**. My account and timeline findings provided context for the data-impact and intelligence chapters, and the briefing used explicit handoffs between presenters.

## Findings with clear limits

| Evidence | Interpretation and boundary |
|---|---|
| Repeated cloud-object retrievals | Supports the team's **Data from Cloud Storage** mapping; does not verify publication on a third-party site |
| New access-key creation without a matching revoke in the dataset | Supports investigation of **Additional Cloud Credentials** and potential persistence; does not prove the key is still active |
| Retrieval of an internal configuration object | A possible discovery lead; its contents and subsequent use were not established |
| Successful backup jobs and no observed delete operations | No destructive impact established from those checks; successful jobs alone do not prove full recoverability |
| Missing explanatory process, service, or task events | A telemetry gap, not proof that execution never occurred |

**MITRE ATT&CK** mapping was tied to the observed evidence. Initial access and operator attribution remained open rather than being filled in with assumptions.

## Response priorities developed by the team

- Contain suspicious account access and review sessions and access keys.
- Preserve relevant evidence and investigate the associated endpoints.
- Review service-account permissions and long-lived credentials.
- Improve detection for unusual retrieval volume, new external sources, and anomalous key creation.
- Address telemetry coverage and retention gaps that limited the investigation.

These were **recommendations from the exercise**, not claims of remediation performed in a production environment.

## About me

I'm **Yarin Greenberg**, a junior SOC analyst with hands-on training in a **430-hour CyberGo by Mamram program**. My interests include **log analysis, incident investigation, identity security, and threat detection**.

My training includes **Splunk/SPL, Microsoft Sentinel/KQL, Wireshark, Windows and Active Directory analysis**, and evidence-based incident reporting. In Vaultline, my focus was turning account activity into a timeline that could be explained and defended in a technical discussion.

[Connect with me on LinkedIn](https://www.linkedin.com/in/yarin-greenberg-21982133a)

## Scenario background

LastPass's public incident updates describe compromised access that led to cloud-based backup data being accessed. Vaultline uses that real-world incident as inspiration for a training investigation; its entities, timeline, counts, and conclusions should not be treated as findings about LastPass.

- [LastPass — December 2022 incident notice](https://blog.lastpass.com/posts/notice-of-recent-security-incident)
- [LastPass — security incident update and recommended actions](https://blog.lastpass.com/posts/security-incident-update-recommended-actions)
