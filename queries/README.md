# SPL investigation query pack

[Home](../README.md) · [Evidence register](../evidence/README.md) · [Report](../docs/investigation-report.md)

**Execution status: not run in this package preparation.** Source files reproduce the seven queries in S1 Appendix B. Reviewed files are newly adapted retrospective searches, not exported historical queries, verified result sets, or deployed detections. Raw logs, Splunk configuration, and lookup CSVs are not included.

## Original report appendix

| Query | Source purpose | Review note |
|---|---|---|
| [Source 01](source-01-scope.spl) | Count retrievals, namespaces, bytes | No explicit success predicate; inspect result distribution before calling every row successful |
| [Source 02](source-02-vpn.spl) | User VPN details | Requires correctly parsed time and fields |
| [Source 03](source-03-windows-time-original.spl) | Windows normalization | Parses `_time` as a string; standard Splunk `_time` is epoch. Historical query retained, not recommended unchanged |
| [Source 04](source-04-key-lifecycle.spl) | Compare key creation and revocation | Listing events does not establish present key state |
| [Source 05](source-05-execution-gap.spl) | Process, service, scheduled-task search | Zero results require telemetry and field checks |
| [Source 06](source-06-backup-delete.spl) | Backup success and delete counts | Does not prove complete coverage or restore readiness |
| [Source 07](source-07-user-baseline-original.spl) | Timing, targets, byte sizes | Uses `bytes`, while corrected aggregation uses `bytes_out`; resolve against schema |

## Reviewed adaptations and expected source findings

| Query | Improvement | Source-reported expectation, not a new result |
|---|---|---|
| [Reviewed 01](reviewed-01-scope.spl) | Separates event count from distinct paths; checks numeric byte coverage and unclassified namespaces | 271 events, 270 customer, 1 internal, 24 customer namespaces, 11,811,168,130 bytes. Distinct paths were not independently established |
| [Reviewed 02](reviewed-02-account-split.spl) | Groups actor and customer/internal scope | svc_archsync: 111 customer events; r.zohar: derived 159 customer plus 1 internal |
| [Reviewed 03](reviewed-03-correlated-timeline.spl) | Uses already-normalized epoch time and preserves host direction | First cloud retrieval precedes VPN by 40m 1s; Windows logons at 19:30 and 20:36 UTC |
| [Reviewed 04](reviewed-04-baseline.spl) | Separates operations and target classes; uses canonical byte field | Morning pipeline pattern coexists with evening customer retrieval; replication stays separate |
| [Reviewed 05](reviewed-05-key-lifecycle.spl) | Leaves lifecycle events visible for manual review | a.perl comparison rotation; svc_archsync creation with no matching revoke reported |
| [Reviewed 06](reviewed-06-negative-checks.spl) | Constrains backup/delete counts to their source families | 103 supplied successful backup jobs and no delete_object reported |

## Field and time prerequisites

1. Set the search window to the complete available exercise coverage. Reported coverage starts Aug 27 and ends Nov 24, 2026; validate first/last times per source rather than assuming continuous coverage.
2. Set the search user's display timezone to UTC. Configure Windows ingestion for its documented UTC+3 timestamps, and the other described sources for UTC. `_time` must already be the correct epoch before using reviewed queries. Do not subtract three hours a second time.
3. For manual normalization checks only: `2026-09-26 22:30:00 +0300` corresponds to `2026-09-26 19:30:00Z`; `2026-10-27 23:36:00 +0300` corresponds to `2026-10-27 20:36:00Z`. Avoid a regex that assumes a CSV timestamp always begins at byte zero.
4. Validate `actor` (cloud/Windows), `user` (VPN), `src_ip`, `src_host`, `host`, `target_object`, `operation`, `EventCode`, `logon_type`, and `bytes_out`. Some original searches use `bytes` or `target`. Do not silently coalesce fields unless their meanings and units match.
5. Confirm bytes are numeric, nonnegative, and populated for all retrieval events. A sum silently ignoring nulls is incomplete. The reviewed queries expose numeric-value coverage but do not prove field correctness.
6. Inspect result/status values and extraction before adding a success filter. The source aggregate query omits a result predicate; changing its population could change the total. Compare all retrieval events against successful ones and document any difference.
7. Check duplicates and collection overlap before deduplicating. Preserve event identifiers and ingestion provenance. `dc(target_object)` is a separate metric and does not replace event count or prove unique content.
8. For key lifecycle closure, obtain stable key IDs and complete IAM history. A generic `/keys/new` path and an actor-level event list are not sufficient to prove a specific key remained active.

## Detection development

These retrospective searches motivate detections for service-account access from new external sources, unusual customer-namespace breadth, internal configuration access, workstation-origin service logons, and unexplained key creation. Thresholds and schedules must come from the organization's baseline, authorized changes, and telemetry latency. No numeric production threshold, false-positive rate, detection success, or deployed alert is claimed here.

Before deployment, test with the real schema and retained data, include legitimate rotation and approved maintenance cases, and verify timezone parsing and missing-field handling. The package verifier checks files and arithmetic only; it does not compile or execute SPL.
