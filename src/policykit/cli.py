"""policykit lint | soa | build"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .lint import errors, lint
from .model import PolicyKitError, load
from .site import build_site
from .soa import build_soa, to_csv, to_markdown


def _as_of(args) -> date:
    return date.fromisoformat(args.as_of) if args.as_of else date.today()


def cmd_lint(args) -> int:
    ws = load(args.root)
    findings = lint(ws, _as_of(args))
    for f in findings:
        print(f)
    n_err = len(errors(findings))
    print(f"\n{len(ws.policies)} policies, {n_err} error(s), {len(findings) - n_err} warning(s)")
    return 1 if n_err or (args.strict and findings) else 0


def cmd_soa(args) -> int:
    ws = load(args.root)
    rows = build_soa(ws)
    out = to_csv(rows) if args.format == "csv" else to_markdown(rows, ws.config["organization"])
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote SoA -> {args.output}")
    else:
        sys.stdout.write(out)
    return 0


def cmd_build(args) -> int:
    ws = load(args.root)
    as_of = _as_of(args)
    findings = lint(ws, as_of)
    if errors(findings):
        for f in errors(findings):
            print(f, file=sys.stderr)
        print("Fix lint errors before building the site.", file=sys.stderr)
        return 1
    out = build_site(ws, args.output, findings, as_of)
    print(f"Built policy site -> {out}/index.html")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="policykit", description="ISO/IEC 27001 policy-as-code toolkit")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp):
        sp.add_argument("--root", default=".", help="repository root containing policykit.yaml")
        sp.add_argument("--as-of", help="evaluate review dates as of YYYY-MM-DD (default: today)")

    lt = sub.add_parser("lint", help="check policies and the SoA")
    common(lt)
    lt.add_argument("--strict", action="store_true", help="fail on warnings as well as errors")
    lt.set_defaults(func=cmd_lint)

    so = sub.add_parser("soa", help="generate the Statement of Applicability")
    common(so)
    so.add_argument("--format", choices=["md", "csv"], default="md")
    so.add_argument("-o", "--output")
    so.set_defaults(func=cmd_soa)

    b = sub.add_parser("build", help="build the static policy site")
    common(b)
    b.add_argument("-o", "--output", default="site")
    b.set_defaults(func=cmd_build)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except PolicyKitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
