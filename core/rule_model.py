from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class Rule:
    id: str
    name: str
    description: Optional[str] = None
    type: str = "required"
    dataset: Optional[str] = None
    field: Optional[str] = None
    left_dataset: Optional[str] = None
    right_dataset: Optional[str] = None
    on: Optional[Dict[str,str]] = None
    expression: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    severity: str = "ERROR"
    tags: List[str] = field(default_factory=list)
    owner: Optional[str] = None
    version: Optional[int] = 1
    tests: List[Dict[str,Any]] = field(default_factory=list)