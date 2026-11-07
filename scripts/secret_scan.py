"""Fail-closed secret scanning with gitleaks.

This replaces the former grep heuristic in `.github/workflows/heal-pr.yml`.
The wrapper is deliberately small: it locates a pinned gitleaks binary, runs it
with the checked-in `.gitleaks.toml`, and maps the result to a clear exit code.

Modes:
  git (default)  scan every commit in the repository history
  dir            scan the current working tree

Exit codes:
  0  no leaks
  1  leaks found (gitleaks exit code 7 is remapped)
  2  gitleaks is missing, self-test failed, or the scanner errored

A missing scanner is an error, never a silent pass: an unobserved check must
not look green.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "8.30.1"
ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".gitleaks.toml"

# A synthetic AWS-shaped key, assembled at runtime so this source file does not
# itself look like a credential. The suffix uses the AWS rule's Base32 alphabet
# and deliberately avoids the "EXAMPLE" placeholder that gitleaks allowlists.
# It is not a real secret.
_SEEDED_KEY = "AKIA" + "Z7X3Q5W2E5R4T2Y4"


def find_binary() -> str | None:
    """Return the gitleaks binary from GITLEAKS_BIN or PATH, else None."""
    configured = os.getenv("GITLEAKS_BIN")
    if configured:
        path = Path(configured)
        return str(path) if path.is_file() else None
    return shutil.which("gitleaks")


def scan_command(binary: str, mode: str, target: Path, config: Path = CONFIG) -> list[str]:
    """Build the gitleaks command line used by CI and local runs."""
    return [
        binary,
        mode,
        str(target),
        "--config",
        str(config),
        "--redact",
        "--no-banner",
        "--log-level",
        "error",
        "--exit-code",
        "7",
    ]


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def scan(target: Path = ROOT, mode: str = "git", config: Path = CONFIG) -> int:
    """Scan a path and return 0 (clean), 1 (leaks), or 2 (scanner error)."""
    binary = find_binary()
    if binary is None:
        print(
            f"gitleaks {VERSION} not found. Install it on PATH or set GITLEAKS_BIN.\n"
            "CI installs the pinned release in .github/workflows/heal-pr.yml.",
            file=sys.stderr,
        )
        return 2

    proc = _run(scan_command(binary, mode, target, config))
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)

    if proc.returncode == 0:
        print(f"gitleaks {mode} scan: clean ({target})")
        return 0
    if proc.returncode == 7:
        print(f"gitleaks {mode} scan: LEAKS FOUND ({target})", file=sys.stderr)
        return 1
    print(f"gitleaks {mode} scan: scanner error (exit {proc.returncode})", file=sys.stderr)
    return 2


def _write(repo: Path, name: str, text: str) -> None:
    (repo / name).write_text(text, encoding="utf-8")


def _findings(binary: str, target: Path, config: Path) -> int:
    report = target / "gitleaks-report.json"
    command = [
        *scan_command(binary, "dir", target, config),
        "--report-format",
        "json",
        "--report-path",
        str(report),
    ]
    proc = _run(command)
    if proc.returncode not in (0, 7):
        raise RuntimeError(f"gitleaks self-test scan failed with exit {proc.returncode}")
    data = json.loads(report.read_text(encoding="utf-8") or "[]")
    return len(data)


def self_test(config: Path = CONFIG) -> int:
    """Prove the scanner and config catch a seeded secret and pass a clean file."""
    binary = find_binary()
    if binary is None:
        print(
            f"gitleaks {VERSION} not found. Install it on PATH or set GITLEAKS_BIN.",
            file=sys.stderr,
        )
        return 2

    with tempfile.TemporaryDirectory(prefix="gitleaks-selftest-") as tmp:
        root = Path(tmp)
        dirty = root / "dirty"
        clean = root / "clean"
        dirty.mkdir()
        clean.mkdir()
        _write(dirty, "settings.py", f'AWS_ACCESS_KEY_ID = "{_SEEDED_KEY}"\n')
        _write(clean, "app.py", 'import os\n\nprint("hello")\nprint(os.getenv("HOME"))\n')

        try:
            dirty_count = _findings(binary, dirty, config)
            clean_count = _findings(binary, clean, config)
        except (RuntimeError, json.JSONDecodeError) as exc:
            print(f"self-test: ERROR: {exc}", file=sys.stderr)
            return 2

    if dirty_count < 1:
        print("self-test: FAIL - seeded AWS key was not detected", file=sys.stderr)
        return 2
    if clean_count != 0:
        print(f"self-test: FAIL - clean control reported {clean_count} finding(s)", file=sys.stderr)
        return 2
    print(f"self-test: PASS - detected {dirty_count} seeded finding(s); clean control passed")
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("git", "dir"), default="git")
    parser.add_argument(
        "--self-test", action="store_true", help="prove a seeded secret is detected"
    )
    args = parser.parse_args(argv)

    if args.self_test:
        raise SystemExit(self_test())
    raise SystemExit(scan(mode=args.mode))


if __name__ == "__main__":
    main()
