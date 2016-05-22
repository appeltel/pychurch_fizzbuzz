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
        self.assertEqual(unchurch(lc.ZERO), 0)
        self.assertEqual(unchurch(lc.THREE), 3)
        self.assertEqual(unchurch(lc.FIVE), 5)
        self.assertEqual(unchurch(lc.HUNDRED), 100)

        self.assertEqual(unchurch(lc.SUCC(lc.HUNDRED)), 101)
        self.assertEqual(unchurch(lc.ADD(lc.HUNDRED)(lc.HUNDRED)), 200)
