from typing import Dict, Callable
from core.strategies.required import RequiredStrategy
from core.strategies.range_check import RangeStrategy
from core.strategies.data_type_check import DataTypeStrategy
from core.strategies.conditional_mandatory import ConditionalMandatoryStrategy
from core.strategies.date_range import DateTimeRangeStrategy
from core.strategies.str_length import StrLengthStrategy
from core.strategies.whitespaces import WhitespaceStrategy
from core.strategies.enum_value import EnumValueStrategy

_STRATEGIES: Dict[str, Callable] = {
    "required": RequiredStrategy,
    "range": RangeStrategy,
    "datatype": DataTypeStrategy,
    "conditional_mandatory": ConditionalMandatoryStrategy,
    "datetime_range": DateTimeRangeStrategy,
    "str_length": StrLengthStrategy,
    "whitespace": WhitespaceStrategy,
    "enum": EnumValueStrategy
}

def get_strategy(name: str):
    cls = _STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}")
    return cls