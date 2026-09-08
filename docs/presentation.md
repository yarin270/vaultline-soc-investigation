# Vaultline presentation

**Full 26-slide English briefing · Team E · 24-minute source schedule**

[Home](../README.md) · [Report](investigation-report.md) · [Original HTML deck](../original-files/Vaultline-Case.html) · [Reconciliation](source-reconciliation.md)

This is a slide-by-slide English adaptation of the full supplied HTML deck, with speaker guidance informed by the Hebrew script. The slide order, four chapters, timing, and handoffs are preserved. Wording applies the evidence corrections documented in the reconciliation note. It is not a six-slide sample or a new rendered PowerPoint.

| Presenter | Slides | Total time |
|---|---|---|
| Imri | 1–5 and 25–26 | 6 minutes |
| Yarin | 6–12 | 6 minutes |
| Alon | 13–18 | 6 minutes |
| Idan | 19–24 | 6 minutes |

## Slide 01 — Vaultline case file

**Presenter:** Imri · **Schedule:** 00:00–00:45

Two valid accounts, one external source, 271 retrieval events totaling 11.00 GiB, and a 73-day suspicious window. Team E presents a training simulation inspired by the 2022 LastPass attack. Findings belong to Vaultline.

**Speaker guidance:** Introduce the four chapters and the Confirmed / Hypothesis / Unknown labels. Use scenario dates and avoid claiming a real-time alert outcome beyond the report: no alert is documented.

## Slide 02 — Case Lead

**Presenter:** Imri · **Schedule:** 00:45–01:00

The case lead opens with the trigger, evidence framework, and investigation method, then returns for recommendations and the closing assessment.

**Speaker guidance:** Pause at the chapter divider. Explain that Yarin covers identity, Alon impact, and Idan context before the closing handoff.

## Slide 03 — Investigation trigger and evidence

**Presenter:** Imri · **Schedule:** 01:00–01:50

A customer reported archive records on a third-party site. No source, link, or screenshot was supplied. The posting remains unverified. Independently reported Cloud Audit findings establish sustained anomalous retrieval, with authentication and identity sources providing context.

**Speaker guidance:** Distinguish the customer allegation from the log-based findings. Unknown publication is neither confirmed nor disproven. Do not claim three sources independently measure the same retrieval volume.

## Slide 04 — Sources and evidence labels

**Presenter:** Imri · **Schedule:** 01:50–02:45

The investigation considered Cloud Audit, VPN, Windows Event, File Audit, Backup, Weblog, and Proxy records with identity and asset context. Confirmed: directly supported in the team’s reported evidence. Hypothesis: consistent but unconfirmed. Unknown: available evidence does not answer the question.

**Speaker guidance:** The HTML deck groups sources into six categories including IAM. This edition uses the approved README inventory and treats key lifecycle events as Cloud Audit context. Correlate when possible; a primary source can establish an event directly.

## Slide 05 — Case at a glance

**Presenter:** Imri · **Schedule:** 02:45–03:30

271 retrieval events. 270 customer retrievals across 24 namespaces and one internal configuration retrieval. 11,811,168,130 bytes, equivalent to 11.00 GiB or 11.81 GB. Accounts: r.zohar and svc_archsync. External source: 31.154.88.203, ownership unknown. Severity: High.

**Speaker guidance:** Give the narrative map: Yarin explains identities and timing, Alon measures data, Idan assesses meaning and confidence. Hand to Yarin.

## Slide 06 — Identity and Access

**Presenter:** Yarin · **Schedule:** 03:30–03:45

Two account baselines, anomalous behavior, authentication timing, the service-account sequence, and the credential lifecycle.

**Speaker guidance:** Thank Imri. Explain that the account timeline supports the later impact and technique analysis.

## Slide 07 — Two account baselines

**Presenter:** Yarin · **Schedule:** 03:45–04:45

During Aug 27–Sep 8, r.zohar retrieves pipeline configuration from 212.117.55.9 near 07:12 and 08:18 UTC, at 14,000–14,500 bytes per request. svc_archsync performs cyclic internal replicate_object operations from 10.90.4.11, 10.90.4.12, and 10.90.5.11. Reported replication totals are about 1.83 GiB, repeatedly accessing roughly 20 MB of unique data.

**Speaker guidance:** Keep the replication baseline separate from incident loss. These are observed patterns, not a claim about every action the identities have ever performed.

## Slide 08 — Concurrent morning and evening patterns

**Presenter:** Yarin · **Schedule:** 04:45–05:45

At Sep 9 21:00 UTC, r.zohar begins customer record retrieval from 31.154.88.203. Each reported customer retrieval is 43,745,037 bytes, in evening bursts about six minutes apart. The normal morning configuration pattern continues alongside it.

**Speaker guidance:** Compare target, source, time, and size. Concurrent patterns establish behavioral deviation, not two different people. A different pattern alone does not determine compromise versus intentional misuse.

