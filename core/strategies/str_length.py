from core.strategies.rule_strategy import RuleStrategy
from typing import Dict, Any, Optional


class StrLengthStrategy(RuleStrategy):
    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        self.min_len = rule.params.get("min")
        self.max_len = rule.params.get("max")
        
    def check(self, event: Dict) -> Optional[Dict]:
        val = event.get(self.rule.field)
        if val is None:
            return None
        
        val_len = len(val)
        
        if(val_len < self.min_len or val_len > self.max_len):
            return {
                "message": f"{self.rule.field} length is {val_len}, and out of range[{self.min_len}, {self.max_len}]",
                "field": self.rule.field,
                "value": val
            }
    
        return None