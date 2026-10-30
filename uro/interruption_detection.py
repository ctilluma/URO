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


"""URO Core: Interruption Detection (Phase 3d.2).

Absence of expected evidence IS evidence of absence. This module provides
two composable monitors that feed the BeliefFaculty:

1. **InterruptionMonitor** — tracks health beliefs about components/docks.
   Used by: coordinator (inter-dock), observer (meta-monitoring).

2. **ServiceWatchdog** — background task that probes services and feeds
   heartbeat/interruption evidence into the BeliefFaculty.
   Used by: every dock (intra-dock), with dock-specific service lists.

Design laws:
- Only previously-healthy components can be 'interrupted'.
- Each interruption episode is distinct evidence; repeated checks saturate.
- Severity scales with silence duration (capped 1.0).
- Recovery injects confirmation evidence.
- Feeds the BeliefFaculty so health is a beta-posterior belief.

Example usage in a dock:
    from uro.interruption_detection import ServiceWatchdog
    from docks.cognitive.belief_faculty import BeliefFaculty, RedisStore
    
    faculty = BeliefFaculty(store=RedisStore(redis_client))
    watchdog = ServiceWatchdog(faculty)
    
    # Memory dock: watch external services
    watchdog.watch("qdrant_pool", check_qdrant, interval=5.0)
    watchdog.watch("redis_pool", check_redis, interval=5.0)
    
    # Boardroom dock: watch board members
    for member in board_members:
        watchdog.watch(f"member_{member.id}", member.check_health, interval=10.0)
    
    # Start background monitoring
    asyncio.create_task(watchdog.run())
"""

import time as _time
from typing import Dict, Any, Optional, List, Callable, Awaitable

DEFAULT_GRACE_MULTIPLIER = 2.0    # intervals of silence before 'interrupted'
DEFAULT_SATURATION_BEATS = 4.0    # missed beats at which severity reaches 1.0
DEFAULT_HEARTBEAT_TRUST = 0.6     # trust weight of establishing heartbeat
DEFAULT_RECOVERY_TRUST = 0.7      # trust weight of recovery confirmation
DEFAULT_INTERRUPTION_TRUST = 0.8  # trust weight of interruption counter-evidence


def health_claim(component: str) -> str:
    """Canonical claim format for health beliefs."""
    return f"{component} is healthy"


def interruption_severity(gap: float, expected_interval: float, saturation_beats: float) -> float:
    """Compute severity [0,1] based on silence duration relative to expected interval."""
    if expected_interval <= 0 or saturation_beats <= 0:
        return 1.0
    missed = gap / expected_interval
    return max(0.0, min(1.0, missed / saturation_beats))


