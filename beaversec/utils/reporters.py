"""Report generation utilities for BeaverSec."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from beaversec.core.exceptions import DataError
from beaversec.utils.audit_logger import AuditLogger


class Reporter:
    """
    Report generation for scan results.

    Supports multiple output formats: JSON, HTML, CSV.
    """

    def __init__(self, output_path: Optional[str] = None):
        """
        Initialize reporter.

        Args:
            output_path: Optional output file path
        """
        self.output_path = output_path
        self.logger = AuditLogger.get_logger("reporter")

    def generate_report(self, data: Dict[str, Any], format: str = "json") -> str:
        """
        Generate report in specified format.

        Args:
            data: Data to report
            format: Output format (json, html, csv)

        Returns:
            str: Formatted report

        Raises:
            DataError: If report generation fails
        """
        try:
            if format == "json":
                return self._generate_json(data)
            elif format == "html":
                return self._generate_html(data)
            elif format == "csv":
                return self._generate_csv(data)
            else:
                raise DataError(f"Unsupported format: {format}")
        except Exception as e:
            raise DataError(f"Failed to generate report: {e}")

    def save_report(self, data: Dict[str, Any], format: str = "json") -> str:
        """
        Generate and save report.

        Args:
            data: Data to report
            format: Output format

        Returns:
            str: Report content

        Raises:
            DataError: If saving fails
        """
        content = self.generate_report(data, format)

        if self.output_path:
            try:
                with open(self.output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.logger.info(f"Report saved to {self.output_path}")
            except Exception as e:
                raise DataError(f"Failed to save report: {e}")

        return content

    def _generate_json(self, data: Dict[str, Any]) -> str:
        """Generate JSON report."""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "results": data,
        }
        return json.dumps(report, indent=2, default=str)

    def _generate_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML report."""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>BeaverSec Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .header { background-color: #4CAF50; color: white; padding: 10px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>BeaverSec Scan Report</h1>
                <p>Generated: {timestamp}</p>
            </div>
            <div class="content">
                <h2>Results</h2>
                <pre>{data_json}</pre>
            </div>
        </body>
        </html>
        """
        return html_template.format(
            timestamp=datetime.utcnow().isoformat(),
            data_json=json.dumps(data, indent=2, default=str)
        )

    def _generate_csv(self, data: Dict[str, Any]) -> str:
        """Generate CSV report."""
        output = []

        # Try to flatten the data structure
        def flatten_data(obj, prefix=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_prefix = f"{prefix}.{key}" if prefix else key
                    yield from flatten_data(value, new_prefix)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_prefix = f"{prefix}[{i}]"
                    yield from flatten_data(item, new_prefix)
            else:
                yield (prefix, obj)

        # Extract headers and rows
        headers = []
        rows = {}

        for key, value in data.items():
            for flat_key, flat_value in flatten_data({key: value}):
                if flat_key not in headers:
                    headers.append(flat_key)
                rows[flat_key] = flat_value

        output.append(",".join(headers))
        output.append(",".join(str(rows.get(h, "")) for h in headers))

        return "\n".join(output)