## Slide 09 — The VPN timing test

**Presenter:** Yarin · **Schedule:** 05:45–06:45

Sep 9: first observed cloud retrieval at 21:00:00 UTC; successful VPN login at 21:40:01 UTC from the same IP and account, with TOTP and a 195-minute session. The difference is 40 minutes and 1 second. Initial access remains unknown.

**Speaker guidance:** The later session cannot explain the earlier cloud access. Shared identity and IP support correlation, not certainty about operator or causality. The source of the TOTP is unknown.

## Slide 10 — Service-account sequence

**Presenter:** Yarin · **Schedule:** 06:45–08:05

Sep 24 21:24: r.zohar retrieves archsync-runtime.yaml, 8,140 bytes, from the Critical cloud tenant. Sep 26 19:30: svc_archsync Type 3 logon from WKS-ENG-01 to SRV-BUILD. Sep 26 21:00: first observed external service-account retrieval. Oct 27 20:36: second logon along the same path.

**Speaker guidance:** The Windows source times 22:30 and 23:36 are UTC+3. Normalize once. The YAML retrieval is confirmed; discovery, contents, and a causal credential transition remain hypotheses or unknown. EventCodes 4688, 4697, 7045, 4698, 4699, 4702 supplied no explanation for the logons.

## Slide 11 — Access-key lifecycle

**Presenter:** Yarin · **Schedule:** 08:05–08:55

a.perl provides a comparison: old-key revocation followed by new-key creation. On Oct 27 at 22:09 UTC, svc_archsync creates a key from 31.154.88.203, with no matching revoke found in the available data. Present key validity is unknown.

**Speaker guidance:** The comparison supports review; it does not make revoke-before-create the only legitimate policy. T1098.001 describes additional cloud credentials. Credential creation is supported; malicious persistence remains an assessment.

## Slide 12 — Timeline recap

**Presenter:** Yarin · **Schedule:** 08:55–09:30

Sep 9 cloud retrieval and later VPN success; Sep 24 internal YAML; Sep 26 network logon and external service retrieval; Oct 27 second logon and key creation; Nov 19 last service retrieval; Nov 21 last suspicious retrieval; Nov 24 coverage ends.

**Speaker guidance:** All event times are in the report and timeline CSV. The suspicious interval is 73d 1h 6m. Coverage ending is an observation, not containment. Hand to Alon for volume and impact.

## Slide 13 — Data and Impact

**Presenter:** Alon · **Schedule:** 09:30–09:50

Measure retrieval scope, reconcile bytes, separate baseline traffic, and define the limit of the impact assessment.

**Speaker guidance:** Introduce the corrected total and explain that arithmetic can be checked without equating events with unique files.

## Slide 14 — Retrieval scope

**Presenter:** Alon · **Schedule:** 09:50–11:00

271 get_object events: 270 customer retrievals across 24 customer namespaces, plus one 8,140-byte internal configuration retrieval. r.zohar accounts for about 6.48 GiB and svc_archsync for 4.52 GiB. The service account has 111 reported customer retrievals across cust-007 through cust-024.

**Speaker guidance:** Use retrieval events throughout. The internal namespace is not a 25th customer. Object contents and legal customer identities are outside these log-derived counts.

## Slide 15 — Byte reconciliation

**Presenter:** Alon · **Schedule:** 11:00–12:20

270 × 43,745,037 + 8,140 = 11,811,168,130 bytes. Divide by 1024³ for 11.00 GiB or 1000³ for 11.81 GB. Service-account component: 111 customer events. Remaining user component: 159 customer events plus YAML.

**Speaker guidance:** 159 is derived as 270 minus 111. This checks arithmetic against the reported components; it is not an independent re-query of the raw data. The displayed GiB and GB are rounded.

## Slide 16 — Baseline exclusions and corrections

**Presenter:** Alon · **Schedule:** 12:20–13:25

Exclude approximately 1.83 GiB of internal replicate_object baseline traffic. The older 110-object figure belongs to unique replication targets, not incident retrievals. The older 11.26 GB figure was not reproducible in the source reconciliation.

**Speaker guidance:** Repeated baseline traffic must not inflate the incident total. Likewise, incident retrieval bytes do not automatically represent unique information.

## Slide 17 — Confidentiality, integrity, and availability

**Presenter:** Alon · **Schedule:** 13:25–14:20

The team assesses confidentiality impact to customer data and internal configuration. All 103 supplied backup jobs reportedly completed SUCCESS. No delete_object operation was found. Integrity or availability impact was not established.

**Speaker guidance:** Backup success does not prove a tested restore or that every scheduled job is represented. Missing delete operations do not rule out all possible modifications. No ransomware or destructive impact is proven.

## Slide 18 — Impact boundary

**Presenter:** Alon · **Schedule:** 14:20–15:30

