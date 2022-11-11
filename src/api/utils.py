from datetime import datetime, timezone, tzinfo
from time import mktime, struct_time
from typing import Optional

import pytz


def to_bool(value: any) -> bool:
    return value in ("1", "True", "true", True, 1)


def struct_time_to_datetime(_time: struct_time, tz: Optional[timezone] = pytz.UTC) -> datetime:
    return datetime.fromtimestamp(mktime(_time), tz=tz)
