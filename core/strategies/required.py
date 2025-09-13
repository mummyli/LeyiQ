from typing import Dict, Any, Optional
from core.strategies.rule_strategy import RuleStrategy

class RequiredStrategy(RuleStrategy):
    def __init__(self, rule, params: Dict[str,Any]=None):
        self.rule = rule

    def check(self, event: Dict) -> Optional[Dict]:
        # return failure record or None
        val = event.get(self.rule.field)
        if val is None or (isinstance(val, str) and val.strip()==""):
            return {"message": f"{self.rule.field} is missing", "field": self.rule.field, "value": val}
        return None