#!/usr/bin/env python3
# === FILE: _BUILD/tools/bootstrap_session.py ===
# PURPOSE:
#   Emit a fully aware initial prompt bundle for any new chat session so the
#   session can be cloned/resumed from repository state. Reads git evidence
#   and the _BUILD project memory, prints the bundle to stdout, and saves it
#   to _BUILD/generated/session_context_bundle.md.
# RFC ANCHORS: project-wide continuity; supports 160 rollout discipline.
# INVARIANTS: read-only with respect to git and library source; never
#   overwrites _BUILD docs; only writes under _BUILD/generated/.
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path
# === END: imports ===

# === START: constants ===
BUILD = "_BUILD"
# === END: constants ===


# === START: run ===
def run(cmd, cwd):
    """PURPOSE: run a git command safely and return stripped stdout text."""
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=60)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""
# === END: run ===


# === START: root ===
def root():
    """PURPOSE: locate the project root via _BUILD ancestry, else via git."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    out = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if out:
        return Path(out)
    return here.parents[2] if len(here.parents) > 2 else here.parent
# === END: root ===


# === START: read ===
def read(path):
    """PURPOSE: read a text file, returning empty string when absent."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""
# === END: read ===


# === START: main ===
def main():
    """PURPOSE: assemble and emit the full-awareness resume bundle."""
    r = root()
    b = r / BUILD
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    state = read(b / "STATE.md")
    phase = "unknown"
    for line in state.splitlines():
        if line.startswith("CURRENT_PHASE:"):
            phase = line.split(":", 1)[1].strip()
    ledger = read(b / "SCAFFOLD_LEDGER.md")
    open_scaf = [l for l in ledger.splitlines()
                 if "[OPEN]" in l.upper() and "[DONE]" not in l.upper()]
    ckpt = read(b / "CHECKPOINTS" / (phase + ".md"))
    git_bits = "\n".join([
        "branch: " + (run(["git", "branch", "--show-current"], r) or "unknown"),
        "head: " + (run(["git", "log", "-1", "--pretty=%h %ad %s", "--date=iso"], r) or "unknown"),
        "last tag: " + (run(["git", "describe", "--tags", "--abbrev=0"], r) or "none"),
        "dirty files: " + str(len(run(["git", "status", "--porcelain"], r).splitlines())),
        "recent commits:",
        run(["git", "log", "--oneline", "-10"], r) or "(none)",
    ])
    parts = [
        "# URO BUILD - FULL-AWARENESS SESSION PROMPT",
        "Generated: " + now,
        "Repo: " + str(r),
        "",
        "INSTRUCTIONS TO ASSISTANT: read every section before responding.",
        "Continue from CURRENT STATE. Honor locked decisions, the 160 Editing",
        "Mandate, and the no-stub commenting contract. Update _BUILD/STATE.md",
        "and the phase checkpoint after meaningful progress. Never delete ADRs.",
        "",
        "## 1. SESSION BOOTSTRAP", read(b / "SESSION_BOOTSTRAP.md"),
        "", "## 2. DECISIONS (ADR LOG)", read(b / "DECISIONS.md"),
        "", "## 3. CURRENT STATE", state,
        "", "## 4. OPEN SCAFFOLDS", "\n".join(open_scaf) or "No open scaffolds.",
        "", "## 5. CURRENT PHASE CHECKPOINT (" + phase + ")", ckpt or "No checkpoint yet.",
        "", "## 6. GIT EVIDENCE", git_bits,
        "", "## 7. MASTER PLAN", read(b / "MASTER_PLAN.md"),
        "", "## 8. TARGET TREE", read(b / "TARGET_TREE.md"),
        "", "## 9. REGRESSION MATRIX", read(b / "REGRESSION_MATRIX.md"),
        "", "## 10. CONFORMANCE MATRIX", read(b / "CONFORMANCE_MATRIX.md"),
        "", "END OF BUNDLE. Begin by restating the current phase and next action.",
    ]
    bundle = "\n".join(parts)
    outdir = b / "generated"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "session_context_bundle.md").write_text(bundle, encoding="utf-8")
    print(bundle)
    print("[bootstrap_session] saved: " + str(outdir / "session_context_bundle.md"),
          file=sys.stderr)
    return 0
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main())
