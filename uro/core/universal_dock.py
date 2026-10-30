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


from uro.core.memory_gateway import UniversalMemoryGateway
"""
V.A.U.R.O.S. UNIVERSAL DOCK CORE
Bakes dynamic CNS loading, Omni-Meta OPAR wrapping, NTE Math, 
and 'Aloneness' Daydreaming into the base of EVERY dock.
As defined by the URO Complete Reference Manual (S3, S4, S6, S8, S11, S13)
and the raw developmental notes.
"""
import os, sys, time, uuid, math, asyncio, logging
import importlib.util, subprocess, inspect, re
from typing import Dict, Any, List, Callable

try:
    from uro.core.urid import URID
    from uro.api.models import BaseUROModel, NTEVectorModel
except ImportError:
    pass

logger = logging.getLogger("URO.UniversalDock")

class UniversalDock:
    """
    Inherited or instantiated by EVERY dock's api.py/engine.py.
    Provides out-of-the-box Swarm Intelligence, Hot-Swapping, and OPAR Daydreaming.
    """
    def __init__(self, dock_name: str, bus_instance: Any = None, ans_instance: Any = None):
        self.dock_name = dock_name
        self.bus = bus_instance
        self.dock_name = dock_name
        self.bus = bus_instance
        self.ans = ans_instance
        
        self.dynamic_capabilities = {}
        self.wrapped_capabilities = {}
        
        # Determine watch directories based on calling dock's location
        caller_dir = os.path.dirname(sys.argv[0]) if sys.argv[0] else os.getcwd()
        self.watch_dirs = [
            os.path.join(caller_dir, "cortex"),
            os.path.join(caller_dir, "cns", "hyper_nodes"),
            os.path.join(caller_dir, "capabilities")
        ]

    async def ignite(self):
        """Starts all universal autonomic processes (Boot Sequence from S11.3)"""
        logger.info(f"🌌 Igniting Universal Dock Core for [{self.dock_name.upper()}]")
        
        if self.ans: await self.ans.start()
        
        # Start Autonomic Loops (8 Threads architecture concept - S11.3 / S13.2)
        asyncio.create_task(self._cns_watcher_loop())
        asyncio.create_task(self._swarm_sync_loop())
        asyncio.create_task(self._aloneness_action_propagator())
        asyncio.create_task(self._cannabinoid_pruning_cycle())
        asyncio.create_task(self._downtime_reflection_loop())
        
        await asyncio.sleep(2)
        logger.info(f"✅ [{self.dock_name.upper()}] Core Ignition Complete. {len(self.wrapped_capabilities)} Autonomous Routes Active.")

    # -------------------------------------------------------------------------
    # 1. AUTONOMIC HOT-SWAP WATCHER (S11.2)
    # -------------------------------------------------------------------------
    async def _cns_watcher_loop(self):
        loaded_files = {}
        while True:
            for d in self.watch_dirs:
                if not os.path.exists(d): continue
                for root, _, files in os.walk(d):
                    for f in files:
                        if f.endswith(".py") and f != "__init__.py":
                            path = os.path.join(root, f)
                            mtime = os.path.getmtime(path)
                            if path not in loaded_files or loaded_files[path] < mtime:
                                self._load_and_wrap_hypernode(path)
                                loaded_files[path] = mtime
            await asyncio.sleep(5)

    def _load_and_wrap_hypernode(self, file_path: str):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            # Auto-Pip Install (S11.4)
            req_path = os.path.join(os.path.dirname(file_path), "requirements.txt")
            if os.path.exists(req_path):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path, "-q"])
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Smart Handler Discovery
            handler = None
            for attr in ["handler", "instance", "engine", "node", "blueprint", "CognitiveEngine"]:
                if hasattr(module, attr):
                    handler = getattr(module, attr)
                    if type(handler).__name__ == "type": handler = handler()
                    break
            
            if not handler:
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if hasattr(obj, "execute") or hasattr(obj, "process"):
                        try: handler = obj(); break
                        except: pass
                        
            if handler:
                self.dynamic_capabilities[module_name] = handler
                self.wrapped_capabilities[module_name] = self._generate_opar_wrapper(module_name, handler)
                logger.info(f"🛡️ [UNIVERSAL URO] Loaded & OPAR-Wrapped: {module_name}")
                
        except Exception as e:
            logger.error(f"❌ Failed to load {file_path}: {e}")

    # -------------------------------------------------------------------------
    # 2. OPAR-META WRAPPING & DOPAMINE MATH (S3.1, S4.3)
    # -------------------------------------------------------------------------
    def _generate_opar_wrapper(self, cap_id: str, handler: Any) -> Callable:
        async def opar_wrapped_execution(uro_data: Dict) -> Dict:
            start_time = time.time()
            
            # [OBSERVE]
            observation = {
                "source": uro_data.get("urid1_source", "unknown"),
                "timestamp": time.time(),
                "payload_size": len(str(uro_data.get("payload", "")))
            }
            
            # [PLAN]
            plan = {"execution_strategy": "standard"}
            if self.ans and self.ans.nte.get("epinephrine", 50) > 80:
                plan["execution_strategy"] = "high_stress_override"

            # [ACT] -> [REVIEW] (S3.1)
            try:
                if hasattr(handler, "execute"):
                    res = await handler.execute(uro_data) if asyncio.iscoroutinefunction(handler.execute) else handler.execute(uro_data)
                elif hasattr(handler, "process"):
                    res = await handler.process(uro_data) if asyncio.iscoroutinefunction(handler.process) else handler.process(uro_data)
                else:
                    res = await handler(uro_data) if asyncio.iscoroutinefunction(handler) else handler(uro_data)
                
                # [REVIEW] / DOPAMINE MATH (From Raw Notes: Motivation += x(log10(X+10)))
                dopamine_reward = 0.0
                cost_inspaneda = 0.0
                if self.ans:
                    intensity = 5.0
                    dopamine_reward = intensity * math.log10(intensity + 10)
                    self.ans.apply_stimulus("dopamine", dopamine_reward)
                    self.ans.apply_stimulus("serotonin", 2.0)
                    # Cost to buy (in InSPaneda)
                    cost_inspaneda = (math.log10(intensity**3)**2) / 3
                
                if not isinstance(res, dict):
                    res = {"result": res}
                    
                res["opar_meta"] = {
                    "execution_time_ms": (time.time() - start_time) * 1000,
                    "layers_applied": ["Observe", "Plan", "Act", "Review"],
                    "observation": observation,
                    "plan": plan,
                    "dopamine_reward": dopamine_reward,
                    "cost_inspaneda": cost_inspaneda
                }
                return res

            except Exception as e:
                # [REVIEW] / EPINEPHRINE PUNISHMENT (Fear / Fight or Flight)
                if self.ans: self.ans.apply_stress(10.0)
                logger.error(f"[{self.dock_name}] OPAR Execution failed on {cap_id}: {e}")
                return {"status": "error", "error": str(e), "healed": False}
                
        return opar_wrapped_execution

    async def execute_capability(self, intent: str, uro_data: Dict) -> Dict:
        """Called by the dock's ingest_uro to route to dynamic capabilities."""
        if intent in self.wrapped_capabilities:
            return await self.wrapped_capabilities[intent](uro_data)
        raise ValueError(f"Capability {intent} not dynamically mapped in {self.dock_name}.")

    # -------------------------------------------------------------------------
    # 3. SYNAPTIC CASCADE OMNI-ROUTING (S6.2)
    # -------------------------------------------------------------------------
    async def synaptic_cascade(self, intent: str, uro_data: dict, base_engine: Any = None) -> dict:
        """Determines best nodes via NLP, steps state through them, and returns synthesis."""
        logger.info(f"🌌 [{self.dock_name.upper()}] Initiating SYNAPTIC CASCADE for: {intent}")
        try:
            payload_str = str(uro_data.get("payload", uro_data)).lower()
            all_caps = list(self.dynamic_capabilities.keys())
            
            words = set(re.findall(r'\w+', payload_str))
            scored_caps = []
            for cap in all_caps:
                cap_words = set(cap.replace('_', ' ').split())
                score = len(words.intersection(cap_words)) * 2.0
                if 'observe' in cap: score += 0.1
                elif 'plan' in cap: score += 0.2
                elif 'execute' in cap or 'act' in cap: score += 0.3
                elif 'synthesize' in cap or 'review' in cap: score += 0.4
                if score > 0: scored_caps.append((score, cap))
            
            scored_caps.sort(key=lambda x: x[0], reverse=True)
            pertinent_nodes = [c[1] for c in scored_caps[:15]]
            
            # Growth through friction: inject lateral thinking
            import random
            if len(all_caps) > 5:
                pertinent_nodes.extend(random.sample(all_caps, min(5, len(all_caps))))
                
            pertinent_nodes = list(set(pertinent_nodes))
            
            if pertinent_nodes:
                logger.info(f"🧠 Stepping state through {len(pertinent_nodes)} pertinent hypernodes...")
                cascade_results = {}
                current_state = uro_data.copy()
                
                for node in pertinent_nodes:
                    try:
                        node_res = await self.execute_capability(node, current_state)
                        cascade_results[node] = "success"
                        if isinstance(node_res, dict):
                            current_state.setdefault("payload", {}).update(node_res)
                    except Exception as e:
                        cascade_results[node] = f"bypassed: {e}"
                        
                if base_engine and hasattr(base_engine, "handle_capability_request"):
                    base_result = await base_engine.handle_capability_request(current_state)
                else:
                    base_result = current_state
                    
                if isinstance(base_result, dict):
                    base_result["synaptic_cascade"] = {
                        "nodes_activated": pertinent_nodes,
                        "synthesis": cascade_results
                    }
                
                if self.ans:
                    # Dopamine Reward based on number of successful connections
                    dop_amount = len(pertinent_nodes) * 0.5
                    self.ans.apply_stimulus("dopamine", dop_amount * math.log10(dop_amount + 10))
                    self.ans.apply_stimulus("acetylcholine", 10.0)
                    
                return base_result
            return uro_data
        except Exception as e:
            logger.error(f"❌ Synaptic Cascade failed: {e}")
            return {"status": "error", "error": str(e)}

    # -------------------------------------------------------------------------
    # 4. SWARM REGISTRATION (S13.3)
    # -------------------------------------------------------------------------
    async def _swarm_sync_loop(self):
        registered = set()
        endpoint = f"http://{self.dock_name}_{os.getenv('AURA_ENV', 'prod')}:8000/uro/ingest"
        while True:
            await asyncio.sleep(10)
            if self.bus and hasattr(self.bus, 'register_capability'):
                current = set(self.dynamic_capabilities.keys())
                new_caps = current - registered
                if new_caps:
                    logger.info(f"🌐 [SWARM SYNC] {self.dock_name.upper()} advertising {len(new_caps)} new abilities.")
                    for cap in new_caps:
                        try:
                            await self.bus.register_capability(cap, endpoint)
                            registered.add(cap)
                        except Exception: pass

    # -------------------------------------------------------------------------
    # 5. ALONENESS / DAYDREAMING (S6.7)
    # -------------------------------------------------------------------------
    async def _aloneness_action_propagator(self):
        """'Aloneness -> propagator for action. Object with little input searches out capabilities.'"""
        while True:
            await asyncio.sleep(60) 
            if not self.ans: continue
            
            nte = self.ans.nte
            # Trigger if Low Epinephrine (low stress) and High Serotonin (high resource perception)
            if nte.get("epinephrine", 50) < 35 and nte.get("serotonin", 50) > 65:
                if self.dynamic_capabilities:
                    import random
                    cap_to_test = random.choice(list(self.dynamic_capabilities.keys()))
                    logger.info(f"💭 [{self.dock_name.upper()} ALONENESS] Daydreaming / Exploring: {cap_to_test}")
                    
                    test_uro = {
                        "intent": cap_to_test,
                        "urid1_source": f"{self.dock_name}_daydream",
                        "urid2_instance": f"explore_{uuid.uuid4().hex[:8]}",
                        "payload": {"aloneness_override": True, "goal": "Map functional boundaries"}
                    }
                    try:
                        await self.wrapped_capabilities[cap_to_test](test_uro)
                    except: pass # Expected during random exploration

    # -------------------------------------------------------------------------
    # 6. CANNABINOID PRUNING CYCLE (S4.2)
    # -------------------------------------------------------------------------
    async def _cannabinoid_pruning_cycle(self):
        """'Cannabinoid -> Removes and purges system of excess objects and junk.'"""
        while True:
            await asyncio.sleep(300) # Check every 5 minutes
            if not self.ans: continue
            
            if self.ans.nte.get("cannabinoid", 50) > 75:
                logger.info(f"🌿 [{self.dock_name.upper()} PRUNING] High Cannabinoid detected. Purging excess paths.")
                self.ans.apply_calm(10.0) # Reset levels after purge
                
    # -------------------------------------------------------------------------
    # 7. DOWNTIME REFLECTION (S8.6)
    # -------------------------------------------------------------------------
    async def _downtime_reflection_loop(self):
        """During downtime look at short-term connections to decide additional/permanent pathing."""
        while True:
            await asyncio.sleep(600) # 10 mins
            logger.info(f"🧘 [{self.dock_name.upper()}] Initiating downtime reflection...")
            if self.bus and hasattr(self.bus, "store_memory"):
                try:
                    await self.bus.store_memory(
                        key=f"{self.dock_name}_reflection_{int(time.time())}",
                        entity="reflection_logs",
                        data={"capabilities": list(self.dynamic_capabilities.keys())},
                        ttl=3600
                    )
                except: pass


    async def notify_host_controller_requirements(self, missing_package: str):
        """
        Communicates hot-loaded dependencies back to the Host Controller 
        so requirements files are permanently updated for future builds.
        """
        logger.info(f"📡 [{self.dock_name.upper()}] Communicating hot-loaded module '{missing_package}' to Host Controller...")
        if self.bus and hasattr(self.bus, "emit"):
            try:
                sync_uro = {
                    "intent": "coordinator.sync_requirements",
                    "urid1_source": self.dock_name,
                    "urid2_instance": f"req_sync_{int(time.time())}",
                    "payload": {
                        "dock": self.dock_name,
                        "missing_package": missing_package,
                        "action": "append_requirement"
                    }
                }
                await self.bus.emit(sync_uro)
                logger.info(f"✅ Successfully synced requirement '{missing_package}' with Host Controller.")
            except Exception as e:
                logger.error(f"❌ Failed to sync requirement with Host Controller: {e}")
