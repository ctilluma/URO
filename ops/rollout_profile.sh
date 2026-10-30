#!/usr/bin/env bash
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
