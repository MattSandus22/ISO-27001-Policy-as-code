---
id: POL-009
title: Business Continuity and Backup Policy
version: "1.0"
status: approved
owner: Head of Platform Engineering
approver: Chief Operating Officer
approved_on: 2025-09-15
review_months: 12
classification: Internal
statement_prefix: BCP
iso27001_controls: ["A.5.29", "A.5.30", "A.8.13", "A.8.14"]
related: [POL-005, POL-008]
---

# Business Continuity and Backup Policy

## Purpose

To keep Northwind's critical services available, and its information recoverable, during and after disruption.

## Scope

The e-commerce platform, payment and order systems, and the corporate services they depend on.

## Recovery objectives

| Service tier | Recovery time objective | Recovery point objective |
|---|---|---|
| Tier 1: checkout, payments, orders | 4 hours | 15 minutes |
| Tier 2: customer support, catalogue | 24 hours | 4 hours |
| Tier 3: corporate tools | 72 hours | 24 hours |

## Policy statements

- **BCP-01** A business impact analysis shall set recovery objectives for each service tier and be reviewed annually.
- **BCP-02** Tier 1 services shall run across at least two availability zones, with automated failover.
- **BCP-03** Backups shall meet each tier's recovery point objective, be encrypted, and be stored in a separate account from the source data.
- **BCP-04** Backup restores shall be tested at least quarterly for Tier 1 and annually for other tiers, with results recorded.
- **BCP-05** Information security controls must remain in place during disruption; temporary workarounds must be risk-assessed and time-limited.
- **BCP-06** The continuity plan shall be exercised at least annually, and lessons learned shall be tracked to completion.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Chief Operating Officer | Approves recovery objectives |
| Head of Platform Engineering | Owns this policy, resilience design and backups |
| Service owners | Maintain recovery runbooks and join exercises |

## Exceptions and enforcement

A service that cannot meet its tier objectives must be recorded as a risk in the risk register with an owner and treatment plan.
