import os, json, time
from typing import Dict, Any

class ResultWriter:
    def __init__(self, out_dir: str = "./tmp/leyiq_results"):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def write_failure(self, rule, row: Dict[str,Any], failure: Dict[str,Any]):
        ts = int(time.time())
        fname = f"{rule.id}_{ts}.jsonl"
        path = os.path.join(self.out_dir, fname)
        record = {
            "rule_id": rule.id,
            "dataset": rule.dataset,
            "severity": rule.severity,
            "ingest_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "failure": failure,
            "row": row
        }
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path