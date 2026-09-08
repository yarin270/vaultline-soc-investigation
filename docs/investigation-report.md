# Vaultline SOC investigation report

**Team E · Training simulation · English portfolio edition**

Vaultline Systems Ltd is the fictional organization in a SOC training scenario inspired by the 2022 LastPass attack. All case entities, dates, and findings here belong to the exercise. The investigation involved approximately **50,000 logs** and four investigators. This edition consolidates the supplied Hebrew report and full presentation, using their corrected findings. It does not represent a fresh examination of the raw dataset.

[Repository home](../README.md) · [Presentation](presentation.md) · [Evidence](../evidence/README.md) · [Queries](../queries/README.md) · [Reconciliation](source-reconciliation.md)

## 1. Executive summary

A customer reported finding archive records on a third-party website. No supporting source, URL, or screenshot was supplied, so the team treated the allegation as the investigation trigger. Publication on that site remains unverified.

The investigation identified sustained anomalous cloud retrieval using `r.zohar` and `svc_archsync` from `31.154.88.203`. The observed suspicious window runs from **2026-09-09 21:00:00 UTC to 2026-11-21 22:06:00 UTC**, described in the briefing as 73 days. The exact elapsed interval is 73 days, 1 hour, 6 minutes. These are scenario dates, not the date this portfolio was prepared.

The corrected total is **271 `get_object` retrieval events and 11,811,168,130 bytes**, or **11.00 GiB / 11.81 GB** rounded to two decimals. Of those events, 270 targeted customer data across 24 customer namespaces. One event retrieved an 8,140-byte internal configuration object. This is an event count, not a claim of 271 unique files or affected people.

The team's impact assessment establishes a confidentiality incident involving customer data and internal operational configuration in the Critical-rated `CLOUD-TENANT`. Integrity or availability impact was not established. The supplied report records 103 successful backup jobs and no observed `delete_object` operations, which do not by themselves establish complete recoverability or absence of unlogged changes.

Severity is **High** because of the critical cloud environment, customer data, two accounts, prolonged activity, and possible persistence. No real-time alert is documented in the supplied findings. Initial access, operator identity, and containment remain unknown. A new service-account access key was created on October 27 with no matching revocation found in the available window. Its current validity is unknown.

## 2. Scope, sources, and method

The exercise used Splunk and SPL to compare baseline behavior, correlate identities and timestamps, quantify retrievals, test alternative explanations, and record negative findings. The approved README identifies seven log families, with identity and asset context. The deck compresses this into six source categories and includes IAM as a category. IAM lifecycle findings here come from Cloud Audit operations and identity context; a separate IAM log export is not supplied in this package.

| Source family | Investigation purpose | Boundary |
|---|---|---|
| Cloud Audit | Object operations, accounts, source IPs, paths, byte counts, access-key lifecycle | Does not expose object contents or operator identity |
| VPN | Authentication, MFA result, session duration | A successful TOTP result does not identify who supplied it |
| Windows Event | Network logons and searches for process, service, task explanations | Raw timestamps are UTC+3; execution coverage is incomplete |
| File Audit | File-access context and latest reported coverage | Not a substitute for cloud-object totals |
| Backup | Reported job completion | Success does not prove a tested restore |
| Weblog | Search for the external IP and a possible web path | No matching path established |
| Proxy | Host-based traffic context | `src_host` prevents direct attribution from an external IP alone |
| Identity and asset lookups | Account roles, assigned workstation, asset criticality | No authoritative IP ownership or allowlist supplied |

The report places the earliest described baseline at August 27, 2026, 00:30 UTC and the latest coverage at November 24, 2026, 11:58:39 UTC. Coverage can differ by source. The deck cover's September 9 start describes neither the full baseline nor all source coverage and is not used as the overall window here.

**Evidence labels:** Confirmed means directly reported as supported by source events in the team's materials. Assessment means an interpretation of those events. Negative finding means the stated search did not locate supporting records. Unknown means the available material cannot resolve the question. Hypotheses do not become facts because several events are temporally close.

