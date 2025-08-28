import yaml
from jsonschema import validate, ValidationError
from core.rule_model import Rule
import logging

# Minimal JSON schema
RULE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "type": {"type": "string"},
        "dataset": {"type": "string"}
    },
    "required": ["id","name","type"]
}

def load_rules_from_yaml(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)
    rules = []
    for r in raw.get('rules', []):
        try:
            validate(instance=r, schema=RULE_SCHEMA)
        except ValidationError as e:
            logging.warning(f"Rule {r.get('id')} failed schema validation: {e}")

        
        rule = Rule(
            id=r.get('id'),
            name=r.get('name'),
            description=r.get('description'),
            type=r.get('type'),
            dataset=r.get('dataset'),
            field=r.get('field'),
            left_dataset=r.get('left_dataset'),
            right_dataset=r.get('right_dataset'),
            on=r.get('on'),
            expression=r.get('expression'),
            params=r.get('params', {}),
            severity=r.get('severity', 'ERROR'),
            tags=r.get('tags', []),
            owner=r.get('owner'),
            version=r.get('version', 1),
            tests=r.get('tests', [])
        )
        rules.append(rule)
    return rules