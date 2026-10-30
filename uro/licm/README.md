# LICM STANDARD LIBRARY (uro.licm)

Full URO-compliant implementation of the Loom Integration Capability Manifest contract.

Mandate:
- Every response is a URO envelope with URID pair and normalized 24-axis NTE.
- Provenance is explicit: LIVE, DERIVED, DEMO, or UNMEASURED.
- No fabricated metrics. Missing measurements must be UNMEASURED with reason.
- ACL tiers: read / write / control.
- Append-only event ring and immutable ledger.
- Control receipts are written BEFORE effects.
- Inter-dock calls use canonical TCP-first transport with HTTP fallback.

Endpoints exposed by build_licm_router:
- GET  /licm/manifest
- GET  /licm/status
- GET  /licm/events       (SSE + JSON fallback, since_seq resume)
- POST /licm/action       (ACL-gated)
- GET  /licm/nte