## 3. Entities and roles

| Entity | Role and observed relevance | Qualification |
|---|---|---|
| `r.zohar` | DevOps user, assigned to `WKS-ENG-01`; morning configuration retrieval and anomalous evening customer retrieval | Account activity does not establish personal culpability |
| `svc_archsync` | Archive replication service account; external customer retrieval and access-key creation | Possible misuse and persistence; current credential state unknown |
| `CLOUD-TENANT` | Critical cloud asset containing customer namespaces and internal configuration | Primary confidentiality impact |
| `WKS-ENG-01` | Medium-rated workstation; source of two service-account Type 3 logons | Endpoint compromise not proven |
| `SRV-BUILD` | High-rated server; destination of those logons | Endpoint compromise not proven |
| `31.154.88.203` | External source associated with anomalous cloud activity and `r.zohar` VPN authentication | Ownership and authorization unknown |
| `212.117.55.9` | Source of the stable morning configuration pattern and comparison rotation | Baseline context |
| `10.90.4.11`, `10.90.4.12`, `10.90.5.11` | Internal service replication sources | Excluded from suspicious retrieval volume; no supplied hostname mapping for `10.90.4.11` |
| `a.perl` | Administrative comparison account with revoke-then-create rotation | Not linked to the main incident path in corrected findings |
| `svc_integrity` | Comparison service account with routine integrity checks | Not linked to the external IP in the team's findings |

The internal object `/internal/config/archsync-runtime.yaml` is operationally relevant to the service-account investigation. Its name alone does not establish secrets, execution, or credential use.

## 4. Timeline

All times below are UTC. Original Windows local times are retained separately in the [timeline CSV](../evidence/timeline.csv). Source evidence IDs are those used in the report, not new event IDs.

| UTC | Observation | Source reference |
|---|---|---|
| Aug 27 00:30 | Internal `svc_archsync` replication baseline begins in described data | VL-E01 |
| Aug 27–Sep 8 | `r.zohar` retrieves small pipeline configuration objects around 07:12 and 08:18 | IA-E21 |
| Aug 30 08:00–08:03 | `a.perl` revokes an old key then creates a new one from `212.117.55.9` | IA-E15 |
| Sep 9 21:00:00 | First observed anomalous `r.zohar` customer retrieval from `31.154.88.203` | IA-E02, IA-E22 |
| Sep 9 21:40:01 | Successful `r.zohar` VPN authentication with TOTP; 195-minute session | IA-E01 |
| Sep 24 21:24 | `r.zohar` retrieves the 8,140-byte `archsync-runtime.yaml` object | VL-E03 |
| Sep 26 19:30 | `svc_archsync` Type 3 logon from `WKS-ENG-01` to `SRV-BUILD` | IA-E08 |
| Sep 26 21:00 | First observed external service-account `get_object` | IA-E06, IA-E07 |
| Oct 27 20:36 | Second Type 3 logon along the same workstation-to-server path | IA-E09 |
| Oct 27 22:09 | Service-account `create_access_key` from the external IP | IA-E14 |
| Nov 19 21:48 | Last reported suspicious service-account retrieval | VL-E04 |
| Nov 21 22:06 | Last reported suspicious retrieval overall, by `r.zohar` | VL-E05 |
| Nov 24 11:58:39 | Latest reported source coverage, in File Audit | VL-E06 |

## 5. Identity and access investigation

### 5.1 User behavior baseline

Between August 27 and September 8, `r.zohar` made small cloud `get_object` requests to `/internal/config/pipeline-X.yaml` from `212.117.55.9`, generally around 07:12 and 08:18 UTC. Reported sizes were 14,000–14,500 bytes. On September 9, the morning pattern continued, while a second pattern began at 21:00 from `31.154.88.203`.

