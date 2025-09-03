from typing import Dict, Any, Optional
from core.strategies.rule_strategy import RuleStrategy

class RangeStrategy(RuleStrategy):
    def __init__(self, rule, params: Dict[str,Any]=None):
        self.rule = rule
        self.min = rule.params.get("min")
        self.max = rule.params.get("max")

    def check(self, event: Dict) -> Optional[Dict]:
        val = event.get(self.rule.field)
        try:
            if val is None:
                return None
            v = float(val)
            if (self.min is not None and v < self.min) or (self.max is not None and v > self.max):
                return {"message": f"{self.rule.field} out of range", "field": self.rule.field, "value": val}
        except Exception:
            return {"message": f"{self.rule.field} not numeric", "field": self.rule.field, "value": val}
        return None