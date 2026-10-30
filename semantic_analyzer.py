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
URO Semantic Analyzer
Canonical shared library for advanced code understanding across all V.A.U.R.O.S. docks.
Fulfills URO Mandate: Single source of truth for structural and semantic evaluation.
"""
import ast
import re
from collections import Counter
from typing import Dict, Any, List
import logging

logger = logging.getLogger("uro.semantic_analyzer")

class SemanticAnalyzer:
    """Shared engine for evaluating code semantics, complexity, and structure."""
    
    @staticmethod
    def analyze(code: str, file_path: str = "unknown.py") -> Dict[str, Any]:
        """
        Perform comprehensive semantic analysis on a code string.
        Returns a structured URO payload with findings and refactoring suggestions.
        """
        if not code.strip():
            return {"status": "skipped", "reason": "empty_code"}
            
        findings = {
            "file_path": file_path,
            "complexity": {},
            "smells": [],
            "suggestions": [],
            "is_valid_python": False
        }

        try:
            tree = ast.parse(code)
            findings["is_valid_python"] = True
            
            # 1. Cognitive Complexity & Nesting Depth
            max_depth = SemanticAnalyzer._get_max_nesting_depth(tree)
            findings["complexity"]["max_nesting_depth"] = max_depth
            if max_depth > 4:
                findings["smells"].append("high_nesting_depth")
                findings["suggestions"].append("Consider extracting nested logic into guard clauses or helper functions.")

            # 2. Magic Constants Detection
            numbers = re.findall(r'\b\d{3,}\b', code)
            counts = Counter(numbers)
            magic_nums = [num for num, count in counts.items() if count >= 2]
            if magic_nums:
                findings["smells"].append("magic_constants")
                findings["suggestions"].append(f"Elevate repeated magic numbers to module-level constants: {magic_nums}")

            # 3. Dead Import Detection
            dead_imports = SemanticAnalyzer._find_dead_imports(tree)
            if dead_imports:
                findings["smells"].append("dead_imports")
                findings["suggestions"].append(f"Remove unused imports to reduce cognitive load: {dead_imports}")

            # 4. Function/Class Count (Basic Metrics)
            findings["metrics"] = {
                "functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            }
            
            findings["status"] = "analyzed"
            
        except SyntaxError as e:
            findings["status"] = "syntax_error"
            findings["error"] = str(e)
            findings["suggestions"].append("Fix syntax errors before semantic analysis can proceed.")

        return findings

    @staticmethod
    def _get_max_nesting_depth(node: ast.AST, current_depth: int = 0) -> int:
        max_d = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler)):
                max_d = max(max_d, SemanticAnalyzer._get_max_nesting_depth(child, current_depth + 1))
            else:
                max_d = max(max_d, SemanticAnalyzer._get_max_nesting_depth(child, current_depth))
        return max_d

    @staticmethod
    def _find_dead_imports(tree: ast.AST) -> List[str]:
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                used_names.add(node.value.id)

        dead_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name
                    if name not in used_names:
                        dead_imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname or alias.name
                    if name not in used_names:
                        dead_imports.append(alias.name)
        return list(set(dead_imports))

# Expose a simple functional API for docks that don't want to instantiate the class
def analyze_code(code: str, file_path: str = "unknown.py") -> Dict[str, Any]:
    return SemanticAnalyzer.analyze(code, file_path)
