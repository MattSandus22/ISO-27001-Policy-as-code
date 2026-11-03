---
id: POL-008
title: Operations Security Policy
version: "1.5"
status: approved
owner: Head of Platform Engineering
approver: Chief Information Security Officer
approved_on: 2026-08-25
review_months: 12
classification: Internal
statement_prefix: OPS
iso27001_controls: ["A.8.6", "A.8.7", "A.8.8", "A.8.9", "A.8.15", "A.8.16", "A.8.17", "A.8.20", "A.8.21", "A.8.22", "A.8.24", "A.8.34"]
related: [POL-005, POL-007, POL-009]
---

# Operations Security Policy

## Purpose

To operate Northwind's platforms securely: hardened configuration, timely patching, protective monitoring, network segmentation and correct use of cryptography.

## Scope

All production and corporate infrastructure, cloud accounts, networks and endpoints.

## Vulnerability remediation targets

| Severity (CVSS) | Internet-facing | Internal |
|---|---|---|
| Critical (9.0+) | 7 days | 14 days |
| High (7.0–8.9) | 14 days | 30 days |
| Medium (4.0–6.9) | 60 days | 90 days |

## Policy statements

- **OPS-01** Systems shall be built from hardened, version-controlled configuration baselines, and drift from baseline must be detected.
- **OPS-02** Capacity of critical services shall be monitored, with alerts before limits are reached.
- **OPS-03** Endpoint and server malware protection shall be installed, updated automatically and centrally monitored.
- **OPS-04** All systems shall be scanned for vulnerabilities at least weekly, and findings must be remediated within the targets in this policy.
- **OPS-05** Security-relevant events shall be logged centrally, protected from tampering, and retained for at least 12 months.
- **OPS-06** Logs and alerts shall be monitored to detect anomalous behaviour, with critical alerts triaged within 30 minutes.
- **OPS-07** All systems shall synchronise their clocks to the approved time source.
- **OPS-08** Networks shall be segmented so that production, corporate and guest networks are isolated, and only required traffic is permitted between them.
- **OPS-09** Network services shall have documented security requirements, and administrative interfaces must not be exposed to the internet.
- **OPS-10** Confidential data shall be encrypted in transit with TLS 1.2 or higher and at rest with AES-256 or equivalent, with keys managed in the approved key-management service.
- **OPS-11** Audit and penetration testing on production systems shall be planned and agreed with the system owner to avoid disrupting operations.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Head of Platform Engineering | Owns this policy and infrastructure baselines |
| Security operations | Monitoring, alert triage, vulnerability scanning |
| System owners | Remediate vulnerabilities within target |

## Exceptions and enforcement

Vulnerabilities that cannot be fixed within target need a risk-accepted exception from the CISO with compensating controls and an expiry date.
