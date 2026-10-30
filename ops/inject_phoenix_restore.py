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


import ast
import sys
import os

repo = os.path.expanduser("~/viridant-auraforge")
routes_path = os.path.join(repo, "docks/phoenix/routes.py")
api_path = os.path.join(repo, "docks/phoenix/api.py")

restore_endpoint_code = """
# === START: phoenix_restore_endpoint ===
@router.post("/phoenix/restore")
async def phoenix_restore(request: Request):
    \"\"\"
    S13.5 / S7.11: Phoenix Restoration Endpoint.
    Accepts dock_name and reason. Wipes compromised state volume and rebuilds
    the dock from a known-good image via Host Controller.
    \"\"\"
    try:
        data = await request.json()
        dock_name = data.get("dock_name")
        reason = data.get("reason", "Aegis critical quarantine")
        
        if not dock_name:
            return {"status": "error", "message": "dock_name is required"}
            
        logger.info(f"[Phoenix] RESTORE initiated for {dock_name}: {reason}")
        
        # Step 1: Wipe compromised state volume via Host Controller
        wipe_result = await bus.emit_uro_and_await(
            intent="host_controller.wipe_state_volume",
            payload={"dock": dock_name, "reason": reason},
            target_dock="host_controller",
            timeout=30
        )
        
        # Step 2: Rebuild dock from known-good image
        rebuild_result = await bus.emit_uro_and_await(
            intent="host_controller.rebuild_from_image",
            payload={"dock": dock_name, "reason": reason},
            target_dock="host_controller",
            timeout=60
        )
        
        return {
            "status": "success",
            "dock_name": dock_name,
            "wipe_result": wipe_result,
            "rebuild_result": rebuild_result
        }
    except Exception as e:
        logger.error(f"Phoenix restore failed: {e}")
        return {"status": "error", "error": str(e)}
# === END: phoenix_restore_endpoint ===
"""

restore_app_code = restore_endpoint_code.replace("@router.post", "@app.post").replace("phoenix_restore_endpoint", "phoenix_restore_endpoint_app")

def inject_endpoint(path, code, marker_name, target_pattern):
    with open(path, 'r') as f:
        content = f.read()
        
    if f"# === START: {marker_name} ===" in content:
        print(f"[SKIP] {marker_name} already in {path}")
        return False
        
    lines = content.split('\n')
    
    anchor_idx = -1
    for i, line in enumerate(lines):
        if target_pattern in line:
            anchor_idx = i
            break
            
    if anchor_idx == -1:
        # Fallback: find last @router.post or @app.post
        for i in range(len(lines)-1, -1, -1):
            if '@router.post(' in lines[i] or '@app.post(' in lines[i]:
                anchor_idx = i
                break
                
    if anchor_idx != -1:
        lines.insert(anchor_idx, code)
        
        with open(path, 'w') as f:
            f.write('\n'.join(lines))
        print(f"[OK] Injected {marker_name} into {path} before {target_pattern}")
        return True
    else:
        print(f"[FAIL] Could not find anchor in {path}")
        return False

inject_endpoint(routes_path, restore_endpoint_code, "phoenix_restore_endpoint", '@router.post("/phoenix/rollback")')
inject_endpoint(api_path, restore_app_code, "phoenix_restore_endpoint_app", '@app.post("/phoenix/isolate")')

# Verify AST
for p in [routes_path, api_path]:
    try:
        ast.parse(open(p).read())
        print(f"[AST OK] {p}")
    except Exception as e:
        print(f"[AST FAIL] {p}: {e}")
