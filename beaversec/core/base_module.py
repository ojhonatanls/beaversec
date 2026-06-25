"""
Base module definitions for BeaverSec modules.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ModuleResult(BaseModel):
    """Resultado padrão retornado por um módulo."""
    module: str = Field(..., description="Nome do módulo")
    target: str = Field(..., description="Alvo escaneado")
    success: bool = Field(default=True, description="Indica se a execução foi bem-sucedida")
    data: Dict[str, Any] = Field(default_factory=dict, description="Dados do resultado")
    error: Optional[str] = Field(default=None, description="Mensagem de erro se houver")


class BaseModule(ABC):
    """Classe base para todos os módulos do BeaverSec."""
    
    name: str = ""
    description: str = ""
    
    @abstractmethod
    async def run(self, **kwargs) -> ModuleResult:
        """Executa o módulo com os argumentos fornecidos."""
        pass