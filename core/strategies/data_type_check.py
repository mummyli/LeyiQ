from typing import Dict, Any, Optional
from core.strategies.rule_strategy import RuleStrategy
from datetime import datetime

class DataTypeStrategy(RuleStrategy):
    DEFAULT_FORMATS = {
        "date": "%Y-%m-%d",
        "time": "%H:%M:%S",
        "datetime": "%Y-%m-%d %H:%M:%S"
    }

    TYPE_MAP = {
        "int": int,
        "integer": int,
        "float": float,
        "double": float,
        "str": str,
        "string": str,
        "bool": lambda v: str(v).lower() in ["true", "false", "1", "0"],
        "number": "number",
        "date": "date",
        "time": "time",
        "datetime": "datetime"
    }

    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        self.expected_type = rule.params.get("expected_type")
        self.custom_format = rule.params.get("format")

    def check(self, event: Dict) -> Optional[Dict]:
        val = event.get(self.rule.field)
        if val is None:
            return None

        expected_type = self.TYPE_MAP.get(self.expected_type.lower())
        if expected_type is None:
            return {
                "message": f"Unknown expected type {self.expected_type}",
                "field": self.rule.field,
                "value": val
            }

        try:
            if expected_type == "number":
                try:
                    int(val)
                except Exception:
                    float(val)
            elif expected_type in ["date", "time", "datetime"]:
                fmt = self.custom_format or self.DEFAULT_FORMATS[expected_type]
                datetime.strptime(str(val), fmt)
            elif callable(expected_type):
                if not expected_type(val):
                    raise ValueError("Not a valid bool value")
            else:
                expected_type(val)
        except Exception:
            return {
                "message": f"{self.rule.field} not of type {self.expected_type} (expected format: {self.custom_format or self.DEFAULT_FORMATS.get(expected_type)})",
                "field": self.rule.field,
                "value": val
            }

        return None
