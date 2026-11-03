---
id: POL-005
title: Information Security Incident Management Policy
version: "2.0"
status: approved
owner: Head of Security Operations
approver: Chief Information Security Officer
approved_on: 2026-05-05
review_months: 12
classification: Internal
statement_prefix: IRP
iso27001_controls: ["A.5.24", "A.5.25", "A.5.26", "A.5.27", "A.5.28", "A.6.8"]
related: [POL-001, POL-008, POL-009]
---

# Information Security Incident Management Policy

## Purpose

To detect, report, assess and respond to information security events and incidents quickly and consistently, and to learn from them.

## Scope

All suspected or confirmed security events affecting Northwind information, systems, staff or suppliers.

## Severity levels

| Severity | Definition | Response target |
|---|---|---|
| SEV-1 | Confirmed breach of Confidential data or major outage of the e-commerce platform | Incident lead engaged within 30 minutes, 24/7 |
| SEV-2 | Contained compromise or significant control failure | Within 4 hours |
| SEV-3 | Suspicious activity or minor policy breach | Next business day |

## Policy statements

- **IRP-01** Northwind shall maintain an incident response plan, with named roles and contact details, that is tested at least annually.
- **IRP-02** All staff and contractors must report suspected security events to the security team immediately through the incident channel or service desk.
- **IRP-03** Reported events shall be triaged, assigned a severity and recorded in the incident register within the response target for that severity.
- **IRP-04** SEV-1 and SEV-2 incidents shall have a named incident lead and a documented timeline of actions and decisions.
- **IRP-05** The DPO shall assess every incident involving personal data for regulatory notification obligations, which may apply within 72 hours.
- **IRP-06** Evidence shall be collected and preserved in a way that maintains its integrity and chain of custody.
- **IRP-07** A blameless post-incident review shall be completed within 10 business days of closing any SEV-1 or SEV-2 incident, with tracked corrective actions.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Head of Security Operations | Owns this policy, the plan and the incident register |
| Incident lead | Coordinates response, communication and recovery |
| Data Protection Officer | Decides on regulator and data-subject notification |
| All staff | Report events promptly and preserve evidence |

## Exceptions and enforcement

This policy has no exceptions for reporting. Failing to report a known incident may result in disciplinary action.
