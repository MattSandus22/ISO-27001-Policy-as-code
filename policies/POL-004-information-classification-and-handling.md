---
id: POL-004
title: Information Classification and Handling Policy
version: "1.2"
status: approved
owner: Data Protection Officer
approver: Chief Information Security Officer
approved_on: 2026-02-14
review_months: 12
classification: Internal
statement_prefix: ICH
iso27001_controls: ["A.5.9", "A.5.12", "A.5.13", "A.5.14", "A.5.33", "A.5.34", "A.7.10", "A.8.10", "A.8.11", "A.8.12"]
related: [POL-003, POL-006]
---

# Information Classification and Handling Policy

## Purpose

To classify information by sensitivity and define how each class is labelled, stored, shared, retained and destroyed, including personal data.

## Scope

All information created, received or processed by Northwind in any form, and the assets that store it.

## Classification levels

| Level | Examples | Minimum handling |
|---|---|---|
| Public | Marketing site, published prices | No restrictions |
| Internal | Policies, org charts, most email | Northwind staff and approved contractors only |
| Confidential | Customer PII, payment data, source code, contracts | Named access, encrypted at rest and in transit |

## Policy statements

- **ICH-01** An inventory of information assets shall be maintained, with an owner and classification for each.
- **ICH-02** Information owners shall classify information as Public, Internal or Confidential; unclassified information must be treated as Internal.
- **ICH-03** Confidential documents shall be labelled, and Confidential systems shall be identified as such in the asset inventory.
- **ICH-04** Confidential information must be encrypted when stored on removable media or sent outside Northwind, using approved tools only.
- **ICH-05** Personal data shall be processed only for documented purposes and in line with the privacy notice and data-protection law.
- **ICH-06** Records shall be retained according to the retention schedule and protected against loss, falsification and unauthorized release.
- **ICH-07** Information shall be securely deleted when no longer needed, and media shall be wiped or destroyed using approved methods.
- **ICH-08** Production personal data must not be used in non-production environments unless it has been masked or anonymised.
- **ICH-09** Data-leakage prevention controls shall monitor email and cloud storage for unauthorized transfer of Confidential information.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Data Protection Officer | Owns this policy, the retention schedule and privacy compliance |
| Information owners | Classify their information and approve sharing |
| All staff | Handle information according to its classification |

## Exceptions and enforcement

Exceptions require approval from the DPO and CISO. Mishandling Confidential information is a security incident and must be reported under POL-005.
