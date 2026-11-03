---
id: POL-002
title: Access Control Policy
version: "1.4"
status: approved
owner: Head of IT
approver: Chief Information Security Officer
approved_on: 2026-04-02
review_months: 12
classification: Internal
statement_prefix: ACP
iso27001_controls: ["A.5.15", "A.5.16", "A.5.17", "A.5.18", "A.8.2", "A.8.3", "A.8.5", "A.8.18"]
related: [POL-001, POL-007]
---

# Access Control Policy

## Purpose

To make sure people and services can access only the information and systems they need, and that access is granted, reviewed and removed in a controlled way.

## Scope

All user, administrator and service accounts on Northwind systems, including cloud consoles, SaaS applications and source-code repositories.

## Policy statements

- **ACP-01** Access shall be granted on the principles of least privilege and need to know, based on role.
- **ACP-02** Every account shall be uniquely attributable to one person or one named service; shared accounts must not be used.
- **ACP-03** Access requests shall be approved by the information asset owner before access is provisioned.
- **ACP-04** Multi-factor authentication shall be required for all remote access, all cloud and SaaS consoles, and all privileged accounts.
- **ACP-05** Passwords shall be at least 14 characters and must not appear on known breached-password lists.
- **ACP-06** Privileged access shall be granted just in time where the platform supports it, and otherwise held in separate admin accounts.
- **ACP-07** Asset owners shall review user access every quarter for Confidential systems and every six months for other systems.
- **ACP-08** Access shall be removed within one business day of a leaver's last working day, and adjusted within five business days of a role change.
- **ACP-09** Service-account credentials shall be stored in the approved secrets manager and rotated at least every 90 days, or replaced with short-lived credentials.
- **ACP-10** Use of utility programs that can override system or application controls shall be restricted to named administrators and logged.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Head of IT | Owns identity platforms and this policy |
| Information asset owners | Approve access and perform access reviews |
| Line managers | Raise joiner, mover and leaver requests on time |
| Security team | Monitor privileged activity and audit compliance |

## Exceptions and enforcement

Exceptions require CISO approval through the security exception process and must be recorded with a compensating control and an expiry date. Unapproved access may be revoked immediately.
