"""
_printer_tests_

Tests for the printer module, ensure that it works
correctly separate of the proposed solution and for
differing Church list implementations
"""
import unittest
from unittest.mock import patch
from collections import namedtuple
from io import StringIO

from fizzbuzz.printer import (
    unchurch,
    unchurch_list,
    church_print
)

ListImpl = namedtuple('ListImpl', ['cons', 'head', 'tail', 'nil', 'isnil'])


class TestPrinter(unittest.TestCase):

    def setUp(self):
        """
        Define some church numerals and math for general use

        Patch out sys.stdout for assertions
        """
        self.zero = lambda f: lambda x: x
        self.one = lambda f: lambda x: f(x)
        self.two = lambda f: lambda x: f(f(x))
        self.three = lambda f: lambda x: f(f(f(x)))
        self.add = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))

        self.four = self.add(self.one)(self.three)
        self.eight = self.add(self.four)(self.four)
        self.ten = self.add(self.eight)(self.two)
        self.twenty = self.add(self.ten)(self.ten)
        self.thirty = self.add(self.twenty)(self.ten)
        self.fourty = self.add(self.thirty)(self.ten)

        self.ch_newline = self.ten
        self.ch_space = self.add(self.thirty)(self.two)
        self.ch_F = self.add(self.thirty)(self.fourty)
        self.ch_0 = self.add(self.fourty)(self.eight)

        self.stdout_patcher = patch('sys.stdout', new=StringIO())
        self.mock_stdout = self.stdout_patcher.start()

    def tearDown(self):
        self.stdout_patcher.stop()

    def test_unchurch(self):
        """
        Basic tests for the unchurch method
        """
        self.assertEqual(unchurch(self.zero), 0)
        self.assertEqual(unchurch(self.three), 3)
        self.assertEqual(unchurch(self.four), 4)
        self.assertEqual(unchurch(self.thirty), 30)

    def test_unchurch_list_implementation_a(self):
        """
        Test the unchurch list function using list implementation a
        defined in this module.
        """
        impl = self._list_implementation_a()
        a0 = impl.cons(self.zero)(impl.nil)
        a1 = impl.cons(self.one)(a0)
        a2 = impl.cons(self.two)(a1)
        a3 = impl.cons(self.three)(a2)

        ul = unchurch_list(a3, head=impl.head, tail=impl.tail, isnil=impl.isnil)
        
        self.assertEqual([3, 2, 1, 0], [unchurch(elem) for elem in ul])

    def test_unchurch_list_implementation_b(self):
        """
        Test the unchurch list function using list implementation b
        defined in this module.
        """
        impl = self._list_implementation_b()
        a0 = impl.cons(self.zero)(impl.nil)
        a1 = impl.cons(self.one)(a0)
        a2 = impl.cons(self.two)(a1)
        a3 = impl.cons(self.three)(a2)

        ul = unchurch_list(a3, head=impl.head, tail=impl.tail, isnil=impl.isnil)
        
        self.assertEqual([3, 2, 1, 0], [unchurch(elem) for elem in ul])

    def test_church_print_implementation_a(self):
        """
        Test the church print function using list implementation a
        defined in this module.
        """
        impl = self._list_implementation_a()
        a0 = impl.cons(self.ch_newline)(impl.nil)
        a1 = impl.cons(self.ch_0)(a0)
        a2 = impl.cons(self.ch_space)(a1)
        a3 = impl.cons(self.ch_F)(a2)

        church_print(a3, head=impl.head, tail=impl.tail, isnil=impl.isnil)
        
        self.assertEqual(self.mock_stdout.getvalue(), 'F 0\n')

    def _list_implementation_a(self):
        """
        Return a Church list implementation for using in tests

        This implementation uses a single pair. This implementation
        was written without copy/paste from any solution code.
        """
        true = lambda a: lambda b: a
        false = lambda a: lambda b: b
        pair = lambda x: lambda y: lambda z: (z)(x)(y)
        first = lambda p: p(true)
        second = lambda p: p(false)
        isnil = lambda l: l(lambda h: lambda t: lambda d: false)(true)
        return ListImpl(
            cons=pair,
            head=first,
            tail=second,
            nil=false,
            isnil=isnil
        )

    def _list_implementation_b(self):
        """
        Return a Church list implementation for using in tests

        This implementation uses a right fold. This implementation
        was written without copy/paste from any solution code.
        """
        true = lambda a: lambda b: a
        false = lambda a: lambda b: b
        pair = lambda x: lambda y: lambda z: (z)(x)(y)
        first = lambda p: p(true)
        second = lambda p: p(false)
        isnil = lambda l: l(lambda h: lambda t: false)(true)
        cons = lambda h: lambda t: lambda c: lambda n: c(h)(t(c)(n))
        head = lambda l: l(true)(false)
        tail = (
            lambda l: lambda c: lambda n:
            l(lambda h: lambda t: lambda g: g(h)(t(c)))
            (lambda t: n)(false)
        )
        return ListImpl(
            cons=cons,
            head=head,
            tail=tail,
            nil=false,
            isnil=isnil
        )
