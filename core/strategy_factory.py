from typing import Dict, Callable
from core.strategies.required import RequiredStrategy
from core.strategies.range_check import RangeStrategy

_STRATEGIES: Dict[str, Callable] = {
    "required": RequiredStrategy,
    "range": RangeStrategy,
}

def get_strategy(name: str):
    cls = _STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}")
    return cls