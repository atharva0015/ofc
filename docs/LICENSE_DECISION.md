# License decision: MIT

**Status:** decided and applied (2026-11-07). This file records the decision;
it is not legal advice. A qualified human must still complete the legal and
vendor review in `docs/HUMAN_SIGNOFF.md` before production use.

## Decision

The project is released under the **MIT License**.

- `LICENSE` contains the full MIT text.
- `pyproject.toml` declares `license = { text = "MIT" }`.
- The project owner approved MIT as the project license.

MIT was chosen because it is short, permissive, compatible with the
Apache-2.0 Healenium reuse, and suitable for a project that may be offered as
a commercial service. It does not impose copyleft obligations on users of the
healing framework.

## Dependency license policy

The project does not relicense its dependencies. `scripts/sbom.py` builds an
SBOM and checks every installed distribution against an allowlist:

- MIT, MIT-0, MIT-CMU
- Apache-2.0
- BSD-2-Clause, BSD-3-Clause
- ISC
- PSF-2.0
- MPL-2.0
- LGPL-3.0-only, LGPL-3.0-or-later

Run the fail-closed check with:

```powershell
python -m scripts.sbom --check
```

CI, `make sbom`, and `python tasks.py sbom` run the same command. Unknown
licenses and licenses outside the allowlist fail the check.

### Recorded exceptions

- **PyGithub (LGPL-3.0)** is kept as a development dependency for the GitOps
  client. It is not linked into the runtime package. If it is distributed,
  keep the LGPL notice and the ability to replace the library.
- **MPL-2.0** components are allowed only as separate, unmodified
  dependencies; file-level copyleft obligations stay with those files.
- **MIT-CMU** is the permissive CMU/MIT-style license used by Pillow. Pillow
  is not a project runtime dependency, but it can appear in developer
  environments through optional presentation tooling. Allowing it does not
  change the project's MIT terms.

The allowlist and exceptions were approved by the project owner on
2026-11-06 and extended with MIT-CMU on 2026-11-07.

## What this does and does not decide

This decides the **project's outbound license** and the **dependency license
allowlist**. It does not:

- approve a vendor, subprocessor, DPA, or data region (see
  `docs/COMPLIANCE.md` and P1.16);
- replace a human legal review;
- tick any box in `docs/HUMAN_SIGNOFF.md`;
- authorize a release or tag.

## Evidence

- `tests/test_sbom.py` — MIT metadata, normalization, OR/AND rules, and
  fail-closed `--check`.
- `reports/evidence/2026-11-07/sbom-check.txt` — 61/61 components allowed in
  the project venv, exit 0.
- `reports/evidence/2026-11-07/sbom-check-clean.txt` — 56/56 components
  allowed in a clean `pip install -e ".[dev]"` venv, exit 0.
- `reports/evidence/2026-11-07/pytest.txt` — full suite green.
