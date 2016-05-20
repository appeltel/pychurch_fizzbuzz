"""
_printer_tests_

Tests for the printer module, ensure that it works
correctly separate of the proposed solution and for
differing Church list implementations
"""
import unittest
import unittest.mock
from collections import namedtuple

from fizzbuzz.printer import (
    unchurch,
    unchurch_list
)

ListImpl = namedtuple('ListImpl', ['cons', 'head', 'tail', 'nil', 'isnil'])


class TestPrinter(unittest.TestCase):

    def test_unchurch(self):
        """
        Basic tests for the unchurch method
        """
        zero = lambda f: lambda x: x
        three = lambda f: lambda x: f(f(f(x)))
        self.assertEqual(unchurch(zero), 0)
        self.assertEqual(unchurch(three), 3)

    def test_unchurch_list_implementation_a(self):
        """
        Test the unchurch list function using list implementation a
        defined in this module.
        """
        impl = self._list_implementation_a()
        zero = lambda f: lambda x: x
        one = lambda f: lambda x: f(x)
        two = lambda f: lambda x: f(f(x))
        three = lambda f: lambda x: f(f(f(x)))
        a0 = impl.cons(zero)(impl.nil)
        a1 = impl.cons(one)(a0)
        a2 = impl.cons(two)(a1)
        a3 = impl.cons(three)(a2)

        ul = unchurch_list(a3, head=impl.head, tail=impl.tail, isnil=impl.isnil)
        
        self.assertEqual([3, 2, 1, 0], [unchurch(elem) for elem in ul])

    def test_unchurch_list_implementation_b(self):
        """
        Test the unchurch list function using list implementation b
        defined in this module.
        """
        impl = self._list_implementation_b()
        zero = lambda f: lambda x: x
        one = lambda f: lambda x: f(x)
        two = lambda f: lambda x: f(f(x))
        three = lambda f: lambda x: f(f(f(x)))
        a0 = impl.cons(zero)(impl.nil)
        a1 = impl.cons(one)(a0)
        a2 = impl.cons(two)(a1)
        a3 = impl.cons(three)(a2)

        ul = unchurch_list(a3, head=impl.head, tail=impl.tail, isnil=impl.isnil)
        
        self.assertEqual([3, 2, 1, 0], [unchurch(elem) for elem in ul])

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
