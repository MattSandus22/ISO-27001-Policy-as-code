"""Lint rules for the policy set and Statement of Applicability."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from .model import Workspace, as_date, control_ids

STATUSES = ("draft", "approved", "retired")
REQUIRED_META = ("id", "title", "version", "owner", "status", "statement_prefix", "iso27001_controls")
POLICY_ID = re.compile(r"^POL-\d{3}$")
NORMATIVE = re.compile(r"\b(shall|must)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    level: str  # error | warning
    ref: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.ref}: {self.message}"


def addressed_controls(ws: Workspace) -> dict[str, list[str]]:
    """Control id -> ids of *approved* policies that address it."""
    out: dict[str, list[str]] = defaultdict(list)
    for p in ws.policies:
        if p.status == "approved":
            for c in p.controls:
                out[c].append(p.id)
    return out


def lint(ws: Workspace, as_of: date | None = None) -> list[Finding]:
    as_of = as_of or date.today()
    findings: list[Finding] = []
    err = lambda ref, msg: findings.append(Finding("error", ref, msg))  # noqa: E731
    warn = lambda ref, msg: findings.append(Finding("warning", ref, msg))  # noqa: E731
    known = set(control_ids())
    ids = [p.id for p in ws.policies if p.id]
    statement_owner: dict[str, str] = {}

    for p in ws.policies:
        ref = p.id or p.path.name
        if not p.meta:
            err(p.path.name, "missing YAML front matter")
            continue
        for f in REQUIRED_META:
            if p.meta.get(f) in (None, "", []):
                err(ref, f"missing required front-matter field '{f}'")
        if p.id and not POLICY_ID.match(p.id):
            err(ref, "policy id must look like POL-001")
        if ids.count(p.id) > 1:
            err(ref, "duplicate policy id")
        if p.id and not p.path.name.startswith(p.id):
            warn(ref, f"file name '{p.path.name}' should start with the policy id")
        if p.status and p.status not in STATUSES:
            err(ref, f"status must be one of {', '.join(STATUSES)}")

        # Annex A mappings. YAML reads an unquoted 5.10 as the number 5.1, so require strings.
        for c in p.meta.get("iso27001_controls") or []:
            if not isinstance(c, str):
                err(ref, f"control {c!r} must be a quoted string such as \"A.5.10\"")
            elif c.removeprefix("A.") not in known:
                err(ref, f"unknown ISO/IEC 27001:2022 Annex A control '{c}'")

        # Approval and review
        try:
            approved_on = as_date(p.meta.get("approved_on"))
        except ValueError:
            err(ref, "approved_on must be a date (YYYY-MM-DD)")
            approved_on = None
        if p.status == "approved":
            if not p.meta.get("approver"):
                err(ref, "approved policy has no approver")
            if not approved_on:
                err(ref, "approved policy has no approved_on date")
            elif approved_on > as_of:
                err(ref, f"approved_on {approved_on} is in the future")
            else:
                due = p.next_review(ws.config)
                if due and due < as_of:
                    warn(ref, f"annual review overdue: approved {approved_on}, "
                              f"review every {p.review_months(ws.config)} months, due {due}")
        if p.meta.get("owner") and p.meta.get("owner") == p.meta.get("approver"):
            warn(ref, "owner and approver are the same person (no independent approval)")

        # Structure
        for section in ws.config["required_sections"]:
            if section not in p.sections:
                warn(ref, f"missing required section '## {section}'")

        # Statements
        prefix = p.meta.get("statement_prefix")
        if p.status != "retired" and not p.statements:
            warn(ref, "no policy statements found (use '- **PREFIX-01** text')")
        for s in p.statements:
            if s.id in statement_owner:
                err(ref, f"statement {s.id} is already used in {statement_owner[s.id]}")
            statement_owner[s.id] = ref
            if prefix and not s.id.startswith(f"{prefix}-"):
                err(ref, f"statement {s.id} does not use this policy's prefix '{prefix}'")
            if not NORMATIVE.search(s.text):
                warn(ref, f"statement {s.id} has no 'shall' or 'must'; it may not be a testable requirement")

        for rel in p.meta.get("related") or []:
            if rel not in ids:
                err(ref, f"related policy '{rel}' does not exist")

    # Statement of Applicability
    addressed = addressed_controls(ws)
    for cid in ws.soa:
        if cid not in known:
            err("soa", f"unknown control '{cid}'")
    for cid in control_ids():
        entry = ws.soa.get(cid, {"applicable": True, "justification": "", "addressed_by": ""})
        ref = f"A.{cid}"
        if not entry["applicable"]:
            if not entry["justification"]:
                err(ref, "excluded from the SoA without a justification")
            if addressed.get(cid):
                warn(ref, f"excluded from the SoA but addressed by {', '.join(addressed[cid])}")
        elif not addressed.get(cid) and not entry["addressed_by"]:
            warn(ref, "applicable but not addressed by any approved policy or documented procedure")

    return findings


def errors(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.level == "error"]
