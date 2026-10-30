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


import os
import re
import sys

repo = os.path.expanduser("~/viridant-auraforge")
px = os.path.join(repo, "docks/phoenix")

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()
        
    if '.levels[' not in content:
        return False
        
    lines = content.split('\n')
    new_lines = []
    modified = False
    
    # Match: var.levels[key] = value
    # We only handle simple '=' assignments for safety. Complex ops (+=, -=) are flagged.
    pattern = re.compile(r'^(\s*)([\w\.\[\]]+)\.levels\[(.+?)\]\s*=\s*(.+)$')
    
    for line in lines:
        m = pattern.match(line)
        if m:
            indent, var, key, val = m.groups()
            replacement = f"{indent}# === START: nte_normalize ===\n"
            replacement += f"{indent}{var}.levels = normalize_nte_state({{**{var}.levels, {key}: {val}}})\n"
            replacement += f"{indent}# === END: nte_normalize ==="
            new_lines.append(replacement)
            modified = True
        else:
            new_lines.append(line)
            
    if modified:
        # Add import if missing
        if 'from uro.synapse.engine import normalize_nte_state' not in content:
            # Find a good place to insert, e.g., after other imports
            for i, l in enumerate(new_lines):
                if l.startswith('import ') or l.startswith('from '):
                    new_lines.insert(i + 1, 'from uro.synapse.engine import normalize_nte_state')
                    break
            else:
                new_lines.insert(0, 'from uro.synapse.engine import normalize_nte_state')
                
        with open(path, 'w') as f:
            f.write('\n'.join(new_lines))
        return True
    return False

count = 0
for root, _, files in os.walk(px):
    if '__pycache__' in root: continue
    for f in files:
        if f.endswith('.py'):
            if process_file(os.path.join(root, f)):
                count += 1
print(f"[OK] Fixed NTE mutations in {count} files")