class InterruptionMonitor:
    """Tracks health beliefs about components/docks.
    
    Used by coordinator to detect inter-dock flapping, or by observer
    for meta-monitoring.
    
    Example:
        monitor = InterruptionMonitor(faculty)
        monitor.register("memory", expected_interval=10.0)
        monitor.heartbeat("memory")  # component is alive
        events = monitor.check()     # returns list of interruptions
    """

    def __init__(self, faculty,
                 grace_multiplier: float = DEFAULT_GRACE_MULTIPLIER,
                 saturation_beats: float = DEFAULT_SATURATION_BEATS,
                 heartbeat_trust: float = DEFAULT_HEARTBEAT_TRUST,
                 recovery_trust: float = DEFAULT_RECOVERY_TRUST,
                 interruption_trust: float = DEFAULT_INTERRUPTION_TRUST):
        self.faculty = faculty
        self.grace_multiplier = grace_multiplier
        self.saturation_beats = saturation_beats
        self.heartbeat_trust = heartbeat_trust
        self.recovery_trust = recovery_trust
        self.interruption_trust = interruption_trust
        self.components: Dict[str, Dict[str, Any]] = {}

    def register(self, component: str, expected_interval: float, now: Optional[float] = None):
        """Register a component to monitor."""
        now = now if now is not None else _time.time()
        self.components[component] = {
            "expected_interval": float(expected_interval),
            "last_seen": now,
            "status": "unknown",
            "episode": 0,
            "interrupted_since": None,
        }

    def heartbeat(self, component: str, now: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """Record a heartbeat. Injects recovery evidence if was interrupted."""
        now = now if now is not None else _time.time()
        comp = self.components.get(component)
        if comp is None:
            return None
        
        prev = comp["status"]
        comp["last_seen"] = now
        
        if prev == "interrupted":
            # Recovery: inject confirmation evidence
            comp["status"] = "healthy"
            comp["interrupted_since"] = None
            self.faculty.ingest(health_claim(component), 
                                trust=self.recovery_trust,
                                origin=f"recovery:{component}:{comp['episode']}",
                                stance="confirm", 
                                now=now)
            return {"component": component, "event": "recovered", "episode": comp["episode"]}
        
        elif prev == "unknown":
            # First heartbeat: establish health
            comp["status"] = "healthy"
            self.faculty.ingest(health_claim(component), 
                                trust=self.heartbeat_trust,
                                origin=f"heartbeat:{component}", 
                                stance="confirm", 
                                now=now)
            return {"component": component, "event": "established"}
        
        return None  # already healthy: repetition is not evidence

    def check(self, now: Optional[float] = None) -> List[Dict[str, Any]]:
        """Scan for interruptions. Injects counter-evidence for new ones."""
        now = now if now is not None else _time.time()
        events = []
        
        for component, comp in self.components.items():
            if comp["status"] != "healthy":
                continue
            
            gap = now - comp["last_seen"]
            threshold = comp["expected_interval"] * self.grace_multiplier
            
            if gap > threshold:
                # Interruption detected
                comp["status"] = "interrupted"
                comp["episode"] += 1
                comp["interrupted_since"] = now
                severity = interruption_severity(gap, comp["expected_interval"], self.saturation_beats)
                
                # Inject counter-evidence
                self.faculty.ingest(health_claim(component), 
                                    trust=severity,
                                    origin=f"interruption:{component}:{comp['episode']}",
                                    stance="counter", 
                                    now=now)
                
                events.append({
                    "component": component, 
                    "event": "interrupted",
                    "episode": comp["episode"], 
                    "gap": gap, 
                    "severity": severity
                })
        
        return events

    def belief_for(self, component: str) -> Dict[str, Any]:
        """Get current belief state for a component."""
        return self.faculty.query(health_claim(component))

    def all_beliefs(self) -> Dict[str, Dict[str, Any]]:
        """Get belief states for all registered components."""
        return {comp: self.belief_for(comp) for comp in self.components}


class ServiceWatchdog:
    """Background service health monitor.
    
    Each dock applies this to its internal services. The watchdog periodically
    probes each service and feeds heartbeat/interruption evidence into the
    BeliefFaculty.
    
    Example:
        # Memory dock: watch external services
        watchdog = ServiceWatchdog(faculty)
        watchdog.watch("qdrant_pool", check_qdrant, interval=5.0)
        watchdog.watch("redis_pool", check_redis, interval=5.0)
        asyncio.create_task(watchdog.run())
        
        # Boardroom dock: watch board members
        watchdog = ServiceWatchdog(faculty)
        for member in board_members:
            watchdog.watch(f"member_{member.id}", member.check_health, interval=10.0)
        asyncio.create_task(watchdog.run())
    """

    def __init__(self, faculty, default_interval: float = 5.0):
        self.faculty = faculty
        self.default_interval = default_interval
        self.monitors: Dict[str, Dict[str, Any]] = {}
        self._running = False

    def watch(self, service_name: str, check_fn: Callable[[], Awaitable[bool]], 
              interval: Optional[float] = None):
        """Register a service to monitor.
        
        Args:
            service_name: canonical name (e.g., "qdrant_pool", "member_alice")
            check_fn: async function that returns True if healthy, raises on failure
            interval: seconds between checks (default: self.default_interval)
        """
        interval = interval or self.default_interval
        self.monitors[service_name] = {
            "check_fn": check_fn,
            "interval": float(interval),
            "status": "unknown",
            "last_seen": None,
            "episode": 0,
            "last_error": None,
        }
        # Ensure belief exists
        claim = health_claim(service_name)
        self.faculty.query(claim)

    async def run(self, stop_event=None):
        """Background loop: periodically check each service.
        
        Args:
            stop_event: asyncio.Event that, when set, stops the loop
        """
        import asyncio
        
        self._running = True
        while not (stop_event and stop_event.is_set()):
            for svc_name, state in self.monitors.items():
                if not self._running:
                    break
                
                try:
                    # Probe the service
                    result = await asyncio.wait_for(
                        state["check_fn"](), 
                        timeout=state["interval"] * 0.9
                    )
                    
                    # Success: heartbeat
                    prev_status = state["status"]
                    state["status"] = "healthy"
                    state["last_seen"] = _time.time()
                    state["last_error"] = None
                    
                    if prev_status == "interrupted":
                        # Recovery
                        state["episode"] += 1
                        self.faculty.ingest(
                            health_claim(svc_name),
                            trust=DEFAULT_RECOVERY_TRUST,
                            origin=f"recovery:{svc_name}:{state['episode']}",
                            stance="confirm"
                        )
                    elif prev_status == "unknown":
                        # First successful check
                        self.faculty.ingest(
                            health_claim(svc_name),
                            trust=DEFAULT_HEARTBEAT_TRUST,
                            origin=f"heartbeat:{svc_name}",
                            stance="confirm"
                        )
                    # else: already healthy, no new evidence (repetition saturates)
                    
                except Exception as e:
                    # Failure: interruption
                    prev_status = state["status"]
                    if prev_status == "healthy":
                        state["status"] = "interrupted"
                        state["episode"] += 1
                        state["last_seen"] = _time.time()
                        state["last_error"] = str(e)
                        
                        self.faculty.ingest(
                            health_claim(svc_name),
                            trust=DEFAULT_INTERRUPTION_TRUST,
                            origin=f"interruption:{svc_name}:{state['episode']}",
                            stance="counter"
                        )
                    elif prev_status == "unknown":
                        # Never succeeded: mark as failed
                        state["status"] = "interrupted"
                        state["last_error"] = str(e)
                    # else: already interrupted, no new evidence (repetition saturates)
            
            # Sleep until next check cycle
            next_interval = min(m["interval"] for m in self.monitors.values()) if self.monitors else self.default_interval
            try:
                await asyncio.sleep(next_interval)
            except asyncio.CancelledError:
                break
        
        self._running = False

    def stop(self):
        """Signal the watchdog to stop."""
        self._running = False

    def status(self, service_name: str) -> Dict[str, Any]:
        """Get current belief state for a service."""
        claim = health_claim(service_name)
        return self.faculty.query(claim)

    def all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get belief states for all watched services."""
        return {svc: self.status(svc) for svc in self.monitors}

    def get_monitor_state(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get raw monitor state (status, last_seen, episode, last_error)."""
        state = self.monitors.get(service_name)
        return state.copy() if state else None
