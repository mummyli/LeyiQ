from typing import Dict, Any, Optional
from core.strategies.rule_strategy import RuleStrategy

class WhitespaceStrategy(RuleStrategy):
    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        self.params = params or {}

    def check(self, event: Dict) -> Optional[Dict]:
        val = event.get(self.rule.field)
        if val is None:
            return None

        try:
            if not isinstance(val, str):
                return {
                    "message": f"{self.rule.field} is not a string",
                    "field": self.rule.field,
                    "value": val
                }

            if val != val.strip():
                return {
                    "message": f"{self.rule.field} contains leading or trailing spaces",
                    "field": self.rule.field,
                    "value": val
                }

        except Exception as e:
            return {
                "message": f"Error checking {self.rule.field}: {str(e)}",
                "field": self.rule.field,
                "value": val
            }

        return None
