import re
from datetime import date

def is_valid_hex_color(color: str) -> bool:
    """Return True if `color` is a valid 6-digit hex color string (e.g. '#FF0000').

    The leading '#' is required; both upper and lower case hex digits are accepted.
    """
    # Anchors (^ and $) ensure the whole string must match — no partial matches
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', color))

def is_valid_date_range(start_date: date, end_date: date) -> bool:
    """Return True if `end_date` is on or after `start_date` (same day is valid)."""
    return end_date >= start_date