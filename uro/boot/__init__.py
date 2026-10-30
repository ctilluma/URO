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


# =====================================================================
# MODULE START : uro.boot
# ---------------------------------------------------------------------
# FILE         : uro/boot/__init__.py
# PURPOSE      : Boot process and system lifecycle exports (RFC 107-109).
# STANDARD     : URO-STD-0001 S12
# =====================================================================
"Boot process and system lifecycle (RFC 107-109)."
from uro.boot.boot_sequence import BOOT_STEPS, BootContext, BootRunner
from uro.boot.child_boot import ChildBoot
from uro.boot.self_check import SELF_CHECK_STEPS, self_check
__all__ = ["BOOT_STEPS", "BootContext", "BootRunner", "ChildBoot",
           "SELF_CHECK_STEPS", "self_check"]
# =====================================================================
# MODULE END   : uro.boot
# =====================================================================
