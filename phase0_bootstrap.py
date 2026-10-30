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
# === FILE: phase0_bootstrap.py ===
# PURPOSE:
#   One-shot writer for the URO build-out Phase-0 deliverable set.
#   Creates the repository-hosted continuity system (_BUILD/), the build
#   tooling (bootstrap_session.py, classify_modules.py, no_stub_audit.py),
#   the RFC-mandated 10-check validation suite (tests/synapse_suite.py), and
#   the profile-aware rollout gate (ops/rollout_profile.sh).
#
#   Run from anywhere:  python3 phase0_bootstrap.py [repo_root] [--force]
#   Idempotent: existing files are skipped unless --force is passed.
#
# CHAT-FENCE-SAFE: this payload contains NO line of only backticks and NO
#   markdown fences inside string constants, so it survives copy/paste as a
#   single code block. Trees are rendered as 4-space-indented text.
#
# RFC ANCHORS: 1.4 Module Map, 16 Compliance Checklist, 17 Conformance
#   Test, 160 Editing Mandate (validation + rollout gates).
# INVARIANTS: stdlib only; never modifies git history; never touches library
#   source under uro/uro/; only creates build/test/ops artifacts.
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import stat
import subprocess
import sys
from pathlib import Path
# === END: imports ===

# === START: constants ===
DATE_STR = "2026-10-29"
BUILD = "_BUILD"
FILES: dict = {}
# === END: constants ===


# === START: doc_session_bootstrap ===
FILES[BUILD + "/SESSION_BOOTSTRAP.md"] = r'''# URO BUILD - SESSION BOOTSTRAP

You are resuming the V.A.U.R.O.S. URO library build-out to RFC-DRAFT v3.0.0.
The repository is the durable source of truth. The chat session is disposable.
All decisions, phase state, scaffolds, and continuity data live in `_BUILD/`.

## Goal
Fully implement every code-driven RFC section as a production-grade library.
Final state: zero stubs, zero scaffolding, fully commented code, file headers,
block START/END markers, function-level PURPOSE comments, immediate
implementability, one canonical source of truth per module.

## Non-negotiable principles
1. RFC 1.4 Module Map is the authority.
2. Canonical imports only; no local re-implementation of clamp/cross-talk/decay.
3. RFC 160 Editing Mandate: existing files modified ONLY via Exact Block
   Replacement bounded by START/END markers, occurrence count == 1 verified.
   Net-new files are created whole.
4. Scaffolding is temporary: tagged SCAFFOLD(Phase-N), tracked in
   _BUILD/SCAFFOLD_LEDGER.md, which MUST be empty before sign-off.
5. Definition of Done = measured conformance (RFC 16/17), never asserted.

## Locked decisions (full ADRs in DECISIONS.md)
- ADR-001: Part 16 (Global Infrastructure) EXCLUDED from library scope.
- ADR-002: Restructure via Option A (canonical tree alongside, migrate, delete
  duplicates only after canonical replacement lands and passes).
- ADR-003: Regression matrix / synapse suite / rollout script did not exist;
  they are built from scratch as Phase-0 deliverables.
- ADR-004: Repository-hosted _BUILD/ + bootstrap_session.py is the official
  chat-cloning mechanism.

## Canonical target
See _BUILD/TARGET_TREE.md (summary: core/, nte/, synapse/, opar/,
coordinator_bus.py, quad/, security/, memory/, pathing/, interchange/,
learning/, hardware/, boot/, economy/, docks/, ecosystem/, invariants.py).

## Critical path
Primitives -> Core -> Security primitives -> NTE axes/state -> Synapse
vector/engine -> Synapse persistence -> OPAR package -> CoordinatorBus.

## Resume rule
Before planning or coding, read: SESSION_BOOTSTRAP.md, DECISIONS.md, STATE.md,
MASTER_PLAN.md, TARGET_TREE.md, SCAFFOLD_LEDGER.md, and the current phase
checkpoint in CHECKPOINTS/. Then continue without re-litigating locked
decisions. Or run _BUILD/tools/bootstrap_session.py and paste its bundle.
'''
# === END: doc_session_bootstrap ===


