from typing import Dict, Any, Optional
from core.strategies.rule_strategy import RuleStrategy
from datetime import datetime

class DateTimeRangeStrategy(RuleStrategy):
    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        self.datatype = rule.params.get("datatype", "datetime")  # date / time / datetime
        self.date_format = rule.params.get("format")
        if not self.date_format:
            raise ValueError(f"Rule {self.rule.id} missing 'format' in params")

        self.min_raw = rule.params.get("min")
        self.max_raw = rule.params.get("max")

        self.min_val = self._parse_boundary(self.min_raw)
        self.max_val = self._parse_boundary(self.max_raw)

    def _parse_boundary(self, raw_val: Optional[str]):
        if not raw_val:
            return None
        try:
            dt = datetime.strptime(raw_val, self.date_format)
            if self.datatype == "date":
                return dt.date()
            elif self.datatype == "time":
                return dt.time()
            return dt
        except Exception as e:
            raise ValueError(f"Invalid boundary value '{raw_val}' for rule {self.rule.id}: {e}")

    def check(self, event: Dict) -> Optional[Dict]:
        val = event.get(self.rule.field)
        if val is None:
            return None

        try:
            parsed = datetime.strptime(str(val), self.date_format)
            if self.datatype == "date":
                parsed = parsed.date()
            elif self.datatype == "time":
                parsed = parsed.time()
        except Exception:
            return {
                "message": f"{self.rule.field} not match format {self.date_format} as {self.datatype}",
                "field": self.rule.field,
                "value": val
            }

        if (self.min_val and parsed < self.min_val) or (self.max_val and parsed > self.max_val):
            return {
                "message": f"{self.rule.field} out of {self.datatype} range",
                "field": self.rule.field,
                "value": val
            }

        return None
