# Evidence register

[Home](../README.md) · [Full report](../docs/investigation-report.md) · [Queries](../queries/README.md)

This register transcribes or summarizes findings from the supplied report and deck. **It is not a raw event export, fabricated log dataset, or newly executed query output.** EV identifiers are unique package locators. IA/VL/CTX identifiers belong to the report and may be reused there. Source S1 is the Hebrew report, S2 the HTML deck, S3 the script, all in [original-files](../original-files/README.md).

| ID | Source locator | Reported evidence | Interpretation boundary |
|---|---|---|---|
| EV01 | S1 §4, §5a, Appendix C; IA-E21; S2 §7–8 | Morning configuration retrieval from 212.117.55.9 continued after Sep 9 | Does not establish operator count |
| EV02 | S1 Appendix C; IA-E02/IA-E22; S2 §8–9 | Sep 9 21:00 r.zohar customer get_object from 31.154.88.203 | Earliest observed anomaly, not initial access |
| EV03 | S1 Appendix C; IA-E01; S2 §9 | Sep 9 21:40:01 VPN success, TOTP, 195-minute session | Who supplied TOTP unknown |
| EV04 | S1 §5a; IA-E04/IA-E05; S2 §7 | Internal cyclical service replication from three 10.x addresses | Baseline excluded from incident total |
| EV05 | S1 Appendix C; VL-E03; S2 §10 | Sep 24 21:24 r.zohar retrieves archsync-runtime.yaml, 8140 bytes | Contents and use unknown |
| EV06 | S1 Appendix C; IA-E08; S2 §10 | Sep 26 22:30 UTC+3 Type 3 from WKS-ENG-01 to SRV-BUILD | Normalized 19:30 UTC; no execution mechanism proven |
| EV07 | S1 §4, §5a; IA-E06/IA-E07; S2 §10 | Sep 26 21:00 first observed external svc_archsync get_object | Does not prove the YAML caused access |
| EV08 | S1 Appendix C; IA-E09; S2 §10 | Oct 27 23:36 UTC+3 second Type 3 on same path | Normalized 20:36 UTC |
| EV09 | S1 §4, Appendix C; IA-E14–IA-E16; S2 §11 | Oct 27 22:09 svc_archsync create_access_key, external source; no matching revoke found | Key validity and persistence intent unresolved |
| EV10 | S1 §4, §5a, Appendix A; IA-E15; S2 §11 | a.perl revoke/create comparison from 212.117.55.9 | Corrects older external-IP attribution |
| EV11 | S1 §5b, §7, Appendix B Q1; S2 §14–16 | 271 events, 24 customer namespaces plus internal, 11,811,168,130 bytes | Event count and cumulative retrieval bytes, not distinct files |
| EV12 | S1 §5a; IA-E10/IA-E11; S2 §10, §20 | No directly explanatory process/service/task event located | Telemetry gap |
| EV13 | S1 §5a; IA-E12/IA-E13/IA-E20; S2 §20 | No service VPN event and no clear guessing pattern | Limited negative finding |
| EV14 | S1 §5c; CTX-E02; S2 §20 | No matching external-IP Weblog path; Proxy uses src_host | No separate web/proxy route proven |
| EV15 | S1 §5c; CTX-E03; S2 §17 | 103 supplied successful backup jobs; no delete_object found | Restore readiness and full integrity not proven |
| EV16 | S1 §4, Appendix C; VL-E04–VL-E06; S2 §12 | Last service retrieval Nov 19; last overall Nov 21; coverage ends Nov 24 | End of observation is not containment |
| EV17 | S1 §5c; CTX-E01 | CLOUD-TENANT Critical, SRV-BUILD High, WKS-ENG-01 Medium | Asset ratings are not proof of host compromise |

## Selected source-reported excerpts

The following normalized transcriptions retain only fields explicitly quoted by S1 Appendix C. They are excerpts from the report, not byte-for-byte raw CSV lines.

| UTC | Account | Source IP | Operation / target | Reported size |
|---|---|---|---|---:|
| 2026-09-09 21:00 | r.zohar | 31.154.88.203 | get_object /cust-001/record-0000.dat | 43,745,037 bytes |
| 2026-09-09 21:06 | r.zohar | 31.154.88.203 | get_object /cust-002/record-0001.dat | 43,745,037 bytes |
| 2026-09-09 21:12 | r.zohar | 31.154.88.203 | get_object /cust-003/record-0002.dat | 43,745,037 bytes |
| 2026-09-09 21:18 | r.zohar | 31.154.88.203 | get_object /cust-004/record-0003.dat | 43,745,037 bytes |
| 2026-09-24 21:24 | r.zohar | 31.154.88.203 | get_object /internal/config/archsync-runtime.yaml | 8,140 bytes |

The access-key target quoted by the report is `/iam/users/svc_archsync/keys/new`. This is an object path, not a disclosed secret or a usable access-key value. It does not provide a stable key identifier sufficient for a definitive lifecycle join.

## Machine-readable companions

- [Timeline CSV](timeline.csv): reported observations and original Windows times, with account and host direction separated.
- [Reported metrics JSON](reported-metrics.json): source-reported measures and explicitly derived components.
- [Scenario entities](scenario-entities.csv): investigation pivots, not a production threat-intelligence blocklist.

All IPs, accounts, and paths are exercise entities. Do not treat these indicators as malicious infrastructure in a live environment.