# === START: doc_decisions ===
FILES[BUILD + "/DECISIONS.md"] = r'''# DECISIONS / ADR LOG
Append-only. Never delete history.

## ADR-001 - Exclude Part 16
Date: ''' + DATE_STR + r'''
Status: Accepted
Part 16 (Global Infrastructure: MagLev, water biovirons, physical logistics)
is excluded from the library build-out. Part 17 remains in scope but minimal
(only code-relevant slivers: 8-hour mandate tracking, token payout schedules,
audit/governance), deferred to the end.

## ADR-002 - Restructure using Option A
Date: ''' + DATE_STR + r'''
Status: Accepted
Build the canonical architecture (TARGET_TREE.md) alongside the existing tree.
Migrate imports and callers. Validate. Delete duplicates only after their
canonical replacement lands and passes. End state must match TARGET_TREE.md.

## ADR-003 - Build validation and regression from scratch
Date: ''' + DATE_STR + r'''
Status: Accepted
tests/synapse_suite.py, ops/rollout_profile.sh, and the regression matrix did
not exist. They are created as first-class Phase-0 deliverables. The suite is
expected to FAIL until Phases 4-9 land; that failure is the honest baseline.

## ADR-004 - Repository-hosted chat continuity
Date: ''' + DATE_STR + r'''
Status: Accepted
Chat continuity lives in the repository, not in chat memory. Official
mechanism: _BUILD/ project memory plus _BUILD/tools/bootstrap_session.py,
which emits a single paste-able full-awareness bundle for any new session.
'''
# === END: doc_decisions ===


# === START: doc_state ===
FILES[BUILD + "/STATE.md"] = r'''# STATE

CURRENT_PHASE: phase-00-continuity
PHASE_STATUS: in-progress
NEXT_ACTION: Run classify_modules.py, review CONFORMANCE_MATRIX.md, then start Phase 1 (primitives)
LAST_UPDATED: ''' + DATE_STR + r'''

## Active Objective
Establish durable continuity, audit the existing tree, and stand up the
validation/rollout gates.

## Completed
- Scope locked: Part 16 excluded (ADR-001).
- Restructure locked: Option A (ADR-002).
- Continuity locked: _BUILD/ + bootstrap_session.py (ADR-004).
- Phase-0 writer executed; _BUILD/, tools, suite, rollout script created.

## In Progress
- Populate CONFORMANCE_MATRIX.md via classify_modules.py.
- Baseline run of tests/synapse_suite.py (expected failures = work list).

## Blocked
None.
'''
# === END: doc_state ===


# === START: doc_master_plan ===
FILES[BUILD + "/MASTER_PLAN.md"] = r'''# MASTER PLAN

## Phase 0 - Continuity, Audit, Validation Foundation
1. _BUILD/ continuity structure. 2. bootstrap_session.py. 3. classify_modules.py.
4. CONFORMANCE_MATRIX.md. 5. tests/synapse_suite.py. 6. ops/rollout_profile.sh.
7. SCAFFOLD_LEDGER.md. 8. Commit + tag uro-build/phase-00-done.

## Phase 1 - Primitives: constants.py, exceptions.py, types.py
## Phase 2 - Core: core/urid.py, core/uro.py, core/header.py, core/components.py,
   core/inheritance.py, core/datetime_uro.py
## Phase 3 - Security primitives: security/inahash.py, security/encryption.py
## Phase 4 - NTE axes/state: nte/axes.py, nte/state.py
## Phase 5 - NTE math: nte/cross_talk.py, polarity.py, math_influence.py,
   firing.py, reward.py, ans.py
## Phase 6 - Synapse vector/engine: synapse/vector.py, synapse/engine.py
## Phase 7 - Synapse persistence: synapse/persistence.py
## Phase 8 - OPAR package: opar/base.py, protocol.py, stages.py, grounding.py,
   compliance.py
## Phase 9 - CoordinatorBus: coordinator_bus.py (consolidate 4 copies)
## Phase 10 - Quad + CROATE: quad/*
## Phase 11 - Security full: pki, identity, acl, policy, circle_security,
   field_encryption, custody, ldap
## Phase 12 - Memory: hierarchy, movement, consolidation, sleep
## Phase 13 - Pathing: pathing, associations, cro_matrix, trust_value, beacons,
   resolution, onion, path_ops, connectors, swarms
## Phase 14 - Interchange: upi, aupi, interchange, self_loading, priority
## Phase 15 - Learning/AIAI: primitives, pattern, action_uros, attention,
   companion, robotics, sensory, wetware
## Phase 16 - Boot + ANS lifecycle: boot_sequence, child_boot, self_check
## Phase 17 - Economy: currency, token_transfer, marketplace, social_pricing,
   supply_chain
## Phase 18 - Docks + interceptor: dock, manifest, registry, interceptor, dock_defs
## Phase 19 - Ecosystem: api/URO_API.py, connectors/db.py, api_creator.py
## Phase 20 - Invariants + final gate: invariants.py, glossary.py,
   no_stub_audit.py --gate clean, SCAFFOLD_LEDGER empty

## Critical path
1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8 -> 9. Everything else hangs off this spine.
'''
# === END: doc_master_plan ===


