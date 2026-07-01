import re

__all__ = ['is_valid_hex_color', 'is_valid_date_range']

def is_valid_hex_color(color: str) -> bool:
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', color))

def is_valid_date_range(start_date, end_date) -> bool:
    return start_date and end_date and end_date >= start_date