"""
Exportador CSV.
"""
import csv
from typing import List

from beaversec.core.base_module import ModuleResult


class CSVExporter:
    def export(self, results: List[ModuleResult], output: str) -> None:
        with open(output, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["module", "target", "success", "duration", "data", "errors"])
            for r in results:
                writer.writerow(
                    [
                        r.module,
                        r.target,
                        r.success,
                        f"{r.duration:.2f}",
                        str(r.data),
                        ";".join(r.errors),
                    ]
                )
