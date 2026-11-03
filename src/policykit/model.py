"""Load configuration, policies (Markdown with YAML front matter) and the SoA."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from importlib import resources
from pathlib import Path

import yaml

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
# A policy statement is a list item that starts with a bold ID, e.g. "- **ACP-03** Users shall ..."
STATEMENT = re.compile(r"^\s*[-*]\s+\*\*([A-Z]{2,5}-\d{2,3})\*\*\s+(.+)$", re.MULTILINE)

DEFAULT_CONFIG = {
    "organization": "Example Organization",
    "policies_dir": "policies",
    "soa_file": "soa.yaml",
    "default_review_months": 12,
    "required_sections": [
        "Purpose",
        "Scope",
        "Policy statements",
        "Roles and responsibilities",
        "Exceptions and enforcement",
    ],
}


class PolicyKitError(Exception):
    pass


@lru_cache(maxsize=None)
def annex_a() -> dict:
    return yaml.safe_load(resources.files("policykit").joinpath("data/annex_a_2022.yaml").read_text())


def control_ids() -> list[str]:
    return list(annex_a()["controls"])


def control_title(cid: str) -> str:
    return annex_a()["controls"][cid]


def theme(cid: str) -> str:
    return annex_a()["themes"][cid.split(".")[0]]


def as_date(value) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def add_months(d: date, months: int) -> date:
    y, m = divmod(d.month - 1 + months, 12)
    year, month = d.year + y, m + 1
    days_in_month = [31, 29 if year % 4 == 0 and (year % 100 or year % 400 == 0) else 28,
                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    return date(year, month, min(d.day, days_in_month))


@dataclass
class Statement:
    id: str
    text: str


@dataclass
class Policy:
    path: Path
    meta: dict
    body: str
    statements: list[Statement] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.path.stem))

    @property
    def status(self) -> str:
        return str(self.meta.get("status", ""))

    @property
    def controls(self) -> list[str]:
        return [str(c).removeprefix("A.") for c in self.meta.get("iso27001_controls", [])]

    @property
    def approved_on(self) -> date | None:
        try:
            return as_date(self.meta.get("approved_on"))
        except ValueError:
            return None

    def review_months(self, config: dict) -> int:
        return int(self.meta.get("review_months", config["default_review_months"]))

    def next_review(self, config: dict) -> date | None:
        return add_months(self.approved_on, self.review_months(config)) if self.approved_on else None


def parse_policy(path: Path) -> Policy:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return Policy(path, {}, text)
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        raise PolicyKitError(f"{path}: invalid front matter: {exc}") from exc
    if not isinstance(meta, dict):
        meta = {}
    body = text[m.end():]
    return Policy(
        path=path,
        meta=meta,
        body=body,
        statements=[Statement(sid, txt.strip()) for sid, txt in STATEMENT.findall(body)],
        sections=[h.strip() for h in HEADING.findall(body)],
    )


@dataclass
class Workspace:
    root: Path
    config: dict
    policies: list[Policy]
    soa: dict  # control id -> {"applicable": bool, "justification": str, "addressed_by": str}

    def by_id(self) -> dict[str, Policy]:
        return {p.id: p for p in self.policies if p.id}


def load(root: str | Path = ".") -> Workspace:
    root = Path(root)
    cfg_file = root / "policykit.yaml"
    config = dict(DEFAULT_CONFIG)
    if cfg_file.exists():
        config.update(yaml.safe_load(cfg_file.read_text()) or {})
    pdir = root / config["policies_dir"]
    if not pdir.is_dir():
        raise PolicyKitError(f"policies directory not found: {pdir}")
    policies = [parse_policy(p) for p in sorted(pdir.glob("*.md"))]
    soa_path = root / config["soa_file"]
    soa_raw = (yaml.safe_load(soa_path.read_text()) or {}) if soa_path.exists() else {}
    soa = {}
    for cid, entry in (soa_raw.get("controls") or {}).items():
        entry = entry or {}
        soa[str(cid).removeprefix("A.")] = {
            "applicable": entry.get("applicable", True),
            "justification": " ".join(str(entry.get("justification") or "").split()),
            "addressed_by": str(entry.get("addressed_by") or "").strip(),
        }
    return Workspace(root, config, policies, soa)
