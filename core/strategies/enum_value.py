from typing import Dict, Any, Optional, Iterable
from core.strategies.rule_strategy import RuleStrategy

class EnumValueStrategy(RuleStrategy):
    """
    Validate that event[self.rule.field] belongs to an allowed set (allowed_values).

    Supported configuration in rule.params:
      - allowed_values: list/tuple/set, required, the set of allowed values
      - case_sensitive: bool, whether comparison is case-sensitive (default True)
      - allow_null: bool, whether None/empty is allowed (default True)
      - trim: bool, whether to strip whitespace from string values before checking (default False)
      - multi_valued: bool, whether the field can contain multiple values (default False)
      - delimiter: str, delimiter for multi-valued strings (default ',')
    
    Returns a dict {"message","field","value"} on validation failure, otherwise None.
    """

    def __init__(self, rule, params: Dict[str, Any] = None):
        self.rule = rule
        self.params = (rule.params or {}).copy()

        allowed = self.params.get("allowed_values")
        if allowed is None:
            raise ValueError(f"Rule {getattr(rule, 'id', '<no-id>')} missing required param 'allowed_values'")

        if not isinstance(allowed, (list, tuple, set, Iterable)):
            raise ValueError("'allowed_values' must be an iterable (list/tuple/set)")

        # configuration flags
        self.case_sensitive: bool = bool(self.params.get("case_sensitive", True))
        self.allow_null: bool = bool(self.params.get("allow_null", True))
        self.trim: bool = bool(self.params.get("trim", False))
        self.multi_valued: bool = bool(self.params.get("multi_valued", False))
        self.delimiter: str = str(self.params.get("delimiter", ","))

        # normalize allowed values into a set of strings for comparison
        if self.case_sensitive:
            self.allowed_set = {str(x) for x in allowed}
        else:
            self.allowed_set = {str(x).lower() for x in allowed}

    def _normalize(self, v: Any) -> str:
        """Convert value to string, optionally trim, and apply case normalization."""
        s = str(v)
        if self.trim:
            s = s.strip()
        return s if self.case_sensitive else s.lower()

    def check(self, event: Dict) -> Optional[Dict]:
        """Perform the enum membership check."""
        val = event.get(self.rule.field)

        # 1) Handle null/empty values
        if val is None or (isinstance(val, str) and val == ""):
            if self.allow_null:
                return None
            else:
                return {
                    "message": f"{self.rule.field} is null/empty but nulls are not allowed",
                    "field": self.rule.field,
                    "value": val
                }

        # 2) Multi-valued field: accept list/tuple or a delimited string
        if self.multi_valued:
            items = []
            if isinstance(val, (list, tuple)):
                items = list(val)
            else:
                # split the string by delimiter into items
                items = [x for x in str(val).split(self.delimiter)]

            for item in items:
                norm = self._normalize(item)
                # skip empty sub-items (adjust behavior here if you want to treat them as invalid)
                if norm == "":
                    continue
                if norm not in self.allowed_set:
                    return {
                        "message": f"{self.rule.field} contains value not in allowed set: '{item}'",
                        "field": self.rule.field,
                        "value": val
                    }
            return None

        # 3) Single-valued field: direct comparison
        norm_val = self._normalize(val)
        if norm_val not in self.allowed_set:
            return {
                "message": f"{self.rule.field} value not in allowed set",
                "field": self.rule.field,
                "value": val
            }

        return None
