"""
Exportador HTML com template Jinja2 (simplificado).
"""
import json
from typing import List

from beaversec.core.base_module import ModuleResult


class HTMLExporter:
    def export(self, results: List[ModuleResult], output: str) -> None:
        items = []
        for r in results:
            data_str = json.dumps(r.data, indent=2)
            err_str = ", ".join(r.errors)
            items.append(
                f"""<div style="border:1px solid #ccc;margin:10px;padding:10px;">
                <h3>{r.module} - {r.target}</h3>
                <p>Status: {"Sucesso" if r.success else "Falha"}</p>
                <p>Duração: {r.duration:.2f}s</p>
                <pre>{data_str}</pre>
                {"<p style='color:red;'>Erros: " + err_str + "</p>" if r.errors else ""}
                </div>"""
            )
        full = f"""<!DOCTYPE html>
        <html><head><title>BeaverSec Report</title>
        <style>body{{font-family:sans-serif;}}</style>
        </head><body><h1>Relatório BeaverSec</h1>
        {"".join(items)}
        </body></html>"""
        with open(output, "w") as f:
            f.write(full)