The new pattern targeted `/cust-XXX/record-XXXX.dat` objects, with a reported 43,745,037 bytes per customer retrieval, in evening bursts at roughly six-minute intervals. Timing, source, object class, and size all deviated from the baseline. The concurrent morning and evening patterns support an anomaly finding. They do not prove two operators or determine whether credentials were stolen or intentionally misused. [IA-E21, IA-E22]

### 5.2 Authentication and the 40-minute gap

The VPN record reports successful TOTP-backed authentication at 21:40:01 UTC on September 9 from the same external IP, with a 195-minute session. Cloud retrieval had started at 21:00:00, **40 minutes and 1 second earlier**. This particular VPN session therefore cannot explain the already-observed cloud access. It remains a correlated observation, not a proven initial-access mechanism. How cloud credentials and the TOTP were obtained or used is unknown. [IA-E01–IA-E03, IA-E17]

### 5.3 Service-account baseline and deviation

The strongest observed service baseline is cyclical `replicate_object` activity from `10.90.4.11`, `10.90.4.12`, and `10.90.5.11`. The report describes 110 unique replication targets, roughly 20 MB of unique data, and about 1.83 GiB of cumulative repeated baseline traffic. Those approximate baseline measures are separate from the anomalous retrieval total. The reported 3,330 actions associated with `10.90.4.11` are also baseline context, not suspicious retrieval events. [IA-E04, IA-E05; report §5b]

On September 26 at 21:00 UTC, `svc_archsync` made its first **observed** external customer retrieval from `31.154.88.203`. External `get_object` activity differed from its internal replication role. No VPN event for this account was found; its direct connection to the external IP comes from Cloud Audit. [IA-E06, IA-E07, IA-E12, IA-E13]

### 5.4 Internal configuration and Windows correlation

`r.zohar`, not `svc_archsync`, retrieved `/internal/config/archsync-runtime.yaml` on September 24 at 21:24 UTC. The object was 8,140 bytes and belonged to the Critical cloud environment. This supports investigation of possible discovery and a transition to service-account use. The available material does not establish the object's contents, execution, secrets, or a causal connection to later service-account activity. [VL-E03, IA-E23]

Two successful Windows Event 4624 Type 3 logons used `svc_archsync` from `WKS-ENG-01` to `SRV-BUILD`. The source timestamps, September 26 22:30 and October 27 23:36 in UTC+3, normalize to 19:30 and 20:36 UTC. Type 3 means a network logon; the notable issue is the workstation source compared with the internal service infrastructure baseline. It does not itself prove RDP or a particular remote execution protocol. [IA-E08, IA-E09]

Searches for EventCodes 4688, 4697, 7045, 4698, 4699, and 4702 found no directly linked process, installed service, or scheduled task that explained these logons. No approved automation explanation was established. Missing explanatory records are a telemetry limitation, not proof that execution never occurred. [IA-E10, IA-E11]

### 5.5 Key lifecycle and privileges

On October 27 at 22:09 UTC, Cloud Audit recorded `create_access_key` for `svc_archsync` from `31.154.88.203`. No matching revocation was found in the available data. The comparison account `a.perl` showed a revoke-then-create sequence on August 30 from `212.117.55.9`. That comparison makes the service-account event worth investigating, but one comparison is not a universal requirement that every legitimate rotation must occur in exactly that order. [IA-E14–IA-E16]

The creation event is confirmed in the report. Malicious persistence remains an assessment, and present key validity requires live IAM evidence. No verified role, policy, or group addition established privilege escalation. Corrected findings do not link `a.perl` to the suspicious external-source key creation. [IA-E19]

## 6. Data and impact investigation

The incident metric is restricted to anomalous Cloud Audit `get_object` events from `31.154.88.203`. Baseline `replicate_object` traffic and normal morning configuration access are outside this total. The supplied report's corrected aggregate can be checked arithmetically:

```text
270 customer retrieval events × 43,745,037 bytes = 11,811,159,990 bytes
1 internal configuration retrieval × 8,140 bytes =         8,140 bytes
Total                                             11,811,168,130 bytes
Binary: total / 1,073,741,824 = 11.00 GiB (rounded)
Decimal: total / 1,000,000,000 = 11.81 GB (rounded)
```