# === START: doc_target_tree ===
FILES[BUILD + "/TARGET_TREE.md"] = r'''# TARGET CANONICAL ARCHITECTURE

End-state of the Python package (repo_root/uro/). Everything else is
consolidated into this tree or deleted. Rendered as 4-space-indented text
(no markdown fences) to keep payloads chat-fence-safe.

    uro/
    ├── __init__.py            # canonical exports only; no _CompatStub
    ├── constants.py           # bit widths, baselines, epoch, currency ratios
    ├── exceptions.py          # typed URO exception hierarchy
    ├── types.py               # shared aliases / Protocols
    ├── core/                  # urid.py uro.py header.py components.py
    │   │                      # inheritance.py datetime_uro.py
    ├── nte/                   # axes.py state.py cross_talk.py polarity.py
    │   │                      # math_influence.py firing.py reward.py ans.py
    ├── synapse/               # vector.py engine.py persistence.py __init__.py
    ├── opar/                  # base.py protocol.py stages.py grounding.py compliance.py
    ├── coordinator_bus.py     # auto synapse create/modulate on emit/await
    ├── quad/                  # quad_capability.py croate.py character_condition.py
    ├── security/              # inahash.py encryption.py pki.py identity.py acl.py
    │   │                      # policy.py circle_security.py field_encryption.py
    │   │                      # custody.py ldap.py
    ├── memory/                # hierarchy.py movement.py consolidation.py sleep.py
    ├── pathing/               # pathing.py associations.py cro_matrix.py trust_value.py
    │   │                      # beacons.py resolution.py onion.py path_ops.py
    │   │                      # connectors.py swarms.py
    ├── interchange/           # upi.py aupi.py interchange.py self_loading.py priority.py
    ├── learning/              # primitives.py pattern.py action_uros.py attention.py
    │   │                      # companion.py robotics.py sensory.py wetware.py
    ├── hardware/              # chip_arch.py asic_specs.py drivers.py (simulation only)
    ├── boot/                  # boot_sequence.py child_boot.py self_check.py
    ├── economy/               # currency.py token_transfer.py marketplace.py
    │   │                      # social_pricing.py supply_chain.py
    ├── docks/                 # dock.py manifest.py registry.py interceptor.py dock_defs/
    ├── ecosystem/             # api/ connectors/ api_creator.py
    ├── invariants.py          # ten invariants as runtime assertions
    └── glossary.py            # glossary as structured data
'''
# === END: doc_target_tree ===


# === START: doc_scaffold_ledger ===
FILES[BUILD + "/SCAFFOLD_LEDGER.md"] = r'''# SCAFFOLD LEDGER

Track all temporary scaffolding here. Must be empty before final sign-off.

Format:
[OPEN] SCAFFOLD(Phase-N): description | owner | removal criteria
[DONE] SCAFFOLD(Phase-N): description | removed in commit/phase

## Open Scaffolds
No open scaffolds.

## Closed Scaffolds
None yet.
'''
# === END: doc_scaffold_ledger ===


# === START: doc_conformance_placeholder ===
FILES[BUILD + "/CONFORMANCE_MATRIX.md"] = r'''# CONFORMANCE MATRIX

Placeholder. Regenerate with:
    python3 _BUILD/tools/classify_modules.py
'''
# === END: doc_conformance_placeholder ===


