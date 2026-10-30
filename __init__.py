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




# --- Pydantic V2 Positional Arg Compatibility Patch ---
# Docks generated against V1 sometimes instantiate Models positionally: Model(a, b)
# Pydantic V2 forbids this. This patch maps positional args to fields in declaration order.
try:
    from pydantic import BaseModel
    _original_pydantic_init = BaseModel.__init__
    def _positional_pydantic_init(self, *args, **kwargs):
        if args:
            fields = list(self.model_fields.keys())
            for i, val in enumerate(args):
                if i < len(fields):
                    kwargs[fields[i]] = val
        _original_pydantic_init(self, **kwargs)
    BaseModel.__init__ = _positional_pydantic_init
except ImportError:
    pass

import os as _os
_sub_pkg = _os.path.join(_os.path.dirname(__file__), 'uro')
if _os.path.isdir(_sub_pkg) and _sub_pkg not in __path__:
    __path__.append(_sub_pkg)
