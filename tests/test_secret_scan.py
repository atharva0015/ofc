"""Secret scanning must fail closed and catch a seeded credential."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scripts import secret_scan

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "heal-pr.yml"
HAS_GITLEAKS = bool(os.getenv("GITLEAKS_BIN"))


def test_find_binary_prefers_explicit_env(tmp_path, monkeypatch) -> None:
    binary = tmp_path / "gitleaks.exe"
    binary.write_text("", encoding="utf-8")
    monkeypatch.setenv("GITLEAKS_BIN", str(binary))
    assert secret_scan.find_binary() == str(binary)


def test_find_binary_missing_is_none(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("GITLEAKS_BIN", str(tmp_path / "missing.exe"))
    assert secret_scan.find_binary() is None


def test_missing_binary_fails_closed(monkeypatch, capsys) -> None:
    monkeypatch.setattr(secret_scan, "find_binary", lambda: None)
    assert secret_scan.scan() == 2
    assert "not found" in capsys.readouterr().err


def test_scan_command_is_redacted_and_fail_closed(tmp_path) -> None:
    command = secret_scan.scan_command("gitleaks", "git", tmp_path)
    assert command[:3] == ["gitleaks", "git", str(tmp_path)]
    assert "--redact" in command
    assert command[command.index("--exit-code") + 1] == "7"
    assert str(secret_scan.CONFIG) in command


def test_workflow_uses_pinned_gitleaks_not_grep() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "grep -rniE" not in text
    assert "gitleaks_8.30.1_linux_x64.tar.gz" in text
    assert "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb" in text
    assert "python -m scripts.secret_scan --self-test" in text
    assert "python -m scripts.secret_scan" in text


@pytest.mark.skipif(not HAS_GITLEAKS, reason="set GITLEAKS_BIN to run gitleaks")
def test_self_test_detects_seeded_secret() -> None:
    assert secret_scan.self_test() == 0


@pytest.mark.skipif(not HAS_GITLEAKS, reason="set GITLEAKS_BIN to run gitleaks")
def test_repository_history_is_clean() -> None:
    assert secret_scan.scan(mode="git") == 0