# === START: doc_regression_matrix ===
FILES[BUILD + "/REGRESSION_MATRIX.md"] = r'''# REGRESSION MATRIX

## 1. Synapse 10-check suite (tests/synapse_suite.py)
01 canonical imports resolve (no _CompatStub).
02 synapse constructs between two endpoints.
03 NTE state has exactly 24 axes.
04 all axes initialize at baseline 50.0.
05 InteractionOutcome tolerates partial payloads; success mandatory.
06 record_interaction modulates all 24 axes (keys preserved, values move).
07 cross-talk is engine-owned; E/I balance rule observable.
08 decay_synapse moves axes toward 50.0.
09 persistence round-trips synapse identity and levels.
10 CoordinatorBus modulation is non-fatal.

## 2. OPAR conformance (opar/compliance.py)
FULFILLED + full opar_trace on valid stimulus; INCAPABLE without exception
escape on failing act; DEFERRED when grounding blocks; receipt["nte"] has 24
keys; no no-op OPAR stub remains.

## 3. Import hygiene
Direct canonical imports work; no _CompatStub reliance; no duplicate
source-of-truth modules active.

## 4. Bit widths
UUID 128; URID 256; URO 512; INAHASH 1024; NTE state 1536 bits.

## 5. Non-fatal mandate
Modulation, persistence, and grounding-gate failures never break message flow.

## 6. Final gate
_BUILD/tools/no_stub_audit.py --gate exits 0; SCAFFOLD_LEDGER has no [OPEN].
'''
# === END: doc_regression_matrix ===


# === START: doc_checkpoint_phase00 ===
FILES[BUILD + "/CHECKPOINTS/phase-00-continuity.md"] = r'''# Phase 00 - Continuity and Audit

## Objective
Durable session memory + audit + validation gates before any library code.

## Deliverables
_BUILD/ docs, tools/bootstrap_session.py, tools/classify_modules.py,
tools/no_stub_audit.py, tests/synapse_suite.py, ops/rollout_profile.sh.

## Exit criteria
1. CONFORMANCE_MATRIX.md populated (every file classified REAL/STUB/EMPTY/PARSE_ERROR).
2. Duplicate-basename list reviewed; consolidation order agreed.
3. Baseline synapse_suite run recorded (failures become Phase 4-9 work items).
4. git commit + tag uro-build/phase-00-done.
'''
# === END: doc_checkpoint_phase00 ===


# === START: tool_bootstrap_session ===
FILES[BUILD + "/tools/bootstrap_session.py"] = r'''#!/usr/bin/env python3
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
    """PURPOSE: locate the repository root via git, else via _BUILD ancestry."""
    out = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if out:
        return Path(out)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
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
'''
# === END: tool_bootstrap_session ===


# === START: tool_classify_modules ===
FILES[BUILD + "/tools/classify_modules.py"] = r'''#!/usr/bin/env python3
# === FILE: _BUILD/tools/classify_modules.py ===
# PURPOSE:
#   Audit every Python module under uro/ and classify it as REAL (substantive
#   definitions), STUB (definitions exist but bodies are pass/docstring/raise),
#   EMPTY (no definitions), or PARSE_ERROR. Flag duplicate basenames that
#   indicate competing sources of truth. Write _BUILD/CONFORMANCE_MATRIX.md.
# RFC ANCHORS: 1.4 Module Map (source of truth), 160 (no blind rewrites).
# INVARIANTS: read-only over the package; only writes CONFORMANCE_MATRIX.md.
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import ast
import subprocess
from collections import Counter
from pathlib import Path
# === END: imports ===

# === START: constants ===
BUILD = "_BUILD"
# === END: constants ===


# === START: root ===
def root():
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
# === END: root ===


# === START: substantive ===
def substantive(node):
    """PURPOSE: decide whether a def/class body performs real work."""
    for stmt in getattr(node, "body", []):
        if isinstance(stmt, ast.Pass):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) \
                and isinstance(stmt.value.value, str):
            continue
        if isinstance(stmt, ast.Raise):
            continue
        return True
    return False
# === END: substantive ===


# === START: classify ===
def classify(path):
    """PURPOSE: return (status, def_count, real_def_count) for one module."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except Exception:
        return ("PARSE_ERROR", 0, 0)
    defs = [n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    real = [d for d in defs if substantive(d)]
    if not defs:
        return ("EMPTY", 0, 0)
    if not real:
        return ("STUB", len(defs), 0)
    return ("REAL", len(defs), len(real))
# === END: classify ===


# === START: main ===
def main():
    """PURPOSE: build and write the conformance matrix markdown."""
    r = root()
    pkg = r / "uro"
    rows = []
    names = Counter()
    if pkg.exists():
        for path in sorted(pkg.rglob("*.py")):
            rel = path.relative_to(r).as_posix()
            status, ndefs, nreal = classify(path)
            names[path.name] += 1
            rows.append((rel, status, ndefs, nreal))
    dups = sorted(n for n, c in names.items() if c > 1)
    lines = [
        "# CONFORMANCE MATRIX",
        "",
        "Generated by _BUILD/tools/classify_modules.py. Re-run after each phase.",
        "",
        "| Existing Path | Status | Defs | Real Defs | Dup Basename | Disposition |",
        "|---|---|---:|---:|---|---|",
    ]
    for rel, status, ndefs, nreal in rows:
        dup = "YES" if Path(rel).name in dups else ""
        if status == "REAL":
            disp = "keep-or-migrate"
        elif status in ("STUB", "EMPTY"):
            disp = "build-or-delete"
        else:
            disp = "inspect"
        lines.append("| %s | %s | %d | %d | %s | %s |" % (rel, status, ndefs, nreal, dup, disp))
    lines += ["", "## Duplicate Basenames (competing sources of truth)", ""]
    if dups:
        lines += ["- %s (%d copies)" % (n, names[n]) for n in dups]
    else:
        lines.append("- none")
    out = r / BUILD / "CONFORMANCE_MATRIX.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote %s (%d modules, %d duplicate basenames)" % (out, len(rows), len(dups)))
    return 0
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main())
'''
# === END: tool_classify_modules ===


