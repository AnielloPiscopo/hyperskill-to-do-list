import re
from datetime import date

def is_valid_hex_color(color: str) -> bool:
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', color))

def is_valid_date_range(start_date: date, end_date: date) -> bool:
    return end_date >= start_date