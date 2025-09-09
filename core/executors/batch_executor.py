from typing import Dict, Any
import pandas as pd
from core.strategy_factory import get_strategy

class BatchExecutor:
    def __init__(self, registry, writer, spark_session=None):
        self.registry = registry
        self.writer = writer
        self.spark = spark_session

    def run_batch(self, dataset: str, df: pd.DataFrame):
        # find rules for dataset
        rules = self.registry.get_for_dataset(dataset)
        results = []
        for rule in rules:
            Strat = get_strategy(rule.type)
            strat = Strat(rule, rule.params)
            # apply per-row (simplified)
            failures = []
            for _, row in df.iterrows():
                fr = strat.check_row(row.to_dict())
                if fr:
                    failures.append({"rule_id": rule.id, "failure": fr, "row": row.to_dict()})
            # write samples
            for f in failures[: rule.params.get("sample_limit", 10)]:
                self.writer.write_failure(rule, f["row"], f["failure"])
            results.append({"rule_id": rule.id, "failures": len(failures), "checked": len(df)})
        return results