# === START: tool_no_stub_audit ===
FILES[BUILD + "/tools/no_stub_audit.py"] = r'''#!/usr/bin/env python3
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
'''
# === END: tool_no_stub_audit ===


# === START: test_synapse_suite ===
FILES["tests/synapse_suite.py"] = r'''#!/usr/bin/env python3
# === FILE: tests/synapse_suite.py ===
# PURPOSE:
#   The RFC 160 10-check validation suite for the synapse protocol.
#   Validates canonical imports, vector construction, 24-axis state,
#   baseline, outcome contract, modulation, engine-owned cross-talk,
#   homeostatic decay, persistence round-trip, and non-fatal bus modulation.
#   Exit code 0 only when all ten checks pass.
# RFC ANCHORS: 16-17 (compliance/conformance), 35-44 (synapse protocol),
#   160 item 4 (run the 10-check suite after core edits).
# NOTE: test-only construction of NTE levels is permitted here; production
#   code MUST NOT mutate nte_state.levels directly (160 item 7).
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESULTS = []
# === END: imports ===


# === START: check ===
def check(name):
    """PURPOSE: register a numbered validation check in declaration order."""
    def wrap(fn):
        RESULTS.append((name, fn))
        return fn
    return wrap
# === END: check ===


# === START: helpers ===
def _axes():
    """PURPOSE: return the canonical 24 axis names from the enums."""
    from uro.nte.axes import NTEAxis, CognitiveAxis
    return [a.value for a in NTEAxis] + [a.value for a in CognitiveAxis]


def _syn():
    """PURPOSE: shared helper returning a synapse for the fixed test pair."""
    import uro.synapse.persistence as persistence
    return persistence.get_or_create_synapse("0" * 64, "1" * 64)


def _syn_id(syn):
    """PURPOSE: stable identity string for a synapse URID."""
    u = syn.synapse_urid
    return u.to_hex() if hasattr(u, "to_hex") else str(u)
# === END: helpers ===


# === START: checks ===
@check("01 canonical imports resolve")
def c01():
    """PURPOSE: prove direct canonical imports work without compat stubs."""
    import uro.synapse.engine as engine
    import uro.synapse.persistence as persistence
    from uro.synapse.vector import SynapseVectorURO
    from uro.nte.axes import NTEAxis, CognitiveAxis
    assert engine and persistence and SynapseVectorURO and NTEAxis and CognitiveAxis


@check("02 synapse constructs between two endpoints")
def c02():
    """PURPOSE: create or fetch a synapse for an endpoint pair."""
    syn = _syn()
    assert syn is not None and syn.urid1 is not None and syn.urid2 is not None


@check("03 NTE state has exactly 24 axes")
def c03():
    """PURPOSE: assert the composite 24-axis state (DD-1)."""
    assert len(_syn().nte_state.levels) == 24


@check("04 all axes initialize at baseline 50.0")
def c04():
    """PURPOSE: assert equilibrium baseline on fresh synapse state."""
    levels = _syn().nte_state.levels
    assert all(abs(v - 50.0) < 1e-9 for v in levels.values())


@check("05 InteractionOutcome tolerates partial payloads")
def c05():
    """PURPOSE: success mandatory, all other keys default neutral."""
    import uro.synapse.engine as engine
    o = engine.InteractionOutcome(success=True)
    assert o["success"] is True
    assert o.get("novelty", 0.0) == 0.0
    assert o.get("load", 0.0) == 0.0
    assert o.get("trust_signal", 0.0) == 0.0


@check("06 record_interaction modulates all 24 axes")
def c06():
    """PURPOSE: keys preserved at 24 and values move on a strong outcome."""
    import uro.synapse.engine as engine
    syn = _syn()
    before = dict(syn.nte_state.levels)
    syn.record_interaction(engine.InteractionOutcome(
        success=True, novelty=0.8, load=0.2, trust_signal=0.5, latency_ms=10.0))
    after = syn.nte_state.levels
    assert set(after) == set(before) and len(after) == 24
    assert any(abs(after[k] - before[k]) > 1e-9 for k in after)


@check("07 cross-talk is engine-owned (E/I balance observable)")
def c07():
    """PURPOSE: the 24x24 second pass lives in the engine, not callers."""
    import uro.synapse.engine as engine
    fn = None
    for name in ("apply_cross_talk", "cross_talk_pass", "_cross_talk", "apply_crosstalk"):
        candidate = getattr(engine, name, None)
        if callable(candidate):
            fn = candidate
            break
    assert callable(fn), "engine exposes no cross-talk pass"
    levels = {k: 50.0 for k in _axes()}
    levels["glutamate"] = 90.0
    levels["gaba"] = 10.0
    probe = dict(levels)
    out = fn(probe)
    out = out if isinstance(out, dict) else probe
    assert out["glutamate"] < 90.0 and out["gaba"] > 10.0


@check("08 decay_synapse moves axes toward 50.0")
def c08():
    """PURPOSE: homeostatic decay pulls extremes back to baseline."""
    import uro.synapse.engine as engine
    syn = _syn()
    syn.nte_state.levels["glutamate"] = 90.0  # test-only construction
    engine.decay_synapse(syn, rate=0.02)
    assert syn.nte_state.levels["glutamate"] < 90.0


@check("09 persistence round-trips identity and levels")
def c09():
    """PURPOSE: write-behind flush then reload yields the same synapse."""
    import uro.synapse.engine as engine
    import uro.synapse.persistence as persistence
    syn = persistence.get_or_create_synapse("0" * 64, "1" * 64)
    syn.record_interaction(engine.InteractionOutcome(success=True, novelty=0.3))
    persistence.mark_dirty(syn)
    persistence.flush_dirty()
    again = persistence.get_or_create_synapse("0" * 64, "1" * 64)
    assert _syn_id(again) == _syn_id(syn)
    for k, v in syn.nte_state.levels.items():
        assert abs(again.nte_state.levels[k] - v) < 1e-9


@check("10 CoordinatorBus modulation is non-fatal")
def c10():
    """PURPOSE: a raising synapse must never break message flow."""
    from uro.coordinator_bus import CoordinatorBus

    class Boom:
        def record_interaction(self, outcome):
            """PURPOSE: always raise to prove non-fatal handling."""
            raise RuntimeError("boom")

        def record_use(self, success):
            """PURPOSE: also raise on the legacy path."""
            raise RuntimeError("boom")

    CoordinatorBus()._modulate_synapse_obj(Boom(), {"success": True})
# === END: checks ===


# === START: main ===
def main():
    """PURPOSE: run every registered check and report the gate result."""
    passed = 0
    for name, fn in RESULTS:
        try:
            fn()
            passed += 1
            print("PASS  " + name)
        except Exception as exc:
            print("FAIL  " + name + " :: " + type(exc).__name__ + ": " + exc)
    total = len(RESULTS)
    print("%d/%d checks passed" % (passed, total))
    return 0 if passed == total == 10 else 1
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main())
'''
# === END: test_synapse_suite ===


