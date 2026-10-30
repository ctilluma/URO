# V.A.U.R.O.S. Core Library - URO (Universal Resource Orchestrator)
# Copyright (C) 2026 V.A.U.R.O.S. Swarm Collective
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


#!/usr/bin/env python3
# === FILE: phase0_patch.py ===
# PURPOSE:
#   Apply the Phase-0 patch via Exact Block Replacement (RFC 160 semantics).
#   Every edit verifies occurrence count == 1 in its target file and aborts
#   otherwise. No regex, no full-file rewrites.
#   Fixes:
#     1. tests/synapse_suite.py runner stringifies exceptions (str(exc)).
#     2. Project-root resolution in classify_modules.py, no_stub_audit.py,
#        bootstrap_session.py, and phase0_bootstrap.py: _BUILD ancestry first
#        (script location), git toplevel only as fallback. Git toplevel is the
#        multi-project repo, one level above the URO project directory.
#     3. STATE.md next-action pointer updated.
#     4. ADR-005 appended to DECISIONS.md (append-only log).
# RFC ANCHORS: 160 Editing Mandate; 1.4 Module Map hygiene.
# INVARIANTS: count-verified replacements only; abort on count != 1.
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import sys
from pathlib import Path
# === END: imports ===

# === START: constants ===
ROOT = Path(__file__).resolve().parent
EDITS = []
# === END: constants ===


# === START: edit_suite_runner ===
EDITS.append(("tests/synapse_suite.py", r'''        except Exception as exc:
            print("FAIL  " + name + " :: " + type(exc).__name__ + ": " + exc)
''', r'''        except Exception as exc:
            print("FAIL  " + name + " :: " + type(exc).__name__ + ": " + str(exc))
'''))
# === END: edit_suite_runner ===


# === START: edit_tools_root ===
OLD_TOOLS_ROOT = r'''def root():
    """PURPOSE: locate the repository root via git, else via _BUILD ancestry."""
    try:
        p = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return Path(p.stdout.strip())
    except Exception:
        pass
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    return here.parents[2] if len(here.parents) > 2 else here.parent
'''
NEW_TOOLS_ROOT = r'''def root():
    """PURPOSE: locate the project root via _BUILD ancestry, else via git."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    try:
        p = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return Path(p.stdout.strip())
    except Exception:
        pass
    return here.parents[2] if len(here.parents) > 2 else here.parent
'''
EDITS.append(("_BUILD/tools/classify_modules.py", OLD_TOOLS_ROOT, NEW_TOOLS_ROOT))
EDITS.append(("_BUILD/tools/no_stub_audit.py", OLD_TOOLS_ROOT, NEW_TOOLS_ROOT))
# === END: edit_tools_root ===


# === START: edit_bootstrap_root ===
EDITS.append(("_BUILD/tools/bootstrap_session.py", r'''def root():
    """PURPOSE: locate the repository root via git, else via _BUILD ancestry."""
    out = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if out:
        return Path(out)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    return here.parents[2] if len(here.parents) > 2 else here.parent
''', r'''def root():
    """PURPOSE: locate the project root via _BUILD ancestry, else via git."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    out = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if out:
        return Path(out)
    return here.parents[2] if len(here.parents) > 2 else here.parent
'''))
# === END: edit_bootstrap_root ===


# === START: edit_phase0_root ===
EDITS.append(("phase0_bootstrap.py", r'''    try:
        p = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return Path(p.stdout.strip())
    except Exception:
        pass
    return Path.cwd().resolve()
''', r'''    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    return Path.cwd().resolve()
'''))
# === END: edit_phase0_root ===


# === START: edit_state ===
EDITS.append(("_BUILD/STATE.md", r'''NEXT_ACTION: Run classify_modules.py, review CONFORMANCE_MATRIX.md, then start Phase 1 (primitives)
''', r'''NEXT_ACTION: Phase-0 patch applied; re-run classify + suite baseline, then start Phase 1 (primitives)
'''))
# === END: edit_state ===


# === START: adr_005 ===
ADR_005 = r'''
## ADR-005 - Phase-0 patch: project-root resolution and suite hardening
Date: 2026-10-29
Status: Accepted
Git toplevel is the multi-project repo (viridant-auraforge), one level above
the URO project directory. All _BUILD tools now resolve the project root via
_BUILD ancestry (script location), with git toplevel only as fallback. The
synapse suite runner stringifies exceptions so a single failure can never
crash the gate. Declared third-party deps (pydantic et al.) are environment
prerequisites, not code defects; install them before baseline runs.
'''
# === END: adr_005 ===


# === START: replace_once ===
def replace_once(path: Path, old: str, new: str) -> None:
    """PURPOSE: count-verified exact block replacement; abort unless count==1."""
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        print("ABORT: %s occurrence count %d != 1 for block: %r"
              % (path, count, old[:70]))
        raise SystemExit(2)
    path.write_text(text.replace(old, new), encoding="utf-8")
    print("patched: %s" % path)
# === END: replace_once ===


# === START: main ===
def main() -> int:
    """PURPOSE: apply all edits, append ADR-005, report result."""
    for rel, old, new in EDITS:
        replace_once(ROOT / rel, old, new)
    dec = ROOT / "_BUILD" / "DECISIONS.md"
    with dec.open("a", encoding="utf-8") as fh:
        fh.write(ADR_005)
    print("appended ADR-005 to %s" % dec)
    print("phase-0 patch complete.")
    return 0
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main())
