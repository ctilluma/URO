#!/usr/bin/env python3
# === FILE: _BUILD/tools/no_stub_audit.py ===
# PURPOSE:
#   Final-gate audit. Scan the URO package for forbidden residue:
#   NotImplementedError, TODO/FIXME/XXX markers, SCAFFOLD( markers,
#   _CompatStub references, and empty modules. Report mode by default;
#   pass --gate to exit non-zero when findings or open scaffolds remain.
# RFC ANCHORS: 16 compliance checklist; 160 editing mandate.
# INVARIANTS: read-only; never edits source.
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
# === END: imports ===

# === START: constants ===
BUILD = "_BUILD"
PATTERNS = [
    ("NotImplementedError", re.compile(r"NotImplementedError")),
    ("TODO", re.compile(r"#\s*TODO")),
    ("FIXME", re.compile(r"#\s*FIXME")),
    ("XXX", re.compile(r"#\s*XXX")),
    ("SCAFFOLD marker", re.compile(r"SCAFFOLD\(")),
    ("_CompatStub", re.compile(r"_CompatStub")),
]
# === END: constants ===


# === START: root ===
def root():
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
# === END: root ===


# === START: main ===
def main():
    """PURPOSE: scan for stub residue and report; fail when --gate is set."""
    gate = "--gate" in sys.argv
    r = root()
    pkg = r / "uro"
    findings = []
    if pkg.exists():
        for path in sorted(pkg.rglob("*.py")):
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(r).as_posix()
            if not text.strip():
                findings.append((rel, 0, "EMPTY MODULE"))
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                for label, rx in PATTERNS:
                    if rx.search(line):
                        findings.append((rel, lineno, label))
    open_scaf = 0
    ledger = r / BUILD / "SCAFFOLD_LEDGER.md"
    if ledger.exists():
        open_scaf = sum(1 for l in ledger.read_text(encoding="utf-8").splitlines()
                        if "[OPEN]" in l.upper() and "[DONE]" not in l.upper())
    print("no_stub_audit: %d code findings, %d open scaffold ledger entries"
          % (len(findings), open_scaf))
    for rel, lineno, label in findings[:200]:
        print("  %s:%d %s" % (rel, lineno, label))
    if len(findings) > 200:
        print("  ... and %d more" % (len(findings) - 200))
    if gate and (findings or open_scaf):
        print("GATE FAILED: stubs or open scaffolds remain.")
        return 1
    print("audit complete.")
    return 0
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main())
