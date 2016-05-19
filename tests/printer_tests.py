"""
_printer_tests_

Tests for the printer module, ensure that it works
correctly separate of the proposed solution and for
differing Church list implementations
"""
import unittest
import unittest.mock
from fizzbuzz.printer import (
    unchurch,
    unchurch_list
)


class TestPrinter(unittest.TestCase):

    def test_unchurch(self):
        zero = lambda f: lambda x: x
        three = lambda f: lambda x: f(f(f(x)))
        self.assertEqual(unchurch(zero), 0)
        self.assertEqual(unchurch(three), 3)
