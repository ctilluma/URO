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
# === FILE: tests/run_all_suites.py ===
# PURPOSE: Single-entry gate: run all sixteen suites, aggregate results,
#          exit non-zero on any failure (rolling maintenance protocol).
# === END FILE HEADER ===
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    "primitives_suite.py", "core_suite.py", "synapse_suite.py",
    "security_suite.py", "nte_suite.py", "nte_math_suite.py",
    "synapse_vector_suite.py", "memory_suite.py", "pathing_suite.py",
    "interchange_suite.py", "learning_suite.py", "opar_suite.py",
    "quad_suite.py", "boot_suite.py", "security_full_suite.py",
    "economy_suite.py",
]
def main():
    results = []
    for name in SUITES:
        proc = subprocess.run([sys.executable, str(ROOT / "tests" / name)],
                              capture_output=True, text=True)
        lines = proc.stdout.strip().splitlines()
        summary = lines[-1] if lines else "NO OUTPUT"
        ok = summary.startswith("10/10") and proc.returncode == 0
        results.append(ok)
        print(("PASS " if ok else "FAIL ") + name + " :: " + summary)
        if not ok:
            for line in lines:
                if line.startswith("FAIL  "):
                    print("     " + line)
    green = sum(results)
    print("%d/%d suites green" % (green, len(SUITES)))
    return 0 if green == len(SUITES) else 1
if __name__ == "__main__":
    sys.exit(main())
