"""Audit logging system for BeaverSec."""

import json
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional


class AuditLogger:
    """
    Secure audit logging system with structured logging.

    Attributes:
        log_dir: Directory for log files
        logger: Python logging instance
    """

    _instance = None
    _loggers = {}

    def __new__(cls):
        """Singleton pattern for AuditLogger."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize logging configuration."""
        self.log_dir = Path.home() / ".beaversec" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        self._configure_root_logger()

    def _configure_root_logger(self):
        """Configure the root logger with handlers."""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # File handler for audit logs
        audit_log_file = self.log_dir / "audit.log"
        file_handler = RotatingFileHandler(
            audit_log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        # JSON structured log handler
        json_log_file = self.log_dir / "audit.json"
        json_handler = RotatingFileHandler(
            json_log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        json_handler.setLevel(logging.INFO)
        json_handler.setFormatter(
            JsonFormatter()
        )
        root_logger.addHandler(json_handler)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a named logger.

        Args:
            name: Logger name

        Returns:
            logging.Logger: Configured logger instance
        """
        if name not in cls._loggers:
            # Ensure root logger is configured
            cls()

            # Create child logger
            logger = logging.getLogger(f"beaversec.{name}")
            logger.setLevel(logging.INFO)
            cls._loggers[name] = logger

        return cls._loggers[name]

    @staticmethod
    def audit_event(event_type: str, user: str, details: Dict[str, Any]) -> None:
        """
        Log an audit event with structured data.

        Args:
            event_type: Type of audit event
            user: User performing the action
            details: Event details
        """
        logger = AuditLogger.get_logger("audit")

        audit_data = {
            "event_type": event_type,
            "user": user,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        }

        logger.info(f"AUDIT: {event_type}", extra={"audit_data": audit_data})


class JsonFormatter(logging.Formatter):
    """Custom formatter for JSON-structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            str: JSON formatted log entry
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add audit data if present
        if hasattr(record, "audit_data"):
            log_data["audit_data"] = record.audit_data

        return json.dumps(log_data)