# === START: ops_rollout_profile ===
FILES["ops/rollout_profile.sh"] = r'''#!/usr/bin/env bash
# === FILE: ops/rollout_profile.sh ===
# PURPOSE: Profile-aware rolling restart with in-container 5-gate verification.
#   Gates: 1 compile, 2 synapse 10-check suite, 3 stub audit, 4 pytest smoke,
#   5 canonical import hygiene. Profiles advance dev -> staging -> uat -> prod
#   and stop at the requested target. Restart is delegated to URO_RESTART_CMD
#   when configured; otherwise the restart step is explicitly skipped.
# RFC ANCHORS: 160 item 4 (roll out profile-by-profile after core edits).
# USAGE: ops/rollout_profile.sh [dev|staging|uat|prod]
# === END FILE HEADER ===
set -euo pipefail

TARGET="${1:-dev}"
PROFILES=(dev staging uat prod)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

gate_compile() { python3 -m compileall -q uro > /dev/null; }
gate_synapse() { python3 tests/synapse_suite.py > /dev/null; }
gate_stub()    { python3 _BUILD/tools/no_stub_audit.py > /dev/null; }
gate_pytest()  { python3 -m pytest tests -q > /dev/null; }
gate_imports() { python3 -c "import uro.synapse.engine, uro.synapse.persistence, uro.coordinator_bus" > /dev/null; }

run_gates() {
  local profile="$1"
  echo "[rollout] ${profile}: gate 1/5 compile"
  gate_compile
  echo "[rollout] ${profile}: gate 2/5 synapse suite"
  gate_synapse
  echo "[rollout] ${profile}: gate 3/5 stub audit"
  gate_stub
  echo "[rollout] ${profile}: gate 4/5 pytest smoke"
  gate_pytest
  echo "[rollout] ${profile}: gate 5/5 import hygiene"
  gate_imports
}

for p in "${PROFILES[@]}"; do
  run_gates "$p"
  if [ -n "${URO_RESTART_CMD:-}" ]; then
    echo "[rollout] ${p}: restarting via URO_RESTART_CMD"
    URO_PROFILE="$p" bash -c "$URO_RESTART_CMD"
  else
    echo "[rollout] ${p}: URO_RESTART_CMD not configured; restart skipped"
  fi
  if [ "$p" = "$TARGET" ]; then
    echo "[rollout] reached target profile: $TARGET"
    exit 0
  fi
done

echo "[rollout] target profile not found: $TARGET (expected one of: ${PROFILES[*]})" >&2
exit 1
'''
# === END: ops_rollout_profile ===


