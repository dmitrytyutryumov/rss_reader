def to_bool(value: any) -> bool:
    return value in ("1", "True", "true", True, 1)
