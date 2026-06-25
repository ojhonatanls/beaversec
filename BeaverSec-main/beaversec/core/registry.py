"""
Module argument registry for BeaverSec.

Centralizes module parameter definitions for consistent CLI parsing.
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type


@dataclass
class ArgDef:
    """Definition of a module argument."""
    name: str
    type: Type
    required: bool = False
    default: Optional[Any] = None
    help: Optional[str] = None
    choices: Optional[List[Any]] = None


class ModuleArgRegistry:
    """Registry for module arguments."""
    
    def __init__(self):
        self._args: Dict[str, List[ArgDef]] = {}
    
    def register(self, module_name: str, arg_def: ArgDef) -> None:
        """Register an argument for a module."""
        if module_name not in self._args:
            self._args[module_name] = []
        self._args[module_name].append(arg_def)
    
    def get_args(self, module_name: str) -> List[ArgDef]:
        """Get all arguments for a module."""
        return self._args.get(module_name, [])
    
    def get_all(self) -> Dict[str, List[ArgDef]]:
        """Get all registered arguments."""
        return self._args.copy()


# Global registry instance
MODULE_ARGS = ModuleArgRegistry()