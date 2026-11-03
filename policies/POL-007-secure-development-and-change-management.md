---
id: POL-007
title: Secure Development and Change Management Policy
version: "1.3"
status: approved
owner: VP Engineering
approver: Chief Information Security Officer
approved_on: 2026-07-09
review_months: 12
classification: Internal
statement_prefix: SDC
iso27001_controls: ["A.8.4", "A.8.25", "A.8.26", "A.8.27", "A.8.28", "A.8.29", "A.8.31", "A.8.32", "A.8.33"]
related: [POL-002, POL-006, POL-008]
---

# Secure Development and Change Management Policy

## Purpose

To build security into how Northwind designs, codes, tests and changes software and infrastructure.

## Scope

All software and infrastructure-as-code developed by or for Northwind, and all changes to production systems.

## Policy statements

- **SDC-01** Security requirements shall be identified and recorded for every new feature that handles Confidential information or changes authentication.
- **SDC-02** New systems and major architecture changes shall undergo a threat model reviewed by the security team.
- **SDC-03** Source code shall be stored in the approved version-control platform, with write access limited to the owning team.
- **SDC-04** Default branches must be protected; every change requires at least one approving review from someone other than the author.
- **SDC-05** Code shall follow the secure coding standard, and automated static analysis and dependency scanning must run on every pull request.
- **SDC-06** Merges with unresolved critical or high-severity findings shall be blocked unless a time-limited exception is approved.
- **SDC-07** Development, test and production environments shall be separated, and developers must not have standing write access to production.
- **SDC-08** Production changes shall be deployed through the CI/CD pipeline with an auditable record of what changed, who approved it, and how to roll back.
- **SDC-09** Emergency changes shall be reviewed retrospectively within two business days.
- **SDC-10** Test data shall not include unmasked production personal data (see POL-004).

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| VP Engineering | Owns this policy and engineering standards |
| Engineering teams | Follow this policy; review each other's code |
| Application security | Threat models, tooling, secure coding training |

## Exceptions and enforcement

Exceptions to SDC-04 through SDC-08 require approval from the VP Engineering and the Head of Application Security, recorded on the change ticket.
