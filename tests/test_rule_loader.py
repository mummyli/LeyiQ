import tempfile
import textwrap
import logging
import pytest

from core.rule_loader import load_rules_from_yaml
from core.rule_model import Rule


def write_temp_yaml(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode="w", encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_load_valid_rules():
    yaml_content = textwrap.dedent("""
    rules:
      - id: "r1"
        name: "Test rule"
        type: "consistency"
        dataset: "table1"
        description: "sample"
    """)
    path = write_temp_yaml(yaml_content)

    rules = load_rules_from_yaml(path)

    assert len(rules) == 1
    assert isinstance(rules[0], Rule)
    assert rules[0].id == "r1"
    assert rules[0].name == "Test rule"
    assert rules[0].dataset == "table1"


def test_invalid_rule_triggers_warning(caplog):
    yaml_content = textwrap.dedent("""
    rules:
      - id: "r2"
        type: "missing_name"
    """)
    path = write_temp_yaml(yaml_content)

    with caplog.at_level(logging.WARNING):
        rules = load_rules_from_yaml(path)


    assert len(rules) == 1
    assert rules[0].id == "r2"
    assert any("failed schema validation" in m for m in caplog.messages)


def test_empty_rules_returns_empty_list():
    yaml_content = "rules: []"
    path = write_temp_yaml(yaml_content)

    rules = load_rules_from_yaml(path)
    assert rules == []


def test_missing_optional_fields():
    yaml_content = textwrap.dedent("""
    rules:
      - id: "r3"
        name: "no extras"
        type: "basic"
    """)
    path = write_temp_yaml(yaml_content)

    rules = load_rules_from_yaml(path)
    r = rules[0]

    assert r.description is None
    assert r.params == {}
    assert r.tags == []
    assert r.severity == "ERROR"
    assert r.version == 1
