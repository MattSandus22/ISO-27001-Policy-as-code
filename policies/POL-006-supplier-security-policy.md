---
id: POL-006
title: Supplier Security Policy
version: "1.1"
status: approved
owner: Procurement Lead
approver: Chief Information Security Officer
approved_on: 2026-06-18
review_months: 12
classification: Internal
statement_prefix: SSP
iso27001_controls: ["A.5.19", "A.5.20", "A.5.21", "A.5.22", "A.5.23", "A.8.30"]
related: [POL-004, POL-007]
---

# Supplier Security Policy

## Purpose

To manage the security risk that suppliers, cloud providers and outsourced developers introduce when they access or process Northwind information.

## Scope

All suppliers that access Northwind systems, process Northwind information, or provide services that the e-commerce platform depends on, including AI model and SaaS providers.

## Policy statements

- **SSP-01** Suppliers shall be tiered by the classification of information they handle and their criticality to the platform.
- **SSP-02** Tier 1 suppliers (Confidential data or critical services) must complete a security assessment, and provide a current SOC 2 Type II or ISO/IEC 27001 certificate, before contract signature.
- **SSP-03** Contracts shall include security, confidentiality, breach-notification, audit and data-return requirements proportionate to the supplier tier.
- **SSP-04** Cloud services shall be approved by the security team before use, with the shared-responsibility model documented for each.
- **SSP-05** Suppliers shall be required to flow equivalent security obligations down to their own subcontractors.
- **SSP-06** Tier 1 suppliers shall be reassessed annually, and all suppliers whenever their service or data access changes materially.
- **SSP-07** Outsourced development shall follow the secure development requirements in POL-007, and its output must pass Northwind's security testing before release.
- **SSP-08** Supplier access shall be removed and data returned or destroyed when the contract ends.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Procurement Lead | Owns this policy and the supplier register |
| Security team | Performs assessments and approves cloud services |
| Contract owners | Monitor supplier performance and changes |
| Legal | Maintains standard security contract clauses |

## Exceptions and enforcement

Using a Tier 1 supplier before assessment requires written CISO risk acceptance with an expiry date. Unapproved cloud services may be blocked.