The sources report retrieval count, byte volume, namespaces, identities, and observed timing. They do not establish every object’s contents, affected individuals, third-party publication, or containment after the window.

**Speaker guidance:** Explain why manifest review, content classification, and Legal/Privacy coordination are recommended. Hand to Idan for context and confidence.

## Slide 19 — Intel and Context

**Presenter:** Idan · **Schedule:** 15:30–15:50

Negative findings, technique mapping, alternative explanations, open questions, and the verification process.

**Speaker guidance:** Connect the reported events and volume to a bounded assessment, with confidence tied to each claim.

## Slide 20 — Negative findings

**Presenter:** Idan · **Schedule:** 15:50–17:05

No clear brute-force or password-spray pattern; no svc_archsync VPN event; no matching external-IP Weblog path; no verified role, policy, or group addition. a.perl and svc_integrity were not linked to the main path. No process, service, or task event explained the network logons.

**Speaker guidance:** Negative findings apply to the reviewed evidence. Proxy records use src_host, limiting direct IP mapping. Missing execution telemetry remains inconclusive. Avoid describing comparison accounts as universally cleared.

## Slide 21 — ATT&CK mapping

**Presenter:** Idan · **Schedule:** 17:05–18:10

T1530 Data from Cloud Storage: supported by repeated retrieval. T1098.001 Additional Cloud Credentials: supported by the key-creation event, with persistence intent and ongoing use unresolved. T1083 File and Directory Discovery: a hypothesis prompted by configuration retrieval.

**Speaker guidance:** No confirmed Initial Access, Execution, or Privilege Escalation mapping. Reading a YAML object does not itself prove enumeration. Distinguish event support from tactic intent.

## Slide 22 — Alternative explanations

**Presenter:** Idan · **Schedule:** 18:10–19:30

Credential compromise and misuse of legitimate access remain open. Successful authentication is compatible with already-valid material, but does not identify acquisition. Workstation-origin service logons are compatible with both endpoint compromise and insider misuse.

**Speaker guidance:** Do not rank the hypotheses or assign equal numerical probabilities. Do not blame r.zohar personally, identify an attacker group, or infer malware execution.

## Slide 23 — Open questions and confidence

**Presenter:** Idan · **Schedule:** 19:30–20:40

Unknown: TOTP origin, IP ownership, personal-device activity, object contents, third-party posting, and current key validity. Source confidence: medium-high for anomalous use and retrieval; medium for possible persistence; low for initial access, operator, and motive.

**Speaker guidance:** Each unknown points to a collection need: MFA logs, ownership records, authorized forensics, manifests/content, customer evidence, or live IAM state. Confidence is qualitative.

## Slide 24 — AI verification and source corrections

**Presenter:** Idan · **Schedule:** 20:40–21:30

The source verification appendix records correction of baseline/incident count confusion, unreproduced volume, YAML misattribution, unsupported IP ownership, and unsupported escalation/entity claims. This English edition applies the reconciliations documented alongside the report.

**Speaker guidance:** AI assisted organization, queries, translation, and drafting. The source team describes verification against CSVs and context. Package preparation did not rerun those queries. Historical originals retain contradictions; use the English report with its reconciliation note. Hand back to Imri.

## Slide 25 — Response priorities

**Presenter:** Imri · **Schedule:** 21:30–22:50

Within 24 hours: contain implicated identities, revoke sessions/keys with approval, preserve evidence, review endpoints, and engage Legal/Privacy. Within 30 days: restrict service identity use, improve anomaly detection, review privileges/MFA and potentially exposed secrets. Long term: phishing-resistant MFA, managed-device access, retention, data classification/DLP, and key audits.

**Speaker guidance:** Recommendations are exercise outputs, not actions performed. Source authority tiers are retained in report §10. Containment can be proportionate without claiming IP ownership or operator identity.

## Slide 26 — High-severity assessment

**Presenter:** Imri · **Schedule:** 22:50–24:00

High severity reflects the Critical cloud asset, customer data, two accounts, prolonged retrieval, and possible persistence. The reported impact is confidentiality loss. Initial access, attribution, and containment remain unknown. No real-time alert is documented in the source findings.

**Speaker guidance:** Close with the evidence boundary introduced at the start. Route identity/timeline questions to Yarin, impact to Alon, context to Idan, and recommendations to Imri. Open discussion.

## Discussion guide

**Was the data posted externally?** The customer allegation remains unverified. The reported retrieval is established separately.

**Is r.zohar responsible personally?** Account activity is not personal attribution. Compromise and misuse remain open explanations.

**Is the key still active?** No matching revoke was found in the available data. Live IAM state is required.

**Why do GiB and GB differ?** They use different divisors for the same byte total. Both displayed values are rounded.

**Did the service logons happen if execution logs are missing?** The logons are reported; the mechanism explaining them remains unresolved.

**Can the queries be reproduced here?** The package supplies source queries and reviewed adaptations, but the raw exercise dataset is not included.
