"""
_solution_tests_

Tests for the solution module, ensure that various
lambda abstractions behave correctly using the printer
module, which has its own independent testing to
ensure correctness.
"""
from functools import partial
import unittest

import fizzbuzz.solution as lc
from fizzbuzz.printer import (
    unchurch,
    unchurch_list,
    church_print
)


class TestSolution(unittest.TestCase):

    def setUp(self):
        """
        Define a church printer partial that prints to string
        using the HEAD, TAIL, and IS_EMPTY abstractions if
        available or raises if they are not defined in the
        solution module.

        Define a similar function to
        unchurch lists of Church numerals into python lists
        of python integers.
        """
        def raise_thunk(*args, **kwargs):
            raise AttributeError(
                'Error: HEAD, TAIL, and/or IS_EMPTY not found in solution'
            )

        try:    
            self.cprint = partial(
                church_print,
                head=lc.HEAD,
                tail=lc.TAIL,
                isnil=lc.IS_EMPTY,
                to_str=True
            )
        except AttributeError:
            self.cprint = raise_thunk

        try:
            uc_list = partial(
                unchurch_list,
                head=lc.HEAD,
                tail=lc.TAIL,
                isnil=lc.IS_EMPTY
            )
            self.plist = lambda x: [unchurch(elem) for elem in uc_list(x)]
        except AttributeError:
            self.plist = raise_thunk
    
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

    def test_wisdom_tooth_predecessor(self):
        """
        Test the alternate "Wisdom Tooth" predecessor function.
        """
        self.assertEqual(unchurch(lc.WT_PRED(lc.FIVE)), 4)
        self.assertEqual(unchurch(lc.WT_PRED(lc.ONE)), 0)
        self.assertEqual(unchurch(lc.WT_PRED(lc.ZERO)), 0)

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
        self.assertEqual(self.plist(three_elem), [3, 2, 1])

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

    def test_unicode_chars(self):
        """
        Test that the unicode codepoints are correct
        """
        self.assertEqual(unchurch(lc.CH_NEWLINE), ord('\n'))
        self.assertEqual(unchurch(lc.CH_SPACE), ord(' '))
        self.assertEqual(unchurch(lc.CH_ZERO), ord('0'))
        self.assertEqual(unchurch(lc.CH_B), ord('B'))
        self.assertEqual(unchurch(lc.CH_F), ord('F'))
        self.assertEqual(unchurch(lc.CH_I), ord('I'))
        self.assertEqual(unchurch(lc.CH_U), ord('U'))
        self.assertEqual(unchurch(lc.CH_Z), ord('Z'))

    def test_integer_to_string(self):
        """
        Tests for the INT_TO_STR function.
        """
        forty_two = lc.ADD(lc.FORTY)(lc.TWO)
        self.assertEqual(self.cprint(lc.INT_TO_STR(forty_two)), '42')

        one_thirty_five = lc.ADD(lc.HUNDRED)(lc.ADD(lc.THIRTY)(lc.FIVE))
        self.assertEqual(self.cprint(lc.INT_TO_STR(one_thirty_five)), '135')
        
    def test_fizzbuzz_literals(self):
        """
        Test the FIZZ and BUZZ string literals
        """
        self.assertEqual(self.cprint(lc.FIZZ), 'FIZZ')
        self.assertEqual(self.cprint(lc.BUZZ), 'BUZZ')

    def test_try_fizz_and_buzz(self):
        """
        Test the TRY_FIZZ and TRY_BUZZ functions
        """
        self.assertEqual(self.cprint(lc.TRY_FIZZ(lc.THIRTY)), 'FIZZ')
        self.assertEqual(self.cprint(lc.TRY_BUZZ(lc.THIRTY)), 'BUZZ')

        self.assertEqual(self.cprint(lc.TRY_FIZZ(lc.TWENTY)), '')
        self.assertEqual(self.cprint(lc.TRY_BUZZ(lc.TWENTY)), 'BUZZ')

        NINE = lc.ADD(lc.FOUR)(lc.FIVE) 
        self.assertEqual(self.cprint(lc.TRY_FIZZ(NINE)), 'FIZZ')
        self.assertEqual(self.cprint(lc.TRY_BUZZ(NINE)), '')

        self.assertEqual(self.cprint(lc.TRY_FIZZ(lc.TWO)), '')
        self.assertEqual(self.cprint(lc.TRY_BUZZ(lc.TWO)), '')

    def test_list_reverse(self):
        """
        Test the REVERSE function
        """
        ZZIF = lc.REVERSE(lc.FIZZ)
        self.assertEqual(self.cprint(lc.REVERSE(lc.FIZZ)), 'ZZIF')

        Z = (lc.CONS)(lc.CH_Z)(lc.EMPTY)
        self.assertEqual(self.cprint(Z), 'Z')

        
        self.assertEqual(self.cprint(lc.EMPTY), '')

    def test_list_append(self):
        """
        Test the APPEND function
        """
        FB = (lc.APPEND)(lc.FIZZ)(lc.BUZZ)
        self.assertEqual(self.cprint(FB), 'FIZZBUZZ')

        F = (lc.APPEND)(lc.FIZZ)(lc.EMPTY)
        self.assertEqual(self.cprint(F), 'FIZZ')

        B = (lc.APPEND)(lc.EMPTY)(lc.BUZZ)
        self.assertEqual(self.cprint(B), 'BUZZ')

        nil = (lc.APPEND)(lc.EMPTY)(lc.EMPTY)
        self.assertEqual(self.cprint(nil), '')

    def test_fizzbuzz_single_number(self):
        """
        Test the FIZZBUZZ_NUM function
        """
        self.assertEqual(self.cprint(lc.FIZZBUZZ_NUM(lc.TEN)), '10 BUZZ\n')

        nine = lc.ADD(lc.FOUR)(lc.FIVE)
        self.assertEqual(self.cprint(lc.FIZZBUZZ_NUM(nine)), '9 FIZZ\n')

        self.assertEqual(
            self.cprint(lc.FIZZBUZZ_NUM(lc.THIRTY)),
            '30 FIZZBUZZ\n'
        )

        self.assertEqual(self.cprint(lc.FIZZBUZZ_NUM(lc.FOUR)), '4 \n')

    def test_fizzbuzz_upto(self):
        """
        Test the FIZZBUZZ_UPTO function
        """
        expected = '1 \n2 \n3 FIZZ\n4 \n5 BUZZ\n'
        self.assertEqual(self.cprint(lc.FIZZBUZZ_UPTO(lc.FIVE)), expected)