# === START: repo_root ===
def repo_root(argv):
    """PURPOSE: resolve target repo root from argv override or git toplevel."""
    for arg in argv:
        if not arg.startswith("--"):
            return Path(arg).resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / BUILD).exists():
            return parent
    return Path.cwd().resolve()
# === END: repo_root ===


# === START: main ===
def main(argv):
    """PURPOSE: write all Phase-0 files idempotently and report the result."""
    force = "--force" in argv
    root = repo_root(argv)
    written, skipped = [], []
    for rel, content in FILES.items():
        target = root / rel
        if target.exists() and not force:
            skipped.append(rel)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        if rel.endswith(".sh"):
            target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        written.append(rel)
    print("repo root: %s" % root)
    print("written (%d):" % len(written))
    for rel in written:
        print("  + " + rel)
    if skipped:
        print("skipped existing (%d), use --force to overwrite:" % len(skipped))
        for rel in skipped:
            print("  = " + rel)
    print("")
    print("next steps:")
    print("  cd %s" % root)
    print("  python3 _BUILD/tools/classify_modules.py")
    print("  python3 tests/synapse_suite.py          # baseline; failures = work list")
    print("  python3 _BUILD/tools/bootstrap_session.py > /tmp/uro_resume.md")
    print("  git add _BUILD tests ops && git commit -m 'Phase 0: continuity, audit, validation foundation'")
    print("  git tag -a uro-build/phase-00-done -m 'Phase 0 complete'")
    return 0
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

