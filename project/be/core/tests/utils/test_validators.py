import datetime

from django.test import TestCase

from core.utils.validators import is_valid_hex_color, is_valid_date_range


class IsValidHexColorTest(TestCase):

    # --- valid ---

    def test_valid_uppercase(self):
        self.assertTrue(is_valid_hex_color('#FF0000'))

    def test_valid_lowercase(self):
        self.assertTrue(is_valid_hex_color('#ff0000'))

    def test_valid_mixed_case(self):
        self.assertTrue(is_valid_hex_color('#fF00Aa'))

    def test_valid_black(self):
        self.assertTrue(is_valid_hex_color('#000000'))

    def test_valid_white(self):
        self.assertTrue(is_valid_hex_color('#FFFFFF'))

    # --- invalid ---

    def test_missing_hash_is_invalid(self):
        self.assertFalse(is_valid_hex_color('FF0000'))

    def test_too_short_is_invalid(self):
        self.assertFalse(is_valid_hex_color('#FF00'))

    def test_too_long_is_invalid(self):
        self.assertFalse(is_valid_hex_color('#FF000000'))

    def test_non_hex_char_is_invalid(self):
        self.assertFalse(is_valid_hex_color('#GG0000'))

    def test_empty_string_is_invalid(self):
        self.assertFalse(is_valid_hex_color(''))

    def test_hash_only_is_invalid(self):
        self.assertFalse(is_valid_hex_color('#'))


class IsValidDateRangeTest(TestCase):

    # --- valid ---

    def test_end_after_start_is_valid(self):
        self.assertTrue(is_valid_date_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 1, 31),
        ))

    def test_equal_dates_is_valid(self):
        d = datetime.date(2024, 1, 1)
        self.assertTrue(is_valid_date_range(d, d))

    # --- invalid ---

    def test_end_before_start_is_invalid(self):
        self.assertFalse(is_valid_date_range(
            datetime.date(2024, 1, 31),
            datetime.date(2024, 1, 1),
        ))
