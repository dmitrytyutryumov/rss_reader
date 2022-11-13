import datetime

import pytest
import pytz
from utils import struct_time_to_datetime, to_bool, to_int


@pytest.mark.parametrize(
    "value, expect_result",
    (
        ("1", True),
        ("True", True),
        ("true", True),
        (True, True),
        (1, True),
        ("0", False),
        ("false", False),
        ("False", False),
    ),
)
def test_to_bool(value, expect_result):
    assert to_bool(value) == expect_result


def test_struct_time_to_datetime():
    value = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=pytz.UTC)
    assert struct_time_to_datetime(value.timetuple()) == value


@pytest.mark.parametrize(
    "value, expect_result",
    (
        ("1", 1),
        ("True", None),
    ),
)
def test_to_int(value, expect_result):
    assert to_int(value) == expect_result