| Account | Customer retrieval events | Internal retrieval events | Bytes derived from reported components | GiB rounded |
|---|---:|---:|---:|---:|
| `r.zohar` | 159, derived as 270 minus 111 | 1 | 6,955,469,023 | 6.48 |
| `svc_archsync` | 111, source-reported | 0 | 4,855,699,107 | 4.52 |
| Total | 270 | 1 | 11,811,168,130 | 11.00 |

The service account's reported customer scope spans `cust-007` through `cust-024`. Overall there are 24 customer namespaces plus the separate top-level `internal` namespace. The namespace count is not a verified count of legal customers or people requiring notification.

This arithmetic validates consistency of the supplied numbers. It does not rerun the Cloud Audit aggregation, prove uniqueness, or establish that every byte represents distinct information. The raw logs and full object manifest are not included.

### Impact assessment

- **Confidentiality:** the team's confirmed impact is anomalous retrieval of customer data and internal configuration from the Critical cloud tenant.
- **Integrity:** no `delete_object` operation was found. Modification or corruption through unobserved mechanisms cannot be ruled out.
- **Availability:** all 103 supplied backup jobs reportedly completed `SUCCESS`. No destructive impact or service outage was established; backup success alone does not demonstrate a restore test.
- **Potential exposure:** the internal YAML may contain operationally sensitive information, but its contents and use are unknown. Secret review and rotation are precautionary recommendations.
- **Current exposure:** the available window does not establish containment or the service key's present state. No production remediation is claimed.

## 7. Intel, negative findings, and alternative explanations

The report found no clear VPN brute-force or password-spray pattern. This is consistent with valid authentication material, but does not identify how it was acquired. The external IP appeared in VPN and Cloud Audit, without a matching Weblog path. Proxy records identify source hosts rather than providing a direct external-IP attribution. No separate web intrusion or proxy transfer route was proven. [IA-E20, CTX-E02]

`a.perl` and `svc_integrity` were examined as comparisons and were not linked to the principal incident path. This is a bounded investigation result, not a universal certification that those identities could never be involved in other activity.

Two explanations remain open: external credential compromise, and misuse of legitimate access, potentially involving an unmanaged personal device. The workstation association is consistent with either a compromised endpoint or insider misuse. The evidence does not rank these explanations, assign numerical probabilities, identify a threat group, or establish that the named account owner performed the actions personally.

## 8. ATT&CK mapping and detection gaps

These are the team's evidence-based mappings, with event confidence separated from intent. They are not claims of a complete attack chain.

| Technique | Evidence and mapping | Limit |
|---|---|---|
| T1530, Data from Cloud Storage | Repeated cloud `get_object` retrieval supports Collection | Third-party publication remains unverified |
| T1098.001, Additional Cloud Credentials | Service-account key creation supports the credential-addition mapping | Persistence intent and continued usability are not directly established |
| T1083, File and Directory Discovery | Report's hypothesis prompted by internal configuration retrieval | A retrieval alone does not prove enumeration; retain as a hypothesis |

Valid-account abuse is a descriptive assessment. No initial-access, execution, or privilege-escalation technique is asserted as confirmed. There is no proven ransomware, encryption, backup destruction, or malware execution finding.

The source materials document no real-time alert for the suspicious activity. A complete alert inventory or detection denominator is not supplied, so no detection rate is calculated. Detection opportunities include new external sources, service-account access from workstations, multi-namespace retrieval, internal configuration access, and anomalous key lifecycle changes. See [query guidance](../queries/README.md) for the distinction between retrospective searches and deployed detections.

## 9. Unresolved questions and confidence

