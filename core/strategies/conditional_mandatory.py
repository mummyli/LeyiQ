from typing import Dict, Any, Optional, List
from core.strategies.rule_strategy import RuleStrategy

class ConditionalMandatoryStrategy(RuleStrategy):
    SUPPORTED_OPERATORS = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "in": lambda a, b: a in b if isinstance(b, (list, tuple, set)) else False,
        "not_in": lambda a, b: a not in b if isinstance(b, (list, tuple, set)) else False
    }

    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        self.conditions: List[Dict[str, Any]] = rule.params.get("conditions", [])
        self.logic: str = rule.params.get("logic", "AND").upper()

    def check(self, event: Dict) -> Optional[Dict]:
        results = []

        for cond in self.conditions:
            field = cond.get("field")
            operator = cond.get("operator")
            value = cond.get("value")

            actual_val = event.get(field)
            op_func = self.SUPPORTED_OPERATORS.get(operator)

            if op_func is None:
                return {
                    "message": f"Unsupported operator {operator}",
                    "field": field,
                    "value": actual_val
                }

            try:
                result = op_func(actual_val, value)
                results.append(result)
            except Exception as e:
                return {
                    "message": f"Condition check error on field {field}: {e}",
                    "field": field,
                    "value": actual_val
                }

        if self.logic == "AND":
            condition_met = all(results)
        elif self.logic == "OR":
            condition_met = any(results)
        else:
            return {
                "message": f"Unsupported logic {self.logic}",
                "field": self.rule.field,
                "value": event.get(self.rule.field)
            }

        target_val = event.get(self.rule.field)
        if condition_met and (target_val is None or str(target_val).strip() == ""):
            return {
                "message": f"{self.rule.field} is mandatory when conditions are met ({self.logic})",
                "field": self.rule.field,
                "value": target_val
            }

        return None
