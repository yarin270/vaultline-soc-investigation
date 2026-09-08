# Source reconciliation

[Home](../README.md) · [Report](investigation-report.md) · [Originals](../original-files/README.md)

The English edition is a reconciled portfolio adaptation, not a literal translation of every sentence. It uses the approved README and explicit user corrections, the updated report's event-level findings and AI verification appendix, and the full 26-slide HTML deck. The Hebrew script supports timing and presentation flow. No raw CSVs were supplied for this packaging pass, so source-reported observations cannot be independently re-queried here.

| Topic | Source inconsistency or overstatement | English edition treatment |
|---|---|---|
| Dataset size | Other portfolios have different datasets | Approximately 50,000 logs, as confirmed by the user. No dataset generated |
| Incident count | “Objects/files” sometimes stands in for events | 271 retrieval events; distinct-file count not established |
| Data scope | 25 namespaces can read as 25 customers | 270 customer events across 24 namespaces, plus one internal event |
| Volume | Older 110-object / 11.26 GB claims; one report passage also calls 11 GiB unreproduced | Corrected byte total 11,811,168,130, or 11.00 GiB / 11.81 GB; 110 is baseline replication uniqueness |
| Account split | 111 “files”; derived 159 sometimes presented as direct data | 111 source-reported service-account customer retrievals; 159 derived user customer retrievals plus one internal retrieval |
| Morning activity | “Baseline breaks” can imply replacement | Normal morning behavior continued alongside the evening anomaly |
| Initial access | VPN is an appealing but later event | First observed cloud retrieval precedes this VPN success by 40m 1s; initial access unknown |
| YAML attribution | Earlier report material blamed `svc_archsync` | `r.zohar` retrieved the YAML; contents, execution, secrets and subsequent use unknown |
| Account transition | Deck says “pivots” as an established causal chain | Sequence is observed; a causal transition through the YAML is a hypothesis |
| Windows path | Incomplete timeline cells can obscure direction | `WKS-ENG-01` source to `SRV-BUILD` destination; Type 3 is a network logon |
| Time zones | Source SPL sometimes parses `_time` as text | Raw Windows UTC+3 is normalized once; reviewed queries use already-correct epoch `_time` and document ingestion prerequisites |
| Access keys | Older §5b links `a.perl` creation to external IP | Corrected identity section and Appendix A place `a.perl` rotation at `212.117.55.9`; principal suspicious creation is `svc_archsync` |
| Rotation interpretation | Deck calls no revoke proof of persistence | Credential creation is reported fact; persistence intent and present validity remain unresolved |
| Privilege escalation | Earlier `a.pearl` and T1078.004 escalation claim | `a.pearl` is a rejected entity; no verified role/policy/group addition or escalation |
| Attribution | “Attacker-owned IP”; personal blame; equal-weight hypotheses | IP ownership unknown; no personal attribution; alternatives remain unranked rather than statistically equal |
| Negative findings | “Cleared,” “clean,” “no alert fired” can sound absolute | Not linked in reviewed evidence; no destructive impact established; no real-time alert documented |
| Backups | Script says none skipped | 103 supplied jobs completed SUCCESS; scheduling completeness and restoration are not proven |
| Sources | Deck says six categories including IAM; README lists seven log families | Seven log families with identity/asset context; no separate IAM export inferred |
| Coverage | HTML cover begins Sep 9; baseline begins Aug 27 | Earliest described baseline Aug 27 00:30, latest coverage Nov 24 11:58:39; coverage may vary by source |
| Calendar dates | Report header 02/09/2026; deck header 03 Sep 2026 precede November events | Preserve historical originals; do not reuse those headers as incident completion dates |
| Duration | “Exactly 73 days” in notes | 73-day headline; exact elapsed interval 73d 1h 6m, not an inclusive calendar-day count |
| Event IDs | IA-E21/IA-E22 reused for different themes in report | Keep locators with named source sections; package register has unique EV identifiers |
| Original distribution note | Deck §24 says source sections remain unreconciled | English edition addresses known contradictions in this table; historical originals still contain them |

Remaining material gaps are substantive: raw logs, object manifest/content, key identifiers and live state, MFA evidence, IP ownership, endpoint forensics, external-posting evidence, and a verified submission/completion date. They are not filled with generated data.

Repository structure was inspired by [Shaharhal's Meridian portfolio](https://github.com/Shaharhal/soc-final-project-meridian). Its README and recursive directory tree were inspected via the GitHub connector, at tree commit `5856f247255f5ce673e64eff0b4a916cb1848e50`. Its report/presentation/original-file organization informed completeness only. No Meridian incident findings, raw data, or wording were transferred.
