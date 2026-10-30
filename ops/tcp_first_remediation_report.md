# TCP-First Transport Remediation Report

- **Generated:** 2026-10-21T04:29:34Z
- **Repo HEAD:** 073996510
- **Mandate:** S9.10 TCP-first transport, S13.2 dock checklist, S14.7 no raw httpx between docks
- **Editing rule:** S14.5 marker-bounded exact block replacement only. THIS PASS IS READ-ONLY; no live modules modified.
- **Baseline:** synapse suite ALL ASPECTS PASS at commit 8a20c20a5 (prior run).

## 1. Raw httpx call-site classification

| File | Classification | Line(s) | Marker blocks present | References send_to_dock_async |
|---|---|---|---|---|
| uro/belief_faculty.py | **VIOLATION** — route via send_to_dock_async | 180,197 (n=2) | 0 | 0 |
| uro/cognition/persistence.py | **VIOLATION** — route via send_to_dock_async | 29 (n=1) | 0 | 0 |
| uro/cognitive_integration/bridge.py | **VIOLATION** — route via send_to_dock_async | 52 (n=1) | 0 | 0 |
| uro/coordinator_bus.py | **VIOLATION** — route via send_to_dock_async | 138 (n=1) | 0 | 0 |
| uro/transport/inter_dock_client.py | ALLOWED — transport substrate (implements S9.10 HTTP fallback) | 65 (n=1) | 0 | 7 |
| uro/transport/universal_client.py | ALLOWED — transport substrate (implements S9.10 HTTP fallback) | 338,425 (n=2) | 0 | 0 |
| uro/transport/universal_listener.py | ALLOWED — transport substrate (implements S9.10 HTTP fallback) | 55,133 (n=2) | 0 | 0 |
| uro/uro_interceptor.py | **VIOLATION** — route via send_to_dock_async | 59,60,113,114 (n=4) | 0 | 0 |

## 2. Violation call-site context (input for S14.5 exact-block planning)

### uro/belief_faculty.py

- line 180:
```python
 176|     async def _store(self, state: Dict[str, Any]) -> None:
 177|         """Store belief state via Memory dock."""
 178|         import httpx
 179|         try:
 180|             async with httpx.AsyncClient(timeout=5.0) as client:
 181|                 await client.post(
 182|                     f"{self.memory_dock_url}/memory/store",
 183|                     json={
 184|                         "key": self.key,
 185|                         "data": {"state": state},
 186|                         "memory_type": "belief_state",
 187|                         "ttl_seconds": None  # Permanent
 188|                     }
```

- line 197:
```python
 193|     async def _load(self) -> Optional[Dict[str, Any]]:
 194|         """Load belief state via Memory dock."""
 195|         import httpx
 196|         try:
 197|             async with httpx.AsyncClient(timeout=5.0) as client:
 198|                 response = await client.get(
 199|                     f"{self.memory_dock_url}/memory/retrieve/{self.key}",
 200|                     timeout=5.0
 201|                 )
 202|                 if response.status_code == 200:
 203|                     data = response.json()
 204|                     return data.get("data", {}).get("state")
 205|         except Exception:
```

### uro/cognition/persistence.py

- line 29:
```python
  25| 
  26|     def __init__(self, dock_name: str = "cognitive"):
  27|         self.dock_name = dock_name
  28|         self.memory_url = self._get_memory_url()
  29|         self.client = httpx.AsyncClient(timeout=20.0)
  30| 
  31|     def _get_memory_url(self) -> str:
  32|         """Resolve memory dock URL."""
  33|         env = os.getenv("AURA_ENV", "prod")
  34|         for host in [f"memory_{env}", "memory_prod", "memory"]:
  35|             try:
  36|                 return f"http://{host}:8000"
  37|             except:
```

### uro/cognitive_integration/bridge.py

- line 52:
```python
  48|         "role": "coder"
  49|     }
  50|     
  51|     try:
  52|         async with httpx.AsyncClient(timeout=300.0) as client:
  53|             # Cognitive's /process_query handles the cache lookup and LLM fallback
  54|             resp = await client.post(f"{COGNITIVE_URL}/process_query", json=payload)
  55|             resp.raise_for_status()
  56|             data = resp.json()
  57|             
  58|             # Extract generated code from Cognitive's response
  59|             # Cognitive often returns the result in 'rag_context', 'response', or 'working_memory'
  60|             generated = data.get("generated_code") or data.get("response", {}).get("text", "")
```

### uro/coordinator_bus.py