| Question | Evidence needed to resolve it |
|---|---|
| How did initial cloud access occur? | Earlier authentication, session, IAM, endpoint, and cloud history |
| Who supplied the TOTP? | MFA provider events, enrolled-device records, and user interview |
| Who owned or was authorized to use the external IP? | Corporate NAT/allowlist records and time-specific provider allocation records |
| What happened on the workstation or personal device? | Authorized endpoint forensics, browser and authenticator evidence |
| What was inside retrieved objects and who was affected? | Storage manifests, data classification, and controlled content review |
| Was anything published on the reported third-party site? | Customer-supplied source and preserved external evidence, coordinated with Legal/Privacy |
| Was the new key revoked, and is the incident contained? | Live IAM state, key identifiers, complete lifecycle history, and later logs |
| Was the YAML used to obtain service-account access? | Object content and credential-use evidence with matching identities and times |

The source assessment gives **medium-high** confidence to anomalous account use and retrieval, **medium** to possible persistence, and **low** to initial access, actor identity, and motive. The exact full incident duration may extend outside the available window. These confidence labels are qualitative judgments, not statistical probabilities.

## 10. Response recommendations

These are exercise recommendations, not completed actions or legal determinations. Authority labels reflect the source report's scenario, not universal permission to act in a real organization.

| Priority | Recommendation | Source authority / finding |
|---|---|---|
| Within 24 hours | Temporarily disable the two implicated accounts, revoke sessions and keys, then reissue after validating ownership and business need | Approval required; IA-E01, IA-E14, CTX-E04 |
| Within 24 hours | Block or challenge the external IP at VPN/cloud controls and monitor recurrence without asserting ownership | Tier 1 in source; IA-E18, CTX-E02 |
| Within 24 hours | Preserve IAM/cloud/VPN/EDR evidence; investigate `WKS-ENG-01` and `SRV-BUILD`; engage Legal/Privacy on the customer report | Management/legal; IA-E08–IA-E11, CTX-E01 |
| Within 30 days | Replace long-lived service credentials with a short-lived workload identity restricted to approved infrastructure; prevent workstation/interactive use | Approval required; IA-E04–IA-E07 |
| Within 30 days | Add alerts for unusual retrieval volume, new external sources, multiple customer namespaces, internal configuration access, and unexplained key creation | Tier 1 in source; IA-E06, IA-E14–IA-E16 |
| Within 30 days | Review permissions for both implicated accounts and `a.perl`; review MFA devices and rotate secrets potentially exposed in the YAML after identifying them | Approval required; VL-E03, IA-E17, IA-E19 |
| Long term | Adopt phishing-resistant MFA, managed-device conditional access, and an enforceable BYOD policy | Management/legal; authentication and personal-device gaps |
| Long term | Extend retention and collection for IAM, MFA, cloud access, and service-account execution, with shared change identifiers | Management; IA-E10–IA-E11, CTX-E04 |
| Long term | Classify archive data, evaluate DLP and retrieval limits, and periodically review service accounts and long-lived keys | Management/legal; data scope and asset criticality |

## 11. Team and AI disclosure

Imri led case framing, synthesis, and recommendations. Yarin Greenberg handled Identity & Access, including baselines, account correlation, Windows time normalization, and the timeline. Alon covered Data & Impact. Idan covered Intel & Context, mapping, hypotheses, and confidence.

The report's AI verification appendix describes assistance with evidence organization, query suggestions, template translation, and drafting. It also records errors: mixing baseline counts with incident totals, misattributing the YAML, unsupported IP ownership, and an unsupported privilege-escalation/entity claim. The team reports checking new claims against CSVs, lookups, and briefing material. This portfolio preparation used those supplied findings, translated and reconciled them, and checked arithmetic and links; it did not independently execute the investigation queries.

## 12. Supporting material

- [Evidence register and excerpts](../evidence/README.md)
- [Machine-readable reported metrics](../evidence/reported-metrics.json)
- [SPL queries and field assumptions](../queries/README.md)
- [Full presentation](presentation.md)
- [Reconciliation and source precedence](source-reconciliation.md)
- [Original sources and hashes](../original-files/README.md)
