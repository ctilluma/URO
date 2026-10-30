LICM DOCK WIRING CHECKLIST
==========================

1. Create a manifest dict or LICMManifest instance.
2. Create providers:
   - status: returns provenance-tagged fields via live/derive_from_registry/unmeasured
   - nte: returns partial NTE state, normalized by the library
   - actions: mapping of action name to callable or {handler, tier}
   - events_source: optional callable returning extra event dicts
3. router = build_licm_router(dock_name, manifest, providers)
4. app.include_router(router)
5. install_tcp_listener(app, dock_name=dock_name) at startup.
6. Loom/proxies call other docks only through uro.licm.client.licm_call.
7. Dock names are env-suffixed automatically: dock_{AURA_ENV}.

ACL matrix:
- read: authenticated operator, dock-pki, admin, root, varuos_admin
- write: dock-pki, admin, root, varuos_admin
- control: varuos_admin only

Headers:
- X-URO-Principal
- X-URO-Role
