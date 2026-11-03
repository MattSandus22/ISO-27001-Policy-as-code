---
id: POL-0XX                     # next free number; file name must start with this id
title: Example Policy
version: "0.1"                  # quote it, so 1.10 is not read as 1.1
status: draft                   # draft | approved | retired
owner: Role that owns the policy
approver: Role that approves it  # must differ from owner
approved_on:                    # YYYY-MM-DD, required once approved
review_months: 12
classification: Internal
statement_prefix: EXP           # 2-5 capital letters, unique across policies
iso27001_controls: ["A.5.1"]    # quote every control id
related: []                     # other policy ids
---

# Example Policy

## Purpose

Why this policy exists, in one or two sentences.

## Scope

Who and what it applies to.

## Policy statements

- **EXP-01** Each statement shall be a single, testable requirement that uses "shall" or "must".
- **EXP-02** Give every statement a stable id. Never renumber; retire ids instead, so audit evidence keeps pointing at the right requirement.

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| Owner | Maintains this policy |

## Exceptions and enforcement

How exceptions are requested and approved, and the consequence of non-compliance.
