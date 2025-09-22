import re
from typing import Dict, Any, Optional
from core.strategies.rule_strategy import RuleStrategy

class RegexStrategy(RuleStrategy):
    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        # regex can be a single string or a list of patterns
        self.pattern = rule.params.get("pattern")

        # pre-compile regex for performance
        self.compiled = None
        try:
            self.compiled = re.compile(self.pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{self.pattern}' in rule {rule.id}: {e}")

    def check(self, event: Dict) -> Optional[Dict]:
        val = event.get(self.rule.field)
        if val is None:
            return None

        val_str = str(val)
        if self.compiled:
            if self.compiled.fullmatch(val_str):
                return None  

        return {
            "message": f"{self.rule.field} does not match required format",
            "field": self.rule.field,
            "value": val
        }
