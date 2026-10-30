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


from __future__ import annotations

import time
from typing import Any, Dict, Tuple
from uro.base_uros import UROEnvelope
from uro.core.urid import URID
from .hashutil import seal_object
from .nte import normalize_nte_state
from .provenance import normalize_provenance
from .timeutil import now_iso

def _serialize_urid(obj: Any) -> Any:
    """Recursively serialize URID objects to hex strings."""
    if isinstance(obj, URID):
        return obj.to_hex() if hasattr(obj, 'to_hex') else str(obj)
    if isinstance(obj, dict):
        return {k: _serialize_urid(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize_urid(v) for v in obj]
    return obj

def licm_envelope(
    urid_pair: Any,
    payload: Any,
    nte_state: Any,
    provenance: Any,
    generated_at: str | None = None,
) -> Dict[str, Any]:
    """
    URO response envelope using canonical UROEnvelope.
    Ensures all returned data is JSON-serializable for FastAPI.
    """
    if isinstance(urid_pair, dict):
        urid1_src = urid_pair.get("urid1")
        urid2_src = urid_pair.get("urid2")
    else:
        urid1_src = urid2_src = None

    urid1 = urid1_src if isinstance(urid1_src, URID) else URID.generate(seed=str(urid1_src or "unknown"))
    urid2 = urid2_src if isinstance(urid2_src, URID) else URID.generate(seed=str(urid2_src or "unknown"))

    normalized_nte = normalize_nte_state(nte_state)
    norm_prov = normalize_provenance(provenance)
    
    # Create canonical UROEnvelope
    env = UROEnvelope(
        urid=urid1,
        payload=payload,
        timestamp=time.time()
    )
    
    # Get dict representation
    result = env.model_dump() if hasattr(env, 'model_dump') else env.dict()
    
    # Ensure URID is serialized to string for FastAPI jsonable_encoder
    result = _serialize_urid(result)
    
    # Extend with LICM-specific fields at the top level
    result["urid_pair"] = {
        "urid1_hex": urid1.to_hex() if hasattr(urid1, 'to_hex') else str(urid1),
        "urid2_hex": urid2.to_hex() if hasattr(urid2, 'to_hex') else str(urid2),
    }
    result["nte_state"] = normalized_nte
    result["provenance"] = norm_prov
    result["generated_at"] = generated_at or now_iso()
    
    # Compute INAHASH seal for the entire envelope
    digest, algorithm = seal_object(result)
    result["inahash"] = digest
    result["hash_algorithm"] = algorithm
    
    return result

def compute_envelope_seal(envelope: Dict[str, Any]) -> Tuple[str, str]:
    body = {k: v for k, v in envelope.items() if k not in ("inahash", "hash_algorithm")}
    return seal_object(body)
