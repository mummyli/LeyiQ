from typing import List, Dict
from core.rule_model import Rule
import threading
import time

class RuleRegistry:
    def __init__(self):
        self._lock = threading.RLock()
        self._rules: Dict[str, Rule] = {}
        self._published: Dict[str, Rule] = {}

    def register(self, rule: Rule):
        with self._lock:
            self._rules[rule.id] = rule

    def publish(self, rule_id: str):
        with self._lock:
            if rule_id in self._rules:
                self._published[rule_id] = self._rules[rule_id]

    def get_all(self) -> List[Rule]:
        with self._lock:
            return list(self._published.values())

    def get_for_dataset(self, dataset: str):
        with self._lock:
            return [r for r in self._published.values() if r.dataset == dataset or r.left_dataset == dataset or r.right_dataset == dataset]