#!/usr/bin/env python3
# PURPOSE: Generate URO_API_REFERENCE.md from the measured canonical surface.
import importlib
import inspect
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(".").resolve()))
NL = chr(10)
CANON = {
    "primitives": ["uro.constants", "uro.exceptions", "uro.types", "uro.genesis_trust"],
    "core": ["uro.core.urid", "uro.core.uro", "uro.core.header", "uro.core.components",
             "uro.core.inheritance", "uro.core.datetime_uro", "uro.core.space"],
    "nte": ["uro.nte.axes", "uro.nte.state", "uro.nte.level", "uro.nte.cross_talk",
            "uro.nte.polarity", "uro.nte.math_influence", "uro.nte.firing",
            "uro.nte.reward", "uro.nte.ans", "uro.nte.neurotransmitters", "uro.nte.nte_state"],
    "synapse": ["uro.synapse.engine", "uro.synapse.vector", "uro.synapse.persistence",
                "uro.synapse.topic_trust"],
    "security": ["uro.security.hashing", "uro.security.encryption", "uro.security.pki",
                 "uro.security.identity", "uro.security.policy", "uro.security.acl",
                 "uro.security.ldap", "uro.security.circle_security",
                 "uro.security.field_encryption", "uro.security.user_keys", "uro.security.custody"],
    "memory": ["uro.memory.engine", "uro.memory.decay"],
    "pathing": ["uro.pathing.beacons", "uro.pathing.connectors", "uro.pathing.onion",
                "uro.pathing.trust", "uro.pathing.cro_matrix", "uro.pathing.path_ops",
                "uro.pathing.stack_processing", "uro.pathing.swarms"],
    "relations": ["uro.relations.association", "uro.relations.pathing"],
    "interchange": ["uro.aupi", "uro.interchange", "uro.hot_swap", "uro.self_loading", "uro.priority"],
    "learning": ["uro.learning.primitives", "uro.learning.dicho", "uro.learning.action_uro",
                 "uro.learning.attention", "uro.learning.aloneness", "uro.learning.cas_loop"],
    "opar": ["uro.opar.stages", "uro.opar.protocol", "uro.opar.base", "uro.opar.grounding",
             "uro.opar.compliance"],
    "quad": ["uro.quad.quad_capability", "uro.quad.character_condition", "uro.quad.croate"],
    "boot": ["uro.boot.boot_sequence", "uro.boot.child_boot", "uro.boot.self_check"],
    "economy": ["uro.economy.goods", "uro.economy.ledger", "uro.economy.pricing",
                "uro.economy.marketplace", "uro.economy.currency", "uro.economy.token_transfer",
                "uro.economy.social_pricing", "uro.economy.supply_chain"],
    "cognition": ["uro.cognition.fuzzy", "uro.cognition.verdict", "uro.cognition.matrix",
                  "uro.cognition.cognitive_fuzzy", "uro.cognition.memory_fuzzy",
                  "uro.cognition.myelination", "uro.cognition.core", "uro.cognition.persistence"],
}
def fmt_sig(fn):
    try:
        return str(inspect.signature(fn))
    except Exception:
        return "(...)"
def first_doc(obj, limit=3):
    doc = inspect.getdoc(obj) or ""
    lines = [l for l in doc.splitlines() if l.strip()]
    return " ".join(lines[:limit]).strip()
out = []
out.append("# URO Library API Reference")
out.append("")
out.append("Generated from source by _BUILD/tools/generate_api_reference.py.")
out.append("Covers the measured canonical surface (16 suites, 160 checks, uro-build/phase-16-done).")
out.append("Legacy shim, vauros_*, and dock-internal layers are excluded by ADR.")
out.append("")
failures = []
counts = {"modules": 0, "classes": 0, "functions": 0}
for section, mods in CANON.items():
    out.append("## " + section)
    out.append("")
    for mpath in mods:
        try:
            mod = importlib.import_module(mpath)
        except Exception as exc:
            failures.append((mpath, type(exc).__name__ + ": " + str(exc)))
            out.append("### " + mpath + " (IMPORT FAILED)")
            out.append("")
            continue
        counts["modules"] += 1
        out.append("### " + mpath)
        md = first_doc(mod, 2)
        if md:
            out.append("")
            out.append(md)
        names = getattr(mod, "__all__", None) or [n for n in dir(mod) if not n.startswith("_")]
        ordered = [n for n in vars(mod) if n in names] + [n for n in names if n not in vars(mod)]
        seen_ids = set()
        for name in ordered:
            obj = getattr(mod, name, None)
            if obj is None or id(obj) in seen_ids:
                continue
            if getattr(obj, "__module__", None) != mpath:
                continue
            if inspect.isclass(obj):
                seen_ids.add(id(obj))
                counts["classes"] += 1
                out.append("")
                out.append("#### class " + name)
                cd = first_doc(obj, 2)
                if cd:
                    out.append("")
                    out.append(cd)
                fields = getattr(obj, "model_fields", None)
                if fields:
                    out.append("")
                    out.append("Fields:")
                    out.append("")
                    for fname, finfo in fields.items():
                        out.append("- " + fname + ": " + str(finfo.annotation))
                elif hasattr(obj, "__dataclass_fields__"):
                    out.append("")
                    out.append("Fields:")
                    out.append("")
                    for fname, f in obj.__dataclass_fields__.items():
                        out.append("- " + fname + ": " + str(f.type))
                for mname, memb in vars(obj).items():
                    if mname.startswith("_") and mname != "__init__":
                        continue
                    if inspect.isfunction(memb) or inspect.ismethod(memb):
                        d = first_doc(memb, 1)
                        line = "- `" + mname + fmt_sig(memb) + "`"
                        if d:
                            line += " - " + d
                        out.append("")
                        out.append(line)
            elif inspect.isfunction(obj):
                seen_ids.add(id(obj))
                counts["functions"] += 1
                d = first_doc(obj, 2)
                out.append("")
                out.append("#### " + name + fmt_sig(obj))
                if d:
                    out.append("")
                    out.append(d)
        out.append("")
out.append("## Generation Summary")
out.append("")
out.append("modules: %d | classes: %d | functions: %d | import failures: %d" % (counts["modules"], counts["classes"], counts["functions"], len(failures)))
for mpath, err in failures:
    out.append("- " + mpath + " :: " + err)
pathlib.Path("URO_API_REFERENCE.md").write_text(NL.join(out) + NL, encoding="utf-8")
print("wrote URO_API_REFERENCE.md ::", counts, "failures:", len(failures))