- line 138:
```python
 134| class CoordinatorBus:
 135|     def __init__(self, dock_name: str):
 136|         self.dock_name = dock_name
 137|         self.coordinator_url = get_coordinator_url()
 138|         self.client = httpx.AsyncClient(timeout=30.0)
 139|         self._registered = False
 140|         self._helper = CanonicalUROHelper(dock_name=dock_name)
 141|         self._synapses: Dict[str, Any] = {}
 142|         logger.info(f"🚌 CoordinatorBus initialized for {dock_name} -> {self.coordinator_url}")
 143|         
 144|         # TCP transport state
 145|         self._tcp_port = 9100
 146|         self._tcp_failed_cache = {}  # dock -> timestamp of last TCP failure
```

### uro/uro_interceptor.py

- line 59:
```python
  55| 
  56| # ============================================================================
  57| # PATCH HTTPX (Async)
  58| # ============================================================================
  59| _original_httpx_post = httpx.AsyncClient.post
  60| _original_httpx_get = httpx.AsyncClient.get
  61| 
  62| async def _patched_httpx_post(self, url, *args, **kwargs):
  63|     is_dock, target_dock = is_dock_url(url)
  64|     if is_dock:
  65|         logger.info(f"[URO Interceptor] ⚡ Redirecting httpx POST {url} -> Coordinator (Target: {target_dock})")
  66|         headers = kwargs.get("headers", {})
  67|         headers["X-URO-Target-Dock"] = target_dock
```

- line 60:
```python
  56| # ============================================================================
  57| # PATCH HTTPX (Async)
  58| # ============================================================================
  59| _original_httpx_post = httpx.AsyncClient.post
  60| _original_httpx_get = httpx.AsyncClient.get
  61| 
  62| async def _patched_httpx_post(self, url, *args, **kwargs):
  63|     is_dock, target_dock = is_dock_url(url)
  64|     if is_dock:
  65|         logger.info(f"[URO Interceptor] ⚡ Redirecting httpx POST {url} -> Coordinator (Target: {target_dock})")
  66|         headers = kwargs.get("headers", {})
  67|         headers["X-URO-Target-Dock"] = target_dock
  68|         headers["X-URO-Original-URL"] = url
```

- line 113:
```python
 109|         new_url = f"{coord_url}{parsed.path}"
 110|         return await _original_httpx_get(self, new_url, *args, **kwargs)
 111|     return await _original_httpx_get(self, url, *args, **kwargs)
 112| 
 113| httpx.AsyncClient.post = _patched_httpx_post
 114| httpx.AsyncClient.get = _patched_httpx_get
 115| 
 116| # ============================================================================
 117| # PATCH REQUESTS (Sync)
 118| # ============================================================================
 119| _original_requests_post = requests.post
 120| _original_requests_get = requests.get
 121| 
```

- line 114:
```python
 110|         return await _original_httpx_get(self, new_url, *args, **kwargs)
 111|     return await _original_httpx_get(self, url, *args, **kwargs)
 112| 
 113| httpx.AsyncClient.post = _patched_httpx_post
 114| httpx.AsyncClient.get = _patched_httpx_get
 115| 
 116| # ============================================================================
 117| # PATCH REQUESTS (Sync)
 118| # ============================================================================
 119| _original_requests_post = requests.post
 120| _original_requests_get = requests.get
 121| 
 122| def _patched_requests_post(url, *args, **kwargs):
```

## 3. FastAPI listener wiring audit (S13.2: install_tcp_listener at startup)

| File instantiating FastAPI | install_tcp_listener wired |
|---|---|
| uro/transport/universal_listener.py | YES |

## 4. Secondary sweep — non-canonical HTTP clients (requests / aiohttp)

- uro/uro_interceptor.py — **review: non-canonical HTTP client**

## 5. OPAR plan — next actions (to be executed next pass)

1. For each VIOLATION in S2: bound the offending region with marker blocks
   (# === START: <name> === / # === END: <name> ===), verify occurrence count == 1,
   then exact-block-replace the httpx call with
   send_to_dock_async(dock_name=..., endpoint=..., payload=..., method=..., timeout=5.0).
2. For each unwired FastAPI app in S3: exact-block-add
   install_tcp_listener(app, dock_name=...) at startup.
3. Re-run synapse suite (S14.6) — exit 0 required.
4. Rollout: ./ops/rollout_profile.sh dev -> staging -> uat -> prod. Never skip a profile.
5. Re-run transport audit — target: 0 raw httpx sites outside uro/transport/.
