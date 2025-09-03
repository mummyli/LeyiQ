from abc import ABC, abstractmethod
from typing import Dict, Any
from core.rule_model import Rule


class RuleStrategy(ABC):
    def __init__(self, rule, params: Dict[str,Any]=None):
        self.rule = rule
    
    @abstractmethod
    def check(self, event: Dict, rule: Rule) -> str:
        """check the rule, return error message, and return None if passed"""
        ...