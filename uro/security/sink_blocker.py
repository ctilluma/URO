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


"""
VAUROS Canonical Security Sink Blocker
Provides a local, AST-based static analysis tool to detect dangerous function calls.

MANDATE: Security gates must FAIL CLOSED if dangerous sinks are detected, 
regardless of external service availability.
"""

import ast
import logging
from typing import Dict, Any, List

logger = logging.getLogger("uro.security.sink_blocker")

# V.A.U.R.O.S. Forbidden Sinks
DANGEROUS_SINKS = {
    "eval", "exec", "compile", "__import__", 
    "os.system", "os.popen", "os.exec",
    "subprocess.call", "subprocess.run", "subprocess.Popen", "subprocess.check_output"
}

def _get_func_name(node) -> str:
    """Recursively extract the full function name from an AST Call node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _get_func_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""

def check_dangerous_sinks(code: str) -> Dict[str, Any]:
    """
    Parse Python code and check for forbidden dangerous sinks.
    
    Returns:
        Dict with 'safe' (bool) and 'findings' (list of dicts).
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "safe": False, 
            "findings": [{"type": "syntax_error", "message": f"Code failed to parse: {e}"}]
        }
        
    findings: List[Dict[str, Any]] = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_name = _get_func_name(node.func)
            
            # Check if the base name or full name is in the blacklist
            base_name = func_name.split('.')[-1] if '.' in func_name else func_name
            
            if func_name in DANGEROUS_SINKS or base_name in DANGEROUS_SINKS:
                findings.append({
                    "type": "dangerous_sink",
                    "severity": "critical",
                    "sink": func_name,
                    "line": str(getattr(node, 'lineno', 0)),
                    "message": f"Direct use of {func_name}() is forbidden by V.A.U.R.O.S. mandate"
                })
                
    if findings:
        logger.warning(f"Sink Blocker detected {len(findings)} dangerous sinks.")
        return {"safe": False, "findings": findings}
        
    return {"safe": True, "findings": []}
