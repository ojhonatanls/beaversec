"""
Logging utilities for BeaverSec.
Provides structured JSON logging with correlation IDs.
"""

import json
import logging
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


# Contexto global para armazenar o correlation ID da execução
_correlation_id: Optional[str] = None


def set_correlation_id(cid: Optional[str] = None) -> str:
    """Define o correlation ID para a execução atual."""
    global _correlation_id
    if cid is None:
        cid = str(uuid.uuid4())
    _correlation_id = cid
    return cid


def get_correlation_id() -> str:
    """Retorna o correlation ID atual ou gera um novo."""
    global _correlation_id
    if _correlation_id is None:
        _correlation_id = str(uuid.uuid4())
    return _correlation_id


class JSONFormatter(logging.Formatter):
    """Formatter que produz logs em JSON."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "correlation_id": get_correlation_id(),
            "module": record.module,
            "function": record.funcName,
            "message": record.getMessage(),
        }
        
        # Adiciona exception info se houver
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Adiciona atributos extras (ex: target, port, etc.)
        if hasattr(record, "extra"):
            log_entry.update(record.extra)
        
        return json.dumps(log_entry)


def setup_logging(
    level: str = "INFO",
    json_output: bool = True,
    log_file: Optional[str] = None
) -> None:
    """
    Configura o sistema de logging.
    
    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_output: Se True, logs em JSON. Se False, logs em texto simples.
        log_file: Caminho para arquivo de log (opcional).
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    if json_output:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    # Suprime logs de bibliotecas externas (ex: aiohttp)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado com contexto."""
    return logging.getLogger(name)