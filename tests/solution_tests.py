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
        Test some of the basic numerals, SUCC, ADD, and MULT functions.
        """
        self.assertEqual(unchurch(lc.ZERO), 0)
        self.assertEqual(unchurch(lc.THREE), 3)
        self.assertEqual(unchurch(lc.FIVE), 5)
        self.assertEqual(unchurch(lc.HUNDRED), 100)

        self.assertEqual(unchurch(lc.SUCC(lc.HUNDRED)), 101)
        self.assertEqual(unchurch(lc.ADD(lc.HUNDRED)(lc.HUNDRED)), 200)

        self.assertEqual(unchurch(lc.MULT(lc.TEN)(lc.TEN)), 100)
        self.assertEqual(unchurch(lc.MULT(lc.ONE)(lc.TEN)), 10)
        self.assertEqual(unchurch(lc.MULT(lc.TEN)(lc.ZERO)), 0)

    def test_predecessor(self):
        """
        Test the PRED predecessor function.
        """
        self.assertEqual(unchurch(lc.PRED(lc.FIVE)), 4)
        self.assertEqual(unchurch(lc.PRED(lc.HUNDRED)), 99)
        self.assertEqual(unchurch(lc.PRED(lc.ONE)), 0)
        self.assertEqual(unchurch(lc.PRED(lc.ZERO)), 0)

    def test_subtraction(self):
        """
        Test the MINUS subtraction function.
        """
        self.assertEqual(unchurch(lc.MINUS(lc.TEN)(lc.FIVE)), 5)
        self.assertEqual(unchurch(lc.MINUS(lc.THIRTY)(lc.FOUR)), 26)
        self.assertEqual(unchurch(lc.MINUS(lc.THIRTY)(lc.ZERO)), 30)
        self.assertEqual(unchurch(lc.MINUS(lc.FIVE)(lc.FIVE)), 0)
        self.assertEqual(unchurch(lc.MINUS(lc.FOUR)(lc.FIVE)), 0)
        self.assertEqual(unchurch(lc.MINUS(lc.ZERO)(lc.ZERO)), 0)

    def test_less_than_or_equal(self):
        """
        Test the LEQ less-than-or-equal predicate.
        """
        self.assertTrue(lc.LEQ(lc.FOUR)(lc.FIVE)(True)(False))
        self.assertTrue(lc.LEQ(lc.ZERO)(lc.FIVE)(True)(False))
        self.assertTrue(lc.LEQ(lc.ZERO)(lc.ZERO)(True)(False))
        self.assertTrue(lc.LEQ(lc.FIVE)(lc.FIVE)(True)(False))
        self.assertFalse(lc.LEQ(lc.TWENTY)(lc.TEN)(True)(False))
        self.assertFalse(lc.LEQ(lc.TEN)(lc.ZERO)(True)(False))

    def test_booleans_and_pairs(self):
        """
        Test for TRUE, FALSE, PAIR, FIRST, SECOND
        """
        self.assertTrue(lc.TRUE(True)(False))
        self.assertFalse(lc.FALSE(True)(False))

        pair = lc.PAIR(lc.ONE)(lc.TWO)
        self.assertEqual(unchurch(lc.FIRST(pair)), 1)
        self.assertEqual(unchurch(lc.SECOND(pair)), 2)

    def test_is_zero(self):
        """
        Test the IS_ZERO predicate
        """
        self.assertTrue(lc.IS_ZERO(lc.ZERO)(True)(False))
        self.assertFalse(lc.IS_ZERO(lc.ONE)(True)(False))
        self.assertFalse(lc.IS_ZERO(lc.HUNDRED)(True)(False))

    def test_list_construction(self):
        """
        Test CONS, EMPTY, IS_EMPTY, HEAD, TAIL
        """
        self.assertTrue(lc.IS_EMPTY(lc.EMPTY)(True)(False))

        one_elem = lc.CONS(lc.ONE)(lc.EMPTY)
        self.assertFalse(lc.IS_EMPTY(one_elem)(True)(False))
        self.assertTrue(lc.IS_EMPTY(lc.TAIL(one_elem))(True)(False))
        self.assertEqual(unchurch(lc.HEAD(one_elem)), 1)

        two_elem = lc.CONS(lc.TWO)(one_elem)
        three_elem = lc.CONS(lc.THREE)(two_elem)
        pylist = unchurch_list(
            three_elem,
            head=lc.HEAD,
            tail=lc.TAIL,
            isnil=lc.IS_EMPTY
        )
        self.assertEqual(
            [unchurch(elem) for elem in pylist],
            [3, 2, 1]
        )

    def test_z_combinator(self):
        """
        Test the Z-combinator against a python factorial
        stepper function.
        """
        def F(next_step):
            def step(n):
                if n == 0:
                    return 1
                return n * next_step(n - 1)
            return step

        # ensure that the stepper function F before applying the
        # Z-combinator
        self.assertEqual((F(F(F(F(F(F(lambda x: x)))))))(4), 24)
        self.assertEqual((F(F(F(F(F(F(lambda x: x)))))))(1), 1)

        factorial = lc.Z(F)

        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(0), 1)

    def test_z_combinator_lambda_predicate(self):
        """
        Test the Z-combinator against a factorial stepper
        function built out of a predicate and abstractions
        from the solution implementation so far.

        Note that the recursive clause of the predicate
        requires a "thunk" - lambda z: (CLAUSE)(z) in order
        to prevent infinite recursion due to eager evaluation
        in python.
        """
        F = (
            lambda f: lambda n: 
            lc.IS_ZERO(n)(lc.ONE)(lambda z: lc.MULT(n)(f(lc.PRED(n)))(z))
        )

        # ensure that the stepper function F before applying the
        # Z-combinator
        self.assertEqual(
            unchurch((F(F(F(F(F(F(lambda x: x)))))))(lc.FOUR)),
            24
        )
        self.assertEqual(
            unchurch((F(F(F(F(F(F(lambda x: x)))))))(lc.ONE)),
            1
        )

        factorial = lc.Z(F)

        self.assertEqual(unchurch(factorial(lc.FIVE)), 120)
        self.assertEqual(unchurch(factorial(lc.THREE)), 6)
        self.assertEqual(unchurch(factorial(lc.ONE)), 1)
        self.assertEqual(unchurch(factorial(lc.ZERO)), 1)

    def test_modular_arithmetic(self):
        """
        Tests for the MOD function.
        """
        self.assertEqual(unchurch(lc.MOD(lc.FIVE)(lc.THREE)), 2)
        self.assertEqual(unchurch(lc.MOD(lc.TWO)(lc.TWO)), 0)
        self.assertEqual(unchurch(lc.MOD(lc.THIRTY)(lc.FOUR)), 2)
        self.assertEqual(unchurch(lc.MOD(lc.ONE)(lc.FOUR)), 1)
        self.assertEqual(unchurch(lc.MOD(lc.TWENTY)(lc.TEN)), 0)
        self.assertEqual(unchurch(lc.MOD(lc.FOUR)(lc.FIVE)), 4)

    def test_division(self):
        """
        Tests for the DIV function.
        """
        self.assertEqual(unchurch(lc.DIV(lc.FIVE)(lc.ONE)), 5)
        self.assertEqual(unchurch(lc.DIV(lc.FIVE)(lc.TWO)), 2)
        self.assertEqual(unchurch(lc.DIV(lc.HUNDRED)(lc.FOUR)), 25)
        self.assertEqual(unchurch(lc.DIV(lc.HUNDRED)(lc.ONE)), 100)
