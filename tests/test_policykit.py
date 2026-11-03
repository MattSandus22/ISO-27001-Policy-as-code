import shutil
from datetime import date
from pathlib import Path

import pytest

from policykit.cli import main
from policykit.lint import errors, lint
from policykit.model import add_months, annex_a, control_ids, load, parse_policy
from policykit.site import build_site
from policykit.soa import build_soa, to_csv

ROOT = Path(__file__).parent.parent
AS_OF = date(2026, 11, 3)


@pytest.fixture
def repo(tmp_path):
    """A writable copy of the sample policy repository."""
    for name in ("policykit.yaml", "soa.yaml"):
        shutil.copy(ROOT / name, tmp_path / name)
    shutil.copytree(ROOT / "policies", tmp_path / "policies")
    return tmp_path


def edit(path: Path, old: str, new: str):
    text = path.read_text()
    assert old in text, f"{old!r} not in {path.name}"
    path.write_text(text.replace(old, new, 1))


def refs(findings, level=None):
    return [f"{f.ref}: {f.message}" for f in findings if level is None or f.level == level]


def test_catalog_has_93_controls_in_4_themes():
    ids = control_ids()
    assert len(ids) == 93 and len(set(ids)) == 93
    counts = {t: sum(c.startswith(f"{t}.") for c in ids) for t in "5678"}
    assert counts == {"5": 37, "6": 8, "7": 14, "8": 34}
    assert set(annex_a()["themes"].values()) == {"Organizational", "People", "Physical", "Technological"}


def test_sample_repo_lints_with_expected_findings():
    findings = lint(load(ROOT), AS_OF)
    assert errors(findings) == []
    assert {f.ref for f in findings} == {"POL-009", "A.5.7"}


def test_parse_policy_extracts_statements_and_sections():
    p = parse_policy(ROOT / "policies" / "POL-002-access-control-policy.md")
    assert p.id == "POL-002" and p.status == "approved"
    assert [s.id for s in p.statements][:3] == ["ACP-01", "ACP-02", "ACP-03"]
    assert len(p.statements) == 10
    assert "Policy statements" in p.sections


def test_unquoted_control_ids_are_rejected(repo):
    # YAML parses 5.10 as the float 5.1, silently mapping the wrong control.
    edit(repo / "policies/POL-003-acceptable-use-policy.md", '"A.5.10", ', "5.10, ")
    assert any("quoted string" in m for m in refs(lint(load(repo), AS_OF), "error"))


def test_unknown_control(repo):
    edit(repo / "policies/POL-002-access-control-policy.md", '"A.8.18"', '"A.8.35"')
    assert any("unknown ISO/IEC 27001:2022 Annex A control" in m for m in refs(lint(load(repo), AS_OF)))


def test_approved_policy_needs_approver_and_date(repo):
    edit(repo / "policies/POL-002-access-control-policy.md", "approver: Chief Information Security Officer\n", "")
    edit(repo / "policies/POL-002-access-control-policy.md", "approved_on: 2026-04-02\n", "")
    errs = refs(lint(load(repo), AS_OF), "error")
    assert any("no approver" in m for m in errs)
    assert any("no approved_on" in m for m in errs)


def test_future_approval_date_is_error(repo):
    edit(repo / "policies/POL-002-access-control-policy.md", "approved_on: 2026-04-02", "approved_on: 2027-04-02")
    assert any("in the future" in m for m in refs(lint(load(repo), AS_OF), "error"))


def test_draft_policies_do_not_count_toward_soa(repo):
    # A.5.34 is addressed by POL-004 (approved) and POL-010 (draft). Remove it from POL-004.
    edit(repo / "policies/POL-004-information-classification-and-handling.md", ', "A.5.34"', "")
    findings = lint(load(repo), AS_OF)
    assert any(f.ref == "A.5.34" and "not addressed" in f.message for f in findings)


def test_exclusion_requires_justification(repo):
    edit(repo / "soa.yaml", "  A.7.11:\n    applicable: false\n    justification: >",
         "  A.7.11:\n    applicable: false\n    old_justification: >")
    assert any(f.ref == "A.7.11" for f in errors(lint(load(repo), AS_OF)))


def test_excluding_an_addressed_control_warns(repo):
    (repo / "soa.yaml").write_text((repo / "soa.yaml").read_text() +
                                   "  A.8.15:\n    applicable: false\n    justification: test\n")
    assert any(f.ref == "A.8.15" and "excluded" in f.message for f in lint(load(repo), AS_OF))


def test_statement_rules(repo):
    path = repo / "policies/POL-012-physical-security-policy.md"
    edit(path, "**PHY-08**", "**ACP-01**")  # wrong prefix and duplicate of POL-002
    edit(path, "- **PHY-07** Equipment shall be placed", "- **PHY-07** Equipment is placed")
    findings = lint(load(repo), AS_OF)
    msgs = refs(findings)
    assert any("already used" in m for m in msgs)
    assert any("does not use this policy's prefix" in m for m in msgs)
    assert any("PHY-07 has no 'shall' or 'must'" in m for m in msgs)


def test_missing_section_and_bad_related(repo):
    path = repo / "policies/POL-006-supplier-security-policy.md"
    edit(path, "## Scope", "## Applicability")
    edit(path, "related: [POL-004, POL-007]", "related: [POL-004, POL-099]")
    msgs = refs(lint(load(repo), AS_OF))
    assert any("missing required section '## Scope'" in m for m in msgs)
    assert any("POL-099" in m for m in msgs)


def test_owner_equals_approver_warns(repo):
    edit(repo / "policies/POL-002-access-control-policy.md",
         "approver: Chief Information Security Officer", "approver: Head of IT")
    assert any("no independent approval" in m for m in refs(lint(load(repo), AS_OF), "warning"))


def test_add_months_handles_month_ends():
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)
    assert add_months(date(2027, 2, 28), 12) == date(2028, 2, 28)
    assert add_months(date(2026, 11, 3), 14) == date(2028, 1, 3)


def test_soa_rows():
    rows = {r.control: r for r in build_soa(load(ROOT))}
    assert len(rows) == 93
    assert rows["A.7.11"].status == "Excluded"
    assert rows["A.5.7"].status == "Gap"
    assert rows["A.5.37"].status == "Addressed" and rows["A.5.37"].other
    assert rows["A.5.10"].policies == ["POL-003"]  # POL-010 is draft
    assert to_csv(list(rows.values())).count("\n") == 94


def test_site_build(tmp_path):
    out = build_site(load(ROOT), tmp_path / "site", [], AS_OF)
    assert (out / "index.html").exists() and (out / "soa.html").exists()
    page = (out / "policies" / "POL-002.html").read_text()
    assert 'id="ACP-04"' in page and "../soa.html#A.5.15" in page


def test_cli(repo):
    root = ["--root", str(repo), "--as-of", "2026-11-03"]
    assert main(["lint", *root]) == 0
    assert main(["lint", *root, "--strict"]) == 1
    assert main(["build", *root, "-o", str(repo / "site")]) == 0
    assert main(["soa", *root, "--format", "csv", "-o", str(repo / "soa.csv")]) == 0
    edit(repo / "policies/POL-002-access-control-policy.md", "status: approved", "status: final")
    assert main(["lint", *root]) == 1
    assert main(["build", *root, "-o", str(repo / "site2")]) == 1
