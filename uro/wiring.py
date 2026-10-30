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
MODULE: Wiring (load -> dispatch -> register -> verify)
INTENT: Auto-wire EVERY python file in a dock (any name, any contents) and make
        each reachable by intent, without per-file edits.
STANDARD: URO-STD-0001 S38

UniversalLoader walks a dock dir, imports every .py, discovers an entry point
(get_orchestrator, any get_* returning an object with .execute, or a class with
.execute), and registers it under many intent aliases. dispatch() falls back to
this registry so nothing is left unwired.
"""
from __future__ import annotations

import os, re, logging, importlib.util
from typing import Any, Dict, Optional

logger = logging.getLogger("VAUROS.Wiring")


_UNIVERSAL: Dict[str, UniversalLoader] = {}



def get_universal(dock_dir: str, bus=None) -> UniversalLoader:
    """Get or create a UniversalLoader for a dock directory."""
    if dock_dir not in _UNIVERSAL:
        loader = UniversalLoader(dock_dir, bus)
        loader.load_all()
        _UNIVERSAL[dock_dir] = loader
    return _UNIVERSAL[dock_dir]

__all__ = ["parse_capability_file", "parse_domain_file", "dispatch",
           "register_capabilities", "UniversalLoader", "get_universal"]

JUNK_DIR = {'venv', '.venv', 'site-packages', 'node_modules', '__pycache__',"__pycache__", "backups", "legacy_bak", ".pytest_cache",
            "sandboxes", "workspace"}
EXCLUDE_FILES = {"__init__.py", "api.py", "main.py"}


def parse_capability_file(path):
    m = re.match(r"cap_(\d+)_(.+)\.py$", os.path.basename(path))
    return (f"Cap{int(m.group(1))}", m.group(2)) if m else (None, None)


def parse_domain_file(path):
    m = re.match(r"dom_(\d+)\.py$", os.path.basename(path))
    return int(m.group(1)) if m else None




def _stem(t: str) -> str:
    """Light suffix-stripping stemmer so forget~forgetting, vector~vectorizer,
    embed~embedder/embeddings, transform~transformation share a root."""
    t = t.lower()
    for suffix in ("izations", "ization", "isations", "isation", "ations",
                   "ation", "ments", "ment", "ings", "ing", "izers", "izer",
                   "isers", "iser", "ers", "er", "ies", "ed", "es", "ness",
                   "tions", "tion", "s"):
        if t.endswith(suffix) and len(t) - len(suffix) >= 3:
            t = t[: -len(suffix)]
            break
    if len(t) >= 3 and t[-1] == t[-2] and t[-1] not in "aeiou":
        t = t[:-1]
    return t


def _tokens(text: str) -> List[str]:
    """Extract stemmed tokens from text for semantic matching."""
    if not text:
        return []
    toks = re.split(r"[^a-zA-Z0-9]+", (text or "").lower())
    return [_stem(t) for t in toks if len(t) > 2]

class UniversalLoader:
    """Import every .py under a dock and expose entry points by alias."""

    def __init__(self, dock_dir: str, bus=None):
        self.dock_dir = dock_dir
        self.bus = bus
        self.by_alias: Dict[str, Any] = {}
        self.manifests: Dict[int, Dict[str, Any]] = {}
        self.errors: Dict[str, str] = {}
        self.known: Dict[str, Dict[str, Any]] = {}

    def load_all(self):
        for dirpath, dirnames, filenames in os.walk(self.dock_dir):
            dirnames[:] = [d for d in dirnames if d not in JUNK_DIR]
            for f in sorted(filenames):
                if not f.endswith(".py") or f in EXCLUDE_FILES or f.endswith("__main__.py"):
                    continue
                if f.endswith("_master.py"):
                    continue
                self._load_one(os.path.join(dirpath, f))

    def _find_entry(self, mod):
        """Find the entry point in a module (getter or class with execute)."""
        # Check for get_orchestrator first
        g = getattr(mod, "get_orchestrator", None)
        if callable(g):
            try:
                return g(self.bus)
            except Exception:
                pass
        
        # Check for any get_* that returns object with .execute.
        # Skip infra getters that return the dispatch/loader: calling them
        # re-enters get_universal -> load_all and recurses infinitely.
        for name in dir(mod):
            if name.startswith("get_") and name not in ("get_universal", "get_universal_dispatch"):
                fn = getattr(mod, name)
                if callable(fn):
                    try:
                        obj = fn(self.bus)
                        if hasattr(obj, "execute"):
                            return obj
                    except Exception:
                        continue
        
        # Check for a class with execute method
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, type) and hasattr(obj, "execute"):
                if getattr(obj, "__module__", "") == mod.__name__:
                    try:
                        return obj(self.bus)
                    except Exception:
                        continue
        
        return None

    def _aliases(self, rel: str):
        base = os.path.basename(rel)[:-3]
        stem = rel[:-3].replace(os.sep, "_")
        a = {base, stem}
        m = re.match(r"cap_(\d+)_(.+)", base)
        if m:
            a.add(f"cap{int(m.group(1))}")
            a.add(m.group(2))
        m2 = re.match(r"dom_(\d+)", base)
        if m2:
            a.add(f"dom{int(m2.group(1))}")
        return a

    def _manifest(self, mod, rel: str) -> Dict[str, Any]:
        """Extract manifest from a module docstring (intent/title + full text)."""
        doc = (mod.__doc__ or "")
        intent = ""
        for line in doc.splitlines():
            line = line.strip()
            if line.upper().startswith("INTENT:"):
                intent = line.split(":", 1)[1].strip()
                break
        base = os.path.basename(rel)[:-3]
        if not intent:
            for line in doc.splitlines():
                line = line.strip()
                if line and not set(line) <= set("=-_* #"):
                    intent = line
                    break
        text = " ".join([intent, base.replace("_", " "), doc])
        return {"file": rel, "intent": intent, "tokens": _tokens(text)}

    def _load_one(self, path: str):
        """Import one file and integrate it.

        Three outcomes, all recorded in self.known:
          - executable:      has a get_*/execute entry point -> by_alias (runnable)
          - semantic_only:   imports fine, no entry point -> known as a knowledge unit
          - import_error:    failed to import -> known as broken
        """
        rel = os.path.relpath(path, self.dock_dir)
        key = rel[:-3].replace(os.sep, "_")
        modname = f"vauros_uni_{key}"
        try:
            stem = os.path.basename(path)[:-3]
            if stem in sys.modules:
                mod = sys.modules[stem]
            else:
                spec = importlib.util.spec_from_file_location(modname, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sys.modules[modname] = mod
        except Exception as e:
            self.errors[key] = f"import: {e}"
            self.known[key] = {"file": rel, "executable": False,
                               "status": "import_error", "intent": rel,
                               "tokens": _tokens(rel)}
            return
        man = self._manifest(mod, rel)
        inst = self._find_entry(mod)
        if inst is None:
            # Knowledge module: integrate semantically so the dock/registry knows it
            self.known[key] = dict(man, executable=False, status="semantic_only")
            return
        aliases = self._aliases(rel)
        for alias in aliases:
            self.by_alias.setdefault(alias, inst)
        self.manifests[id(inst)] = man
        self.known[key] = dict(man, executable=True, status="executable",
                               aliases=aliases)



async def dispatch_instance(inst: Any, payload: dict) -> dict:
    """Execute an instance from the universal loader."""
    if not hasattr(inst, "execute"):
        return {"mode": "INCAPABLE", "reason": "no execute method"}
    try:
        result = await inst.execute(payload)
    except TypeError:
        # Try without payload
        result = await inst.execute()
    except Exception as e:
        logger.error(f"dispatch_instance execute failed: {e}")
        return {"mode": "DEFERRED", "reason": str(e)}
    return {"mode": "FULFILLED", "payload_uros": [result] if not isinstance(result, list) else result}


async def dispatch_capability(cap: Any, payload: dict) -> dict:
    """Execute a capability from the master."""
    if not hasattr(cap, "execute"):
        return {"mode": "INCAPABLE", "reason": "no execute method"}
    try:
        result = await cap.execute(payload)
    except TypeError:
        result = await cap.execute()
    except Exception as e:
        logger.error(f"dispatch_capability execute failed: {e}")
        return {"mode": "DEFERRED", "reason": str(e)}
    return {"mode": "FULFILLED", "payload_uros": [result] if not isinstance(result, list) else result}


async def dispatch_domain(dom: Any, payload: dict) -> dict:
    """Execute a domain from the master."""
    if not hasattr(dom, "execute"):
        return {"mode": "INCAPABLE", "reason": "no execute method"}
    try:
        result = await dom.execute(payload)
    except TypeError:
        result = await dom.execute()
    except Exception as e:
        logger.error(f"dispatch_domain execute failed: {e}")
        return {"mode": "DEFERRED", "reason": str(e)}
    return {"mode": "FULFILLED", "payload_uros": [result] if not isinstance(result, list) else result}

async def dispatch(master, dock_name: str, intent: str,
                   payload: Optional[Dict[str, Any]] = None,
                   context: Any = None, nte: Any = None,
                   dock_dir: Optional[str] = None) -> Optional[dict]:
    """Generic dispatcher. Resolves intent -> capability/domain/instance and executes."""
    caps = getattr(master, "capabilities", {})
    domains = getattr(master, "domains", {})
    payload = payload or {}

    # Strip dock prefix
    target = intent
    if intent.startswith(f"{dock_name}."):
        target = intent.split(".", 1)[1]

    # 1. Try master domains/capabilities with normalized forms
    normalized_variants = [target]
    import re
    if m := re.match(r"domains_dom_(\d+)", target):
        normalized_variants.append(f"Dom{int(m.group(1)):02d}")
    elif m := re.match(r"dom_?(\d+)$", target):
        normalized_variants.append(f"Dom{int(m.group(1)):02d}")
    elif m := re.match(r"capabilities_cap_(\d+)", target):
        normalized_variants.append(f"Cap{int(m.group(1))}")
    elif m := re.match(r"cap_?(\d+)(?:_.*)?$", target):
        normalized_variants.append(f"Cap{int(m.group(1))}")

    for v in normalized_variants:
        if v in domains:
            return await dispatch_domain(domains[v], payload)
        if v in caps:
            return await dispatch_capability(caps[v], payload)

    # 2. Fall back to universal loader
    if dock_dir:
        uni = get_universal(dock_dir, getattr(master, "bus", None))
        for v in [target] + normalized_variants:
            if v in uni.by_alias:
                return await dispatch_instance(uni.by_alias[v], payload)

    return None





# =====================================================================
# DOCK REGISTRATION HELPERS (commonly imported by docks)
# =====================================================================
def register_with_master(dock_name: str, capabilities: list = None, **kwargs):
    """
    Register a dock with the master registry.
    
    This is a convenience wrapper around get_registry().register_dock().
    """
    registry = get_registry()
    if hasattr(registry, 'register_dock'):
        return registry.register_dock(dock_name, capabilities or [], **kwargs)
    return None

def register_domain(domain_name: str, domain_id: str = None, **kwargs):
    """Register a domain with the registry."""
    registry = get_registry()
    if hasattr(registry, 'register_domain'):
        return registry.register_domain(domain_name, domain_id or domain_name, **kwargs)
    return None

def register_dock(dock_name: str, **kwargs):
    """Register a dock (alias for register_with_master)."""
    return register_with_master(dock_name, **kwargs)

def register_capability(capability_name: str, capability_ref: str = None, **kwargs):
    """Register a capability with the registry."""
    registry = get_registry()
    if hasattr(registry, 'register_capability'):
        return registry.register_capability(capability_name, capability_ref or capability_name, **kwargs)
    return None

# Update __all__
if '__all__' in dir():
    __all__.extend([
        'register_with_master',
        'register_domain',
        'register_dock',
        'register_capability',
    ])


# BASE-URO WIRING CONSTANTS (flat names docks import)
DOMAIN_ALIAS = "domain"
CAPABILITY_ALIAS = "capability"

def register_with_dock(dock_name, *a, **k):
    """Register an entity with a dock."""
    return register_dock(dock_name, *a, **k) if 'register_dock' in globals() else None

def invoke_capability(capability_name, *a, **k):
    """Invoke a registered capability by name via the universal loader."""
    try:
        loader = get_universal()
        if hasattr(loader, 'invoke'): return loader.invoke(capability_name, *a, **k)
        if hasattr(loader, 'dispatch'): return loader.dispatch(capability_name, *a, **k)
    except Exception:
        pass
    return None
