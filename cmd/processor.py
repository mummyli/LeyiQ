import argparse
from core.rule_loader import load_rules_from_yaml
from core.rule_registry import RuleRegistry
from core.result_writer import ResultWriter
from core.executors.batch_executor import BatchExecutor
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", default="rules/sample_rules.yaml")
    parser.add_argument("--file", required=True, help="path to jsonl for dataset")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    rules = load_rules_from_yaml(args.rules)
    
    # register rules
    registry = RuleRegistry()
    for r in rules:
        registry.register(r)
        registry.publish(r.id)
    
    writer = ResultWriter()
    be = BatchExecutor(registry, writer)
    df = pd.read_json(args.file, lines=True)
    res = be.run_batch(args.dataset, df)
    print("Results:", res)

if __name__ == "__main__":
    main()