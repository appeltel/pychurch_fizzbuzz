"""
_solution_tests_

Tests for the solution module, ensure that various
lambda abstractions behave correctly using the printer
module, which has its own independent testing to
ensure correctness.
"""
import unittest

import fizzbuzz.solution as lc
from fizzbuzz.printer import (
    unchurch,
    unchurch_list,
    church_print
)


class TestSolution(unittest.TestCase):

    def test_basic_math(self):
        """
        Test some of the basic numerals, succ, and add functions.
        """
        self.assertEqual(unchurch(lc.zero), 0)
        self.assertEqual(unchurch(lc.three), 3)
        self.assertEqual(unchurch(lc.five), 5)
        self.assertEqual(unchurch(lc.hundred), 100)

        self.assertEqual(unchurch(lc.succ(lc.hundred)), 101)
        self.assertEqual(unchurch(lc.add(lc.hundred)(lc.hundred)), 200)
