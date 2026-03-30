# test_utils.py - Existing tests for utils.py

import unittest
from utils import validate_email, format_currency, truncate_string


class TestValidateEmail(unittest.TestCase):

    def test_valid_email(self):
        result = validate_email("user@example.com")
        self.assertTrue(result)

    def test_invalid_email_no_at(self):
        result = validate_email("userexample.com")
        self.assertFalse(result)

    def test_invalid_email_no_domain(self):
        result = validate_email("user@")
        self.assertFalse(result)

    def test_empty_string(self):
        result = validate_email("")
        self.assertFalse(result)


class TestFormatCurrency(unittest.TestCase):

    def test_positive_amount(self):
        result = format_currency(1234.56)
        self.assertEqual(result, "$1,234.56")

    def test_zero(self):
        result = format_currency(0)
        self.assertEqual(result, "$0.00")

    def test_none_amount(self):
        result = format_currency(None)
        self.assertEqual(result, "$0.00")


class TestTruncateString(unittest.TestCase):

    def test_short_string(self):
        result = truncate_string("hello", 100)
        self.assertEqual(result, "hello")

    def test_long_string(self):
        result = truncate_string("a" * 200, 100)
        self.assertEqual(len(result), 100)
        self.assertTrue(result.endswith("..."))

    def test_empty_string(self):
        result = truncate_string("")
        self.assertEqual(result, "")

    def test_exact_length(self):
        result = truncate_string("hello", 5)
        self.assertEqual(result, "hello")


if __name__ == "__main__":
    unittest.main()
