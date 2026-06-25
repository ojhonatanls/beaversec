"""
Exportador JSON.
"""
import json
from typing import List

from beaversec.core.base_module import ModuleResult


class JSONExporter:
    def export(self, results: List[ModuleResult], output: str) -> None:
        data = [r.model_dump() for r in results]
        with open(output, "w") as f:
            json.dump(data, f, indent=